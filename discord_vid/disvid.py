"""
Main entrypoint for command line based conversion
"""
import os
import sys

from discord_vid import disvid_lib
from discord_vid import disvid_libx264
from discord_vid import disvid_nvenc
from discord_vid.preset import Preset, get_preset_options


def convert(preset: str, filename):
    """
    Converts a given filename using the provided preset
    """
    preset = Preset.from_str(preset)
    print(f"Converting {filename} using {preset.name}")

    size, output_options = get_preset_options(preset)
    size = list(size)

    input_options = ["-i", filename]
    options = [input_options, output_options]
    has_nvidia = disvid_lib.check_nvidia()
    # choose encoder
    if has_nvidia:
        size[1] = disvid_nvenc.guess_target(size[2])
        filename = os.path.splitext(filename)[0] + "_nvenc.mp4"
        output_options += [filename]
        print(output_options)
        disvid_lib.generate_file_loop(disvid_nvenc.generate_file, size, options)
    else:
        size[1] = disvid_libx264.guess_target(size[2])
        filename = os.path.splitext(filename)[0] + "_libx264.mp4"
        output_options += [filename]
        disvid_lib.generate_file_loop(disvid_libx264.generate_file, size, options)


# pipenv run python -m discord_vid.disvid {PRESET} file.mp4
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("python -m discord_vid.disvid {PRESET} file.mp4")
        sys.exit()
    convert(sys.argv[1], sys.argv[2])
