"""
Basic task framework on ffmpeg tasks
"""
from dataclasses import dataclass
import os
from collections import namedtuple
from discord_vid.preset import get_preset
from discord_vid.disvid_lib import (
    guess_encoder,
    get_encoder_lib,
    Encoder,
    generate_file_loop_threaded,
    bytes_to_mb,
)
from discord_vid.ffprobe import get_video_data

TaskCallbacks = namedtuple("TaskCallbacks", ["start", "update", "finish"])
MB_TO_BYTES = 1024 * 1024


@dataclass
class FileSizeTarget:
    """File size target in bytes"""

    min_size: int
    max_size: int
    target_size: int


class Task:
    """FFMPEG task"""

    def __init__(self, preset_name, filename):
        self.preset_name = preset_name
        self.filename = filename
        self.preset = get_preset(self.preset_name)
        self.file_size = None  # setup later when we set encoder
        self.input_options = ["-i", filename]
        self.encoder = guess_encoder()
        self.set_encoder(self.encoder)
        self.callbacks = None
        self.src_data = get_video_data(self.filename)

        self.finished = False
        self.render_task = None
        self.current_options = None

    def set_render_task(self, render_task):
        """sets the render task which is the current ffmpeg commands running"""
        self.render_task = render_task

    def set_callbacks(self, callbacks: TaskCallbacks):
        """register callbacks for when starting, updating and finishing a task"""
        self.callbacks = callbacks

    def set_encoder(self, encoder: Encoder):
        """sets encoder and target starting size"""
        encoder_lib = get_encoder_lib(encoder)
        min_size = self.preset.min_size_mb * MB_TO_BYTES
        max_size = self.preset.max_size_mb * MB_TO_BYTES
        target_size = encoder_lib.guess_target(max_size)
        self.file_size = FileSizeTarget(
            min_size=min_size, max_size=max_size, target_size=target_size
        )

    def generate_file(self):
        """generates the file by calling generate_file_loop"""
        options = [self.input_options, self.preset.args[:]]
        encoder_lib = get_encoder_lib(self.encoder)

        # set scaling (pre vs post)
        pre_post, command = encoder_lib.get_scale_cmd(self.preset.scale, self.src_data)
        if pre_post == "decode":
            options[0] = command + options[0]
        elif pre_post == "encode":
            options[1] = command + options[1]

        # set output filename
        filename = os.path.splitext(self.filename)[0] + encoder_lib.extension()
        options[1].append(filename)

        self.current_options = options
        print(f"Converting {self.filename} using {self.preset_name}")
        generate_file_loop_threaded(encoder_lib.generate_file_cmd, self)

    def on_encoder_finish(self, output_size, target_size, finished=False):
        """callback for when encoder finishes"""
        min_size = bytes_to_mb(self.file_size.min_size)
        target_size = bytes_to_mb(target_size)
        output_size = bytes_to_mb(output_size)
        max_size = bytes_to_mb(self.file_size.max_size)

        if finished:
            message = f"Finished: {output_size:.2f}MB"
            self.finished = True
        elif output_size < min_size:
            message = f"Too small: {output_size:.2f}MB"
        elif output_size > max_size:
            message = f"Too big: {output_size:.2f}MB"

        if self.callbacks.finish is not None:
            self.callbacks.finish(finished, message)

    def cancel(self):
        """call to kill the task immediately"""
        if not self.finished:
            print("cancel called")
            self.render_task.cancel()

    def is_cancelled(self):
        """returns if the task is cancelled"""
        if self.render_task is not None:
            return self.render_task.is_cancelled()
        return False
