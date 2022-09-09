"""
Gui for when no arguments are passed
"""

from gui.uninstall_gui import main


def no_func():
    """an empty function"""
    return


def get_error_msg(presets, default_preset):
    """
    returns longform error message when
    not enough arguments presented
    """
    msg = "Usage: dv.exe <PRESET> <FILE_PATH>\n"
    msg += "dv.exe Default C:/files/test.mp4\n"
    msg += "\nPresets:\n"
    msg += "\n".join(presets) + "\n"
    msg += f"Default preset: {default_preset}\n"
    msg += "\n\n\n for more info: http://github.com/alex-ong/discord_vid"
    return msg


def show_noargs(msg):
    """shows popup for no arguments"""
    main("Error: Wrong arguments", msg, no_func)
