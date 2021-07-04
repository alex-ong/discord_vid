"""
discord vid libx264 implementation
"""
import sys
import subprocess
import os
from disvid_lib import generate_file_loop, NITRO, scale_rate

# These are defined here because different encoders
# Have different overheads
TARGET_FILE_SIZE = 8100
TARGET_FILE_SIZE_NITRO = 48500


def generate_file(v_rate, a_rate):
    """
    Generate file with libx264 2-pass options auto-injected
    """
    scale_cmd = scale_rate()
    # fmt: off
    command = ( #first pass
        "ffmpeg -y".split()
        + sys.argv[1:-1]
        + "-threads 8 -speed 4 -row-mt 1 -tile-columns 2 -vsync cfr".split()
        + f"-b:v {v_rate:.0f}k -minrate {v_rate/2:.0f}k".split()
        + f"-maxrate {v_rate*2:.0f}k -bufsize 1M".split()
        + "-an -pass 1 -f mp4".split()
        ) 
    if scale_cmd is not None:
        command += scale_cmd.split()
    command += ["NUL"]
    
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
    )
    if scale_cmd is not None:
        command += scale_cmd.split()
    command += [sys.argv[-1]]
    # fmt: on
    print(" ".join(command))
    subprocess.run(command, check=True)

    return os.path.getsize(sys.argv[-1])


if __name__ == "__main__":
    size = TARGET_FILE_SIZE_NITRO if NITRO else TARGET_FILE_SIZE
    generate_file_loop(generate_file, size)
