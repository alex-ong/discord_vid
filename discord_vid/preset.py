"""
Presets for users
"""

from discord_vid.config import get_config


def get_preset(preset_name: str):
    """
    returns filesize and ffmpeg options for a preset given its name
    """
    config = get_config()
    presets = config.presets
    if preset_name.lower() == "default":
        preset = config.presets["default_preset"]
    if preset_name not in presets:
        raise ValueError(f"Invalid preset: {preset}")
    return presets[preset_name]


def get_preset_names():
    """Return list of preset names"""
    config = get_config()
    return config.presets.keys()


def display_presets():
    """Prints out preset names"""
    presets = get_preset_names()
    print("Preset list:\n" + "\n".join(presets))
    default_preset = get_config().default_preset
    print(f"Default preset: {default_preset}")
    return (presets, default_preset)
