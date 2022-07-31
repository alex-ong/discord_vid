"""
We need 7zip application as it is compressed as BCJ2.
Python's py7zr does not support this format unfortunately.
"""
import subprocess
import os

import requests
from install.helpers import add_to_path, download_file

SEVEN_ZIP_INSTALL_PATH = "C:\\Program Files\\7-Zip\\"

SEVEN_ZIP_URL = "https://www.7-zip.org/download.html"
SEVEN_ZIP_ROOT = "https://www.7-zip.org/"
GITHUB_URL = "https://github.com"


def get_latest_url():
    """get the latest .msixbundle from github"""
    data = requests.get(SEVEN_ZIP_URL)
    words = data.text.split()

    candidates = []
    for word in words:
        if ".exe" in word and word.startswith("href"):
            start = word.index('"') + 1
            end = word.rindex('"')
            word = word[start:end]
            print(word)
            candidates.append(word)

    return candidates[0]


def install_7z(force=False):
    """
    Installs 7z if not installed
    """
    is_installed = subprocess.call("where 7z")
    if is_installed != 0 or force:
        download_7z(force)


def download_7z(force=False):
    """Downloads and unzips 7zip"""
    print("Installing 7zip")
    add_to_path(SEVEN_ZIP_INSTALL_PATH)
    os.environ["PATH"] += f";{SEVEN_ZIP_INSTALL_PATH};"
    is_installed = subprocess.call("where 7z")
    print(f"7zip on path: {is_installed}")
    if is_installed != 0 or force:
        print("Installing 7zip by downloading it!")
        filename = get_latest_url()
        src = SEVEN_ZIP_ROOT + filename
        dest = os.path.basename(filename)
        download_file(src, dest)
        subprocess.call([dest, "/S"], shell=True)
        is_installed = subprocess.call("where 7z")
        print(f"7zip on path: {is_installed}")


# run as python -m install.install_7z
if __name__ == "__main__":
    install_7z()
