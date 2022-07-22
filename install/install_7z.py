import subprocess
import os

from install.modify_path import add_to_path
SEVEN_ZIP_INSTALL_PATH = "C:\\Program Files\\7-Zip\\"

def install_7z(force=False):
    is_installed = subprocess.call("where 7z")
    if (is_installed != 0 or force):
        download_7z()

def download_7z():
    print("Installing 7zip")
    subprocess.call("winget install 7zip.7zip")
    add_to_path(SEVEN_ZIP_INSTALL_PATH)
    os.environ["PATH"] += f";{SEVEN_ZIP_INSTALL_PATH};"
    subprocess.call("where 7z")


def test():
    os.environ["PATH"] += f";{SEVEN_ZIP_INSTALL_PATH};"
    subprocess.call("where 7z")

# run as python -m install.install_7z
if __name__ == "__main__":
    test()