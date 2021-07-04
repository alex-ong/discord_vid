"""
discord vid libx264 implementation
"""
import sys
import subprocess
import os
from disvid_lib import generate_file_loop, NITRO, scale_rate

# These are defined here because different encoders
# Have different overheads
TARGET_SIZE = 7600
TARGET_SIZE_NITRO = 49500

        
def generate_file(v_rate, a_rate):
    """
    Generate file with nvenc options auto-injected
    """
    scale_cmd = scale_rate()
    # fmt: off
    command = (
        ["ffmpeg", "-y"]
        + sys.argv[1:-1] # passthrough options.
        + [ "-b:v", f"{v_rate:.0f}k", "-maxrate", f"{v_rate*2:.0f}k",
            "-b:a",f"{a_rate:.0f}k"]
        )
    if scale_cmd:
        command += scale_cmd.split()
    command += [sys.argv[-1]] # output filename
    # fmt: on

    print(" ".join(command))
    subprocess.run(command, check=True)
    return os.path.getsize(sys.argv[-1])


if __name__ == "__main__":
    size = TARGET_SIZE_NITRO if NITRO else TARGET_SIZE
    generate_file_loop(generate_file, size)