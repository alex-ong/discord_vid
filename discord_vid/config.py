"""
Basic global config file.
"""

import json
import os
import sys
from collections import OrderedDict
from dataclasses import asdict, dataclass

from discord_vid.lightweight_pydantic import to_dataclass

DEFAULT_CONFIG = "data/DEFAULT_CONFIG.json"
USER_CONFIG = "data/USER_CONFIG.json"

CONFIG = None


@dataclass
class Preset:
    """Preset inside USER_CONFIG.json"""

    min_size_mb: float
    max_size_mb: float
    args: list[str]
    scale: str | None = None


@dataclass
class Config:
    """
    USER_CONFIG.json
    """

    presets: dict[str, Preset]
    default_preset: str
    simultaneous_tasks: int
    encoder_cache: str | None = None
    encoder_cache_date: str | None = None


def get_default_config_path():
    """returns default config path"""
    folder = os.path.split(sys.argv[0])[0]
    root = os.path.abspath(folder)
    return root + "/" + DEFAULT_CONFIG


def get_user_config_path():
    """returns default user config path"""
    folder = os.path.split(sys.argv[0])[0]
    root = os.path.abspath(folder)
    return root + "/" + USER_CONFIG


def get_config():
    """lazily gets the config file"""
    global CONFIG  # pylint: disable=global-statement

    if CONFIG is not None:
        return CONFIG
    default_config = get_default_config_path()
    user_config = get_user_config_path()

    with open(default_config, encoding="utf8") as default_file:
        data = json.load(default_file, object_pairs_hook=OrderedDict)

    try:
        with open(user_config, encoding="utf8") as user_file:
            data2 = json.load(user_file, object_pairs_hook=OrderedDict)
    except FileNotFoundError, json.JSONDecodeError:
        # missing, or being written concurrently by another instance
        data2 = {}

    data.update(data2)
    CONFIG = to_dataclass(Config, data)
    print(asdict(CONFIG))
    return CONFIG


def save_config(data: Config):
    """saves the config file"""
    user_config = get_user_config_path()
    data_dict = asdict(data)

    # write to a temp file then atomically replace, so concurrently-launched
    # instances never read a partially-written/corrupted file
    tmp_path = f"{user_config}.tmp"
    with open(tmp_path, "w", encoding="utf8") as config:
        json.dump(data_dict, config, indent=4)
    os.replace(tmp_path, user_config)


# python -m discord_vid.config
if __name__ == "__main__":
    get_config()
