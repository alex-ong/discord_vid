"""
discord vid libx264 implementation
"""
import sys
import subprocess
import os
from disvid_lib import generate_file_loop

TARGET_FILE_SIZE = 8100


def generate_file(v_rate, a_rate):
    """
    Generate file with libx264 2-pass options auto-injected
    """

    # fmt: off
    command = ( #first pass
        "ffmpeg -y".split()
        + sys.argv[1:-1]
        + "-threads 8 -speed 4 -row-mt 1 -tile-columns 2 -vsync cfr".split()
        + f"-b:v {v_rate:.0f}k -minrate {v_rate/2:.0f}k".split()
        + f"-maxrate {v_rate*2:.0f}k -bufsize 1M".split()
        + "-an -pass 1 -f mp4 NUL".split()
    )
    # fmt: on

    print(" ".join(command))
    subprocess.run(command, check=True)

    # fmt: off
    command = ( #second pass
        "ffmpeg -y".split()
        + sys.argv[1:-1]
        + f"-b:v {v_rate:.0f}k -minrate {v_rate/2:.0f}k".split()
        + f"-maxrate {v_rate*1.5:.0f}k -bufsize 1M".split()
        + "-threads 8 -speed 2 -row-mt 1 -tile-columns 2".split()
        + f"-b:a {a_rate:.0f}k".split()
        + "-pass 2".split()
        + [sys.argv[-1]]
    )
    # fmt: on
    print(" ".join(command))
    subprocess.run(command, check=True)

    return os.path.getsize(sys.argv[-1])


if __name__ == "__main__":
    generate_file_loop(generate_file, TARGET_FILE_SIZE)
