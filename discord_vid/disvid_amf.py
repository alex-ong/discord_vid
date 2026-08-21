"""
Discord vid amd amf implementation
"""

from install.install_ffmpeg import FFMPEG_EXE

# These are defined here because different encoders
# have different overheads. It's just a starting point.


def extension():
    """return file extension for file converted using this module"""
    return "_amf.mp4"


def guess_target(max_size):
    """
    guesses the target size based on max size and AI
    """
    if max_size <= 9000:
        return 0.95 * max_size
    return 0.98 * max_size


def get_scale_cmd(resolution, _):
    """
    returns list of (mode, command) pairs for hardware decode acceleration.
    hwaccel_output_format is deliberately left unset so ffmpeg auto-downloads
    decoded frames to system memory, keeping presets' own software "-vf"
    filters (e.g. scale=) working unmodified.
    :param str resolution: 1280:-1
    """
    decode_cmd = ["decode", ["-hwaccel", "d3d11va"]]
    if resolution is None:
        return [decode_cmd]
    return [decode_cmd, ["encode", ["-vf", f"scale={resolution}"]]]


def generate_file_cmd(v_rate, options):
    """
    Generates subprocess command to run, and the output filename.
    """

    input_options, output_options = options
    v_rate /= 1024
    # fmt: off
    command = (
        [FFMPEG_EXE, "-y"]
        + input_options
        + [ "-c:v", "h264_amf",
            "-b:v", f"{v_rate:.0f}k", "-maxrate", f"{v_rate*1.5:.0f}k",
            "-minrate", f"{v_rate*0.7:.0f}k",
            "-bufsize", "1M"]
        + output_options # passthrough options.
        )

    # fmt: on
    output_file = output_options[-1]
    return ([command], output_file, None)
