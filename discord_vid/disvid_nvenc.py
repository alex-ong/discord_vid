"""
discord vid libx264 implementation
"""
import subprocess
import os

from install.install_ffmpeg import FFMPEG_EXE

# These are defined here because different encoders
# have different overheads. It's just a starting point.
# TARGET_SIZE = 7600
# TARGET_SIZE_NITRO = 50*1024


def guess_target(max_size):
    """
    guesses the target size based on max size and AI
    """
    if max_size <= 9000:
        return 0.95 * max_size
    return 0.98 * max_size


def generate_file(v_rate, a_rate, options):
    """
    Generate file with nvenc options auto-injected
    """

    input_options, output_options = options
    v_rate /= 1024
    a_rate /= 1024
    # fmt: off
    command = (
        [FFMPEG_EXE, "-y"]
        + input_options
        + [ "-b:v", f"{v_rate:.0f}k", "-maxrate", f"{v_rate*1.5:.0f}k",
            "-minrate", f"{v_rate:.0f}k",
            "-bufsize", "1M",
            "-b:a",f"{a_rate:.0f}k"]
        + output_options # passthrough options.
        )

    # fmt: on
    output_file = output_options[-1]
    print(" ".join(command))
    subprocess.run(command, check=True)
    return os.path.getsize(output_file)
