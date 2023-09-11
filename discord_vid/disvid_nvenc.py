"""
Discord vid nvenc implementation
"""

from install.install_ffmpeg import FFMPEG_EXE
from discord_vid.ffprobe import Codec, SourceVideoData

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

def get_scale_cmd(resolution, src_data: SourceVideoData):
    """
    returns scale command;
    and whether it occurs in decode or encode phase
    :param str resolution: 1280:-1
    """
    if resolution is None:
        return None, None
    if src_data.codec == Codec.UNKNOWN:
        return ["encode", ["-vf", resolution]]
    
    if src_data.codec == Codec.H264:
        codec = "h264_cuvid"
    elif src_data.codec == Codec.H265:
        codec = "hevc_cuvid"
    
    res_str = get_decode_resolution(resolution, src_data.resolution)
    return ["decode", ["-c:v", codec, "-resize", res_str]]
    
    
def get_decode_resolution(target_resolution, source_resolution):
    """
    convert from 1280:-1 and [1920,1080] to 1280x720
    """
    target_w, target_h = target_resolution.split(":")
    target_w = int(target_w)
    target_h = int(target_h)
    source_aspect = source_resolution[0]/float(source_resolution[1])
    if target_w == -1:
        target_w = int(target_h * source_aspect)
    elif target_h == -1:
        target_h = int(target_w / source_aspect)

    resolution_str = f"{target_w}x{target_h}"
    return resolution_str

def generate_file_cmd(v_rate, options):
    """
    Generates subprocess command to run, and the output filename.
    """

    input_options, output_options = options
    v_rate /= 1024
    # fmt: off
    command = (
        [FFMPEG_EXE, "-y"]
        #+ ["-v", "quiet", "-stats"]
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
