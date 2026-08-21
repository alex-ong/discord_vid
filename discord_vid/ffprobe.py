"""
Wrapper around ffprobe
"""

import json
import subprocess
from dataclasses import dataclass
from enum import Enum

from install.install_ffmpeg import FFPROBE_EXE


class Codec(Enum):
    """Enum representing Codecs of source file"""

    UNKNOWN = 1
    H264 = 2
    H265 = 3

    @classmethod
    def from_str(cls, string: str):
        """creates Codec from a string"""
        if string.lower() == "h264":
            return Codec.H264
        if string.lower() == "hevc":
            return Codec.H265
        return Codec.UNKNOWN


@dataclass
class SourceVideoData:
    """Datatype representing source videos metadata"""

    codec: Codec
    resolution: tuple[int, int]
    duration: float


def get_video_data(filename):
    """gets video codec; h264, h265 or CPU"""
    result = subprocess.run(
        [
            FFPROBE_EXE,
            "-v",
            "quiet",
            "-print_format",
            "json",
            "-show_format",
            "-show_streams",
            filename,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=True,
        # skip allocating a console entirely, avoiding Windows Terminal's
        # slow console-handoff when it's the default terminal app
        creationflags=subprocess.CREATE_NO_WINDOW,
    )
    json_str = result.stdout
    data = json.loads(json_str)

    for stream in data["streams"]:
        if stream["codec_type"] == "video":
            resolution = (stream["width"], stream["height"])
            codec_name = stream["codec_name"]
            duration = get_duration(stream, data["format"])
            return SourceVideoData(
                codec=Codec.from_str(codec_name),
                resolution=resolution,
                duration=duration,
            )
    return None


def get_duration(stream, container_format):
    """
    gets duration from the video stream, falling back to the container's
    overall duration (some containers, e.g. mkv, omit per-stream duration)
    """
    if "duration" in stream:
        return float(stream["duration"])
    return float(container_format["duration"])
