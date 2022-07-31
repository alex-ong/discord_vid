"""
discord vid libx264 implementation
"""
import subprocess
import os
from install.install_ffmpeg import FFMPEG_EXE

# These are defined here because different encoders
# Have different overheads
TARGET_FILE_SIZE = 8100
TARGET_FILE_SIZE_NITRO = 48500


def extension():
    """return file extension for file converted using this module"""
    return "_libx264.mp4"


def guess_target(max_size):
    """
    guesses the target size based on max size and AI
    """
    if max_size <= 9000:
        return 1.02 * max_size
    return 0.97 * max_size


def generate_file(v_rate, a_rate, options):
    """
    Generate file with libx264 2-pass options auto-injected
    """

    input_options, output_options = options
    v_rate /= 1024
    a_rate /= 1024

    output_no_file = output_options[:-1]
    # fmt: off
    command = ( #first pass
        [FFMPEG_EXE,  "-y"]
        + input_options
        + "-threads 8 -speed 4 -row-mt 1 -tile-columns 2 -vsync cfr".split()
        + f"-b:v {v_rate:.0f}k -minrate {v_rate/2:.0f}k".split()
        + f"-maxrate {v_rate*2:.0f}k -bufsize 1M".split()
        + "-an -pass 1 -f mp4".split()
        + output_no_file
        + ["NUL"]
        )

    # fmt: on
    print(" ".join(command))
    subprocess.run(command, check=True)

    # fmt: off
    command = ( #second pass
        [FFMPEG_EXE, "-y"]
        + input_options
        + f"-b:v {v_rate:.0f}k -minrate {v_rate/2:.0f}k".split()
        + f"-maxrate {v_rate*1.5:.0f}k -bufsize 1M".split()
        + "-threads 8 -speed 2 -row-mt 1 -tile-columns 2".split()
        + f"-b:a {a_rate:.0f}k".split()
        + "-pass 2".split()
        + output_options
    )
    # fmt: on
    subprocess.run(command, check=True)
    output_file = output_options[-1]

    return os.path.getsize(output_file)
