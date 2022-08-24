"""
Presets for users
"""

from discord_vid.config import get_config

MB_TO_BYTES = 1024 * 1024


def get_size(min_size, max_size):
    """Converts min/max tuple to min/target/max triplet"""
    return [min_size, 0, max_size]


def presetdata_to_options(data):
    """Convert json dictionary to tuple of size and options"""
    min_size = int(data["min_size_mb"] * MB_TO_BYTES)
    max_size = int(data["max_size_mb"] * MB_TO_BYTES)
    options = data["args"]
    return (get_size(min_size, max_size), options)


def get_preset_options(preset: str):
    """
    returns filesize and ffmpeg options for a preset given its name
    """
    config = get_config()
    presets = config["presets"]
    if preset.lower() == "default":
        preset = config["default_preset"]
    if preset not in presets:
        raise ValueError("Invalid preset: {preset}")
    return presetdata_to_options(presets[preset])


def get_presets():
    """ Return list of preset names """
    config = get_config()
    return config["presets"].keys()


def display_presets():
    """ Prints out preset names """
    config = get_config()
    presets = config["presets"].keys()
    print("Preset list:\n" + "\n".join(presets))
    default_preset = config["default_preset"]
    print(f"Default preset: {default_preset}")
    return config["presets"].keys()
