"""
Basic task framework on ffmpeg tasks
"""
import os
from discord_vid.preset import get_preset_options
from discord_vid.disvid_lib import (
    guess_encoder,
    get_encoder_lib,
    Encoder,
    generate_file_loop_threaded,
    bytes_to_mb,
)


class Task:
    """FFMPEG task"""

    def __init__(self, preset, filename):
        self.preset = preset
        self.filename = filename
        self.process = None

        self.size, self.output_options = get_preset_options(self.preset)
        self.size = list(self.size)

        self.input_options = ["-i", filename]
        self.encoder = guess_encoder()
        self.set_encoder(self.encoder)
        self.on_update_cb = None
        self.on_finish_cb = None
        self.video_length = None
        self.current_options = None  # options of currently running task

    def set_on_update(self, callback):
        """register the update callback"""
        self.on_update_cb = callback

    def set_on_finish(self, callback):
        """register the finish callback"""
        self.on_finish_cb = callback

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
        elif output_size < min_size:
            message = f"Too small: {output_size:.2f}MB"
        elif output_size > max_size:
            message = f"Too big: {output_size:.2f}MB"

        if self.on_finish_cb is not None:
            self.on_finish_cb(finished, message)
