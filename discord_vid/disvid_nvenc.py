"""
Discord vid nvenc implementation
"""

from install.install_ffmpeg import FFMPEG_EXE

# These are defined here because different encoders
# have different overheads. It's just a starting point.
# TARGET_SIZE = 7600
# TARGET_SIZE_NITRO = 50*1024


def extension():
    """return file extension for file converted using this module"""
    return "_nvenc.mp4"


def guess_target(max_size):
    """
    guesses the target size based on max size and AI
    """
    if max_size <= 9000:
        return 0.95 * max_size
    return 0.98 * max_size


def generate_file_cmd(v_rate, options):
    """
    Generates subprocess command to run, and the output filename.
    """

    input_options, output_options = options
    v_rate /= 1024
    # fmt: off
    command = (
        [FFMPEG_EXE, "-y"]
        + ["-v", "quiet", "-stats"]
        + input_options
        + [ "-c:v", "h264_nvenc",
            "-b:v", f"{v_rate:.0f}k", "-maxrate", f"{v_rate*1.5:.0f}k",
            "-minrate", f"{v_rate*0.7:.0f}k",
            "-bufsize", "1M"]
        + output_options # passthrough options.
        )

    # fmt: on
    output_file = output_options[-1]
    return ([command], output_file, None)
