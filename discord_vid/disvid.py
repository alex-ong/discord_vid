"""
Main entrypoint for command line based conversion
"""
import os
import sys

from discord_vid import disvid_lib
from discord_vid import disvid_libx264
from discord_vid import disvid_nvenc
from discord_vid.preset import Preset, get_preset_options
from discord_vid.task import Task

def convert(task: Task):
    """
    Converts a given filename using the provided preset
    """
    task.generate_file()


# pipenv run python -m discord_vid.disvid {PRESET} file.mp4
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("python -m discord_vid.disvid {PRESET} file.mp4")
        sys.exit()
    print(sys.argv)
    convert(sys.argv[1], sys.argv[2])
