import os
from discord_vid.preset import Preset, get_preset_options
from discord_vid.disvid_lib import (
guess_encoder, 
get_encoder_lib, 
Encoder, 
generate_file_loop,
bytes_to_mb,
kb_to_mb
)

class Task:
    def __init__(self, preset, filename):
        self.preset = preset
        self.filename = filename
        self.process = None

        self.preset = Preset.from_str(preset)
        

        self.size, self.output_options = get_preset_options(self.preset)
        self.size = list(self.size)
        
        self.input_options = ["-i", filename]
        self.encoder = guess_encoder()
        self.set_encoder(self.encoder)
    
    def set_encoder(self, encoder:Encoder):
        self.encoder_lib = get_encoder_lib(encoder)
        self.size[1] = self.encoder_lib.guess_target(self.size[2])

    def generate_file(self):
        options = [self.input_options, self.output_options[:]]
        filename = os.path.splitext(self.filename)[0] + self.encoder_lib.extension()
        options[1].append(filename)
        print(f"Converting {self.filename} using {self.preset.name}")
        generate_file_loop(self.encoder_lib.generate_file, self, options)

    def on_encoder_finish(self, size, finished=False):
        min_size, target_size, max_size = self.size
        if size < min_size:
            print("For some reason we got a REALLY low file size:")
            print(
                f"Actual: {bytes_to_mb(size)}\n" + f"Target {kb_to_mb(target_size)}"
            )
        elif size > max_size:
            print(
                "Uh oh, we're still over size.\n"
                + f"Actual: {bytes_to_mb(size)}\n"
                + f"Target supplied: {kb_to_mb(target_size)}"
            )
        else:
            print(
                f"Actual: {bytes_to_mb(size)}\n"
                + f"Target supplied: {kb_to_mb(target_size)}"
            )