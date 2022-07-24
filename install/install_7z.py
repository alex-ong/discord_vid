"""
We need 7zip application as it is compressed as BCJ2.
Python's py7zr does not support this format unfortunately.
"""
import subprocess
import os

from install.helpers import add_to_path

SEVEN_ZIP_INSTALL_PATH = "C:\\Program Files\\7-Zip\\"


def install_7z(force=False):
    """
    Installs 7z if not installed
    """
    is_installed = subprocess.call("where 7z")
    if is_installed != 0 or force:
        download_7z()


def download_7z():
    """Downloads and unzips 7zip"""
    print("Installing 7zip")
    subprocess.call("winget install 7zip.7zip")
    add_to_path(SEVEN_ZIP_INSTALL_PATH)
    os.environ["PATH"] += f";{SEVEN_ZIP_INSTALL_PATH};"
    is_installed = subprocess.call("where 7z")
    print(f"7zip on path: {is_installed}")


# run as python -m install.install_7z
if __name__ == "__main__":
    install_7z()
