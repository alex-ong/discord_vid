"""
Basic task framework on ffmpeg tasks
"""
import os
from collections import namedtuple
from discord_vid.preset import get_preset_options
from discord_vid.disvid_lib import (
    guess_encoder,
    get_encoder_lib,
    Encoder,
    generate_file_loop_threaded,
    bytes_to_mb,
)


TaskCallbacks = namedtuple("TaskCallbacks", ["start", "update", "finish"])


class Task:
    """FFMPEG task"""

    def __init__(self, preset, filename):
        self.preset = preset
        self.filename = filename

        self.size, self.output_options = get_preset_options(self.preset)
        self.size = list(self.size)

        self.input_options = ["-i", filename]
        self.encoder = guess_encoder()
        self.set_encoder(self.encoder)
        self.callbacks = None
        self.video_length = None
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
        self.size[1] = encoder_lib.guess_target(self.size[2])

    def set_video_length(self, seconds):
        """Sets the video's length"""
        self.video_length = seconds

    def generate_file(self):
        """generates the file by calling generate_file_loop"""
        options = [self.input_options, self.output_options[:]]
        encoder_lib = get_encoder_lib(self.encoder)
        filename = os.path.splitext(self.filename)[0] + encoder_lib.extension()
        options[1].append(filename)
        self.current_options = options
        print(f"Converting {self.filename} using {self.preset}")
        generate_file_loop_threaded(encoder_lib.generate_file_cmd, self)

    def on_encoder_finish(self, output_size, target_size, finished=False):
        """callback for when encoder finishes"""
        size = (bytes_to_mb(item) for item in self.size)
        target_size = bytes_to_mb(target_size)
        output_size = bytes_to_mb(output_size)
        min_size, _, max_size = size

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
