"""
Presets for users
"""

from enum import Enum

AUDIO_RATE = 64
AUDIO_RATE_NITRO = 128
FULL_SIZE_BYTES = 8 * 1024 * 1024
FULL_SIZE_BYTES_NITRO = 50 * 1024 * 1024
MIN_SIZE_BYTES_NITRO = 0.90 * FULL_SIZE_BYTES_NITRO
MIN_SIZE_BYTES = 0.92 * FULL_SIZE_BYTES

SIZE_8 = (MIN_SIZE_BYTES, 0, FULL_SIZE_BYTES)
SIZE_50 = (MIN_SIZE_BYTES_NITRO, 0, FULL_SIZE_BYTES_NITRO)


class Preset(Enum):
    """
    Preset enumerator class
    """

    EIGHT_MB_720P30 = 1
    EIGHT_MB_720P60 = 2
    FIFTY_MB_1080P30 = 3
    FIFTY_MB_1080P60 = 4
    DEFAULT = 5

    @staticmethod
    def from_str(label: str):
        """
        converts from string to preset
        """
        result = Preset.from_intstr(label)
        if result is None:
            try:
                result = Preset[label.upper()]
            except KeyError:
                print(f"Invalid preset: {label}")
                return Preset.DEFAULT
        return result

    @staticmethod
    def from_intstr(label: str):
        """
        converts from integer string to preset
        """
        try:
            value = int(label)
            return Preset(value)
        except ValueError:
            return None


def get_preset_options(preset: Preset):
    """
    returns filesize and ffmpeg options for a preset
    """
    if preset == Preset.EIGHT_MB_720P30:
        return (SIZE_8, ["-vf", "scale=-1:720", "-r", "30", "-b:a", "64k"])
    if preset == Preset.EIGHT_MB_720P60:
        return (SIZE_8, ["-vf", "scale=-1:720", "-r", "60", "-b:a", "64k"])
    if preset == Preset.FIFTY_MB_1080P30:
        return (SIZE_50, ["-vf", "scale=-1:1080", "-r", "30", "-b:a", "128k"])
    if preset == Preset.FIFTY_MB_1080P60:
        return (SIZE_50, ["-vf", "scale=-1:1080", "-r", "60", "-b:a", "128k"])
    return []
