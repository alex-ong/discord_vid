"""
Basic global config file.
"""
import json
from collections import OrderedDict

DEFAULT_CONFIG = "data/DEFAULT_CONFIG.json"
USER_CONFIG = "data/USER_CONFIG.json"

CONFIG = None


def get_config():
    """lazily gets the config file"""
    global CONFIG  # pylint: disable=global-statement

    if CONFIG is not None:
        return CONFIG
    with open(DEFAULT_CONFIG, "r", encoding="utf8") as default_file:
        data = json.load(default_file, object_pairs_hook=OrderedDict)

    try:
        with open(USER_CONFIG, "r", encoding="utf8") as user_file:
            data2 = json.load(user_file, object_pairs_hook=OrderedDict)
    except FileNotFoundError:
        data2 = {}

    data.update(data2)
    save_config(data)

    CONFIG = data
    return CONFIG


def save_config(data):
    """saves the config file"""
    with open(USER_CONFIG, "w", encoding="utf8") as config:
        json.dump(data, config, indent=4)


# python -m discord_vid.config
if __name__ == "__main__":
    get_config()
