"""
Toolkit for adding shift+rightclick context menu
"""
import os
import sys

INSTALL_SAMPLE = "data/sample_install.reg.bak"
INSTALL_ACTUAL = "data/install.reg"
UNINSTALL_ACTUAL = "data/uninstall.reg"


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
    lines = []
    exe = get_install_exe()
    icon = get_install_ico()
    with open(INSTALL_SAMPLE, "r", encoding="utf8") as file:
        for line in file:
            line = line.replace("{exe_path}", exe)
            line = line.replace("{icon_path}", icon)
            lines.append(line)

    for line in lines:
        print(line.strip())

    with open(INSTALL_ACTUAL, "w", encoding="utf8") as file:
        file.writelines(lines)


def install_context():
    """
    Installs the context file
    """
    print("We are going to install a registry shortcut to enable right click menu")
    print(
        "After completion, hold shift and right click a video"
        + " then select DiscordVid submenu to convert easily"
    )
    input("Press enter to continue. Press *No* if you don't want a context menu")
    os.startfile(get_install_path() + "/" + INSTALL_ACTUAL)


def uninstall_context():
    """
    Uninstalls the context file
    """
    print(
        "We are going to de-install a registry shortcut that previously enabled right click menu"
    )
    input("Press enter to continue. Press *Yes* to uninstall")
    os.startfile(get_install_path() + "/" + UNINSTALL_ACTUAL)


# python -m install.install_context"
if __name__ == "__main__":
    generate_context()
