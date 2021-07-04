"""
A bunch of useful library functions
"""
import glob
import os
import subprocess
import sys

AUDIO_RATE = 64
FULL_SIZE_BYTES = 8 * 1024 * 1024
MIN_SIZE_BYTES = int(7.5 * 1024 * 1024)


def check_nvidia():
    """
    Checks if you have an nvidia gpu installed.
    """

    args = "wmic path win32_VideoController get name"
    result = subprocess.run(args.split(), capture_output=True, check=True)
    items = result.stdout.lower().split()
    items = [item.decode("utf-8") for item in items]

    if "nvidia" in items:
        return True

    return False


def get_length(filename):
    """
    returns length of file in seconds
    """
    # fmt: off
    result = subprocess.run(
        [
            "ffprobe", "-v", "error",
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


def delete_logs():
    """
    Deletes logs generated by ffmpeg2pass
    """
    file_list = glob.glob("ffmpeg2pass-*.log")
    # Iterate over the list of file_paths & remove each file.
    for file_path in file_list:
        os.remove(file_path)

    file_list = glob.glob("ffmpeg2pass-*.mbtree")
    # Iterate over the list of file_paths & remove each file.
    for file_path in file_list:
        os.remove(file_path)


def get_bitrate(target_size, length):
    """
    Returns target video bitrate based on target size, its length in seconds,
    and the audio bitrate
    """
    bitrate = (target_size * 8 - AUDIO_RATE * length) / length
    return bitrate


def generate_file_loop(generate_file_func, target_size):
    """
    Used by each encoder type;
    they run this loop, supplying their file generation function
    and starting target file size.
    """
    if len(sys.argv) < 2:
        print(f"usage: {sys.argv[0]} <regular ffmpeg commands>")

    i_index = get_index(["-i", "-I"], sys.argv)
    if i_index is None:
        print("'-i' not found")
        sys.exit()

    filename = sys.argv[i_index + 1]
    print(f"Getting file:{filename}")
    length = get_length(filename)
    print(f"File length:{length} seconds")
    print(f"Estimated audio size:, {AUDIO_RATE*length/8}KB")

    actual_size = generate_file_loop_iter(target_size, length, generate_file_func)

    if actual_size < MIN_SIZE_BYTES:
        print("For some reason we got a REALLY low file size.")
        target_size *= float(FULL_SIZE_BYTES) / actual_size
        actual_size = generate_file_loop_iter(target_size, length, generate_file_func)

    while actual_size > 8 * 1024 * 1024:
        print("Uh oh, we're still over size: ", actual_size / 1024 / 1024.0)
        target_size -= 100
        actual_size = generate_file_loop_iter(target_size, length, generate_file_func)


def generate_file_loop_iter(target_size, length, func):
    """
    one loop of the file generation process
    """
    bitrate = get_bitrate(target_size, length)
    if bitrate < 0:
        print("Unfortunately there is not enough bits for video!")
        sys.exit()
    actual_size = func(bitrate, AUDIO_RATE)
    delete_logs()  # only necessary for libx264, but lets just delete it always.
    return actual_size


def main():
    """
    main function for this program
    """
    if "--check_nvidia" in sys.argv:
        has_nvidia = check_nvidia()
        print("We have NVIDIA!")
        sys.exit(0 if has_nvidia else 1)

    sys.exit(0)


if __name__ == "__main__":
    main()
