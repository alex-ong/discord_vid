"""
A bunch of useful library functions
"""
from datetime import timedelta, datetime
from threading import Thread, Event
import os
import subprocess
import sys
from enum import Enum
from queue import Queue, Empty

from install.install_ffmpeg import FFPROBE_EXE
from discord_vid import disvid_nvenc
from discord_vid import disvid_libx264
from discord_vid.renderingtask import RenderingTask


class Encoder(Enum):
    """Enum representing which encoder to use"""

    NVIDIA = 1
    CPU = 2
    INTEL = 3
    AMD = 4


def get_audio_rate(output_options):
    """
    Gets the audio rate from output optoins
    assumes its already specified in k (e.g: 64k, 128k)
    """
    audio_index = output_options.index("-b:a") + 1
    return int(output_options[audio_index].lower().replace("k", "")) * 1000


def get_encoder_lib(encoder: Encoder):
    """Converts from encoder enum to encoder library"""
    if encoder == Encoder.NVIDIA:
        return disvid_nvenc

    return disvid_libx264


def guess_encoder():
    """Checks if you have an nvidia gpu installed."""

    args = "wmic path win32_VideoController get name"
    result = subprocess.run(args.split(), capture_output=True, check=True)
    items = result.stdout.lower().split()
    items = [item.decode("utf-8") for item in items]

    if "nvidia" in items:
        return Encoder.NVIDIA

    return Encoder.CPU


def get_length(filename):
    """
    returns length of file in seconds
    """
    # fmt: off
    result = subprocess.run(
        [
            FFPROBE_EXE, "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            filename,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=True
    )
    # fmt: on

    return float(result.stdout)


def get_index(strings, array):
    """
    gets index of any of the strings in *strings* inside array *array*
    """
    for string in strings:
        try:
            return array.index(string)
        except ValueError:
            pass
    return None


def get_bitrate(target_size, length, audio_rate):
    """
    Returns target video bitrate based on target size, its length in seconds,
    and the audio bitrate in Kbps
    @target_size: Size in KByte
    @length: length in seconds
    @audio_rate: Rate in Kbits/s
    return: bitrate in Kbit/s
    """
    audio_size = audio_rate * length
    target_size_kbits = target_size * 8
    bitrate = (target_size_kbits - audio_size) / length
    return bitrate


def generate_file_loop_threaded(generate_file_func, task):
    """runs generate_file_loop in background thread"""
    thread = Thread(target=generate_file_loop, args=(generate_file_func, task))
    thread.start()


def generate_file_loop(generate_file_func, task):
    """
    Used by each encoder type;
    they run this loop, supplying their file generation function
    and starting target file size.
    """

    length = get_length(task.filename)
    task.set_video_length(length)

    min_size, target_size, max_size = task.size
    actual_size = file_loop_iter(target_size, generate_file_func, task)

    if task.is_cancelled():
        return

    if actual_size < min_size:
        task.on_encoder_finish(actual_size, target_size, False)
        target_size *= float(max_size) / (actual_size * 1.02)
        actual_size = file_loop_iter(target_size, generate_file_func, task)

    if task.is_cancelled():
        return

    while actual_size > max_size and not task.is_cancelled():
        task.on_encoder_finish(actual_size, target_size, False)
        target_size -= int(0.01 * max_size)
        actual_size = file_loop_iter(target_size, generate_file_func, task)

    task.on_encoder_finish(actual_size, target_size, True)


def kb_to_mb(value):
    """
    Converts KibiBytes to MebiBytes
    """
    return value / 1024.0


def bytes_to_mb(value):
    """
    Converts bytes to Mebibytes
    """
    return value / 1024.0 / 1024.0


def file_loop_iter(target_size, ffmpeg_command_gen, task):
    """
    Generates ffmpeg commands and cleanup functions to run, then runs them.
    """
    task_data = generate_file_loop_iter(target_size, ffmpeg_command_gen, task)
    render_task = RenderingTask(task_data, Event(), task.callbacks.update)
    task.set_render_task(render_task)
    return execute_file_loop_iter(render_task)


def generate_file_loop_iter(target_size, ffmpeg_command_gen, task):
    """
    one loop of the file generation process
    """
    audio_rate = get_audio_rate(task.current_options[1])
    bitrate = get_bitrate(target_size, task.video_length, audio_rate)

    if bitrate < 0:
        raise ValueError("Not enough bits for video")

    return ffmpeg_command_gen(bitrate, task.current_options)


def execute_file_loop_iter(render_task):
    """
    Executes a set of ffmpeg commands, and the cleanup functions.
    Calls on_update while ffmpeg is running
    """

    for index, command in enumerate(render_task.commands):
        run_ffmpeg_with_status(
            command,
            render_task.stop_event,
            render_task.on_update,
            (index, len(render_task.commands)),
        )

    if render_task.cleanup is not None:
        render_task.cleanup(render_task.output_file)

    return os.path.getsize(render_task.output_file)


def enqueue_output(out, queue, stop_event):
    """enqueues a line from the process to the queue"""
    for line in out:
        queue.put(line)
        if stop_event.is_set():
            break
    out.close()


def run_ffmpeg_with_status(command, stop_event, callback, subtask_id):
    """Runs ffmpeg, calling callback with the percentage"""
    print(command)
    queue = Queue()

    with subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        bufsize=1,
        startupinfo=hide_ffmpeg(),
    ) as process:
        thread = Thread(target=enqueue_output, args=(process.stdout, queue, stop_event))
        thread.daemon = True
        thread.start()
        while not stop_event.is_set() and thread.is_alive():
            try:
                line = queue.get(timeout=0.1)
            except Empty:
                continue
            else:  # got line
                if callback is None:
                    continue

                progress_seconds = parse_time_line(line)
                if progress_seconds:
                    callback(progress_seconds, subtask_id)

        if stop_event.is_set():  # cancelled
            process.terminate()
        thread.join()


def parse_time_line(line):
    """converts ffmpeg status line to time in seconds"""
    if not line.startswith("frame"):
        return None
    pairs = line.split()
    time_str = [pair for pair in pairs if pair.startswith("time")][0]
    time_str = time_str.split("=")[1]  # 00:00:00.000
    if time_str.startswith("-"):  # negative time fix
        return None
    date_time = datetime.strptime(time_str.split(".")[0], "%H:%M:%S")
    milliseconds = float(time_str.split(".")[1]) * 10
    delta = timedelta(
        hours=date_time.hour,
        minutes=date_time.minute,
        seconds=date_time.second,
        milliseconds=milliseconds,
    )
    return delta.total_seconds()


def hide_ffmpeg():
    """returns a startupinfo that can hide ffmpeg"""
    startup_info = subprocess.STARTUPINFO()
    startup_info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    return startup_info


def main():
    """
    main function for this program
    """
    if "--guess_encoder" in sys.argv:
        has_nvidia = guess_encoder()
        print("We have NVIDIA!")
        sys.exit(0 if has_nvidia else 1)

    sys.exit(0)


if __name__ == "__main__":
    main()
