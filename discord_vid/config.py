"""
Basic global config file.
"""

from dataclasses import asdict
import os
import sys
import json
from typing import Dict, List, Optional
from collections import OrderedDict

from pydantic.dataclasses import dataclass

DEFAULT_CONFIG = "data/DEFAULT_CONFIG.json"
USER_CONFIG = "data/USER_CONFIG.json"

CONFIG = None


@dataclass
class Preset:
    """Preset inside USER_CONFIG.json"""

    min_size_mb: float
    max_size_mb: float
    args: List[str]
    scale: Optional[str] = None


@dataclass
class Config:
    """
    USER_CONFIG.json
    """

    presets: Dict[str, Preset]
    default_preset: str
    simultaneous_tasks: int


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

    with open(default_config, "r", encoding="utf8") as default_file:
        data = json.load(default_file, object_pairs_hook=OrderedDict)

    try:
        with open(user_config, "r", encoding="utf8") as user_file:
            data2 = json.load(user_file, object_pairs_hook=OrderedDict)
    except FileNotFoundError:
        data2 = {}

    data.update(data2)
    CONFIG = Config(**data)
    save_config(CONFIG)
    print(asdict(CONFIG))
    return CONFIG


def save_config(data: Config):
    """saves the config file"""
    user_config = get_user_config_path()
    with open(user_config, "w", encoding="utf8") as config:
        data_dict = asdict(data)
        json.dump(data_dict, config, indent=4)


# python -m discord_vid.config
if __name__ == "__main__":
    get_config()
