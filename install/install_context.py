"""
Toolkit for adding shift+rightclick context menu
"""

import os
import sys
from discord_vid.preset import get_presets
import subprocess

INSTALL_ACTUAL = "data/install.reg"
UNINSTALL_ACTUAL = "data/uninstall.reg"


def get_uninstall_header_string():
    """returns uninstallation header string"""
    strings = [
        "Windows Registry Editor Version 5.00" + "\n",
        r"[-HKEY_CLASSES_ROOT\*\shell\DiscordVid]" + "\n",
        r"[-HKEY_CLASSES_ROOT\Directory\shell\DiscordVid]" + "\n",
    ]
    return strings


def get_header_string():
    """returns the header string"""
    strings = [
        r"Windows Registry Editor Version 5.00",
        r"",
        r"[HKEY_CLASSES_ROOT\*\shell\DiscordVid]",
        r'"MUIVerb"="DiscordVid"',
        r'"SubCommands"="DiscordVid.Default;DiscordVid.8MB_720p30;DiscordVid.8MB_720p60;DiscordVid.50MB_1080p30;DiscordVid.50MB_1080p60;DiscordVid.100MB"',
        r'"Extended"=""',
        r'"Icon"="{icon_path}"',
        r"",
        r"[HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\CommandStore\shell\DiscordVid.Default]",
        r'"MUIVerb"="Compress (default)"',
        r"[HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\CommandStore\shell\DiscordVid.Default\command]",
        r'@="\"{exe_path}\" \"default\" \"%1\""',
        r"",
    ]
    return "\n".join(strings)


def get_preset_string(quality: str, exe_path: str):
    """returns the string for installing one preset"""
    quality_readable = quality.replace("_", " ")
    preset_name = f"DiscordVid.{quality}"
    line1 = (
        r"[HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\CommandStore\shell"
        + "\\"
    )
    line1 += preset_name + "]\n"
    line2 = r'"MUIVerb"="Compress to ' + quality_readable + '"\n'

    line3 = (
        r"[HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\CommandStore\shell\DiscordVid."
        + f"{quality}"
        + r"\command]"
        + "\n"
    )
    line4 = r'@="\"' + exe_path + r"\" \"" + quality + r'\" \"%1\""' + "\n"

    preset = [line1, line2, line3, line4]

    uninstall_line = "[-" + line1[1:]

    return [preset, uninstall_line]


def get_install_path():
    """gets installation path"""
    result = os.path.dirname(sys.argv[0])
    result = os.path.abspath(result)
    result = result.replace("\\", "/")
    result = result.replace("/", "\\\\")
    return result


def get_install_exe():
    """gets path to exe"""
    return get_install_path() + "\\\\dv.exe"


def get_install_ico():
    """gets path to icon"""
    return get_install_path() + "/data/discordvidlogo-24-black.ico"


def generate_context():
    """
    Generates a context installation file
    """

    exe = get_install_exe()
    icon = get_install_ico()

    header = get_header_string()
    header = header.replace("{exe_path}", exe)
    header = header.replace("{icon_path}", icon)

    preset_lines = []
    uninstall_lines = []
    for preset in get_presets():
        preset_line, uninstall_line = get_preset_string(preset, exe)
        preset_lines.extend(preset_line)
        uninstall_lines.append(uninstall_line)

    with open(INSTALL_ACTUAL, "w", encoding="utf8") as file:
        file.write(header)
        file.writelines(preset_lines)

    with open(UNINSTALL_ACTUAL, "w", encoding="utf8") as file:
        file.writelines(get_uninstall_header_string())
        file.writelines(uninstall_lines)


def install_context():
    """
    Installs the context file
    """
    command = get_install_path() + "/" + INSTALL_ACTUAL
    os.startfile(command)


def uninstall_context():
    """
    Uninstalls the context file
    """    
    command = get_install_path() + "/" + UNINSTALL_ACTUAL
    os.startfile(command)


# python -m install.install_context"
if __name__ == "__main__":
    generate_context()
