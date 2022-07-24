"""
Installs winget
"""
import os
import subprocess
import requests

from install.helpers import download_file

WINGET_URL = "https://github.com/microsoft/winget-cli/releases/"
GITHUB_URL = "https://github.com"


def get_latest_url():
    """get the latest .msixbundle from github"""
    data = requests.get(WINGET_URL)
    words = data.text.split()

    candidates = []
    for word in words:
        if ".msixbundle" in word and word.startswith("href"):
            start = word.index('"') + 1
            end = word.rindex('"')
            word = word[start:end]
            candidates.append(word)

    return GITHUB_URL + candidates[0]


def install_winget(force=False):
    """download and install winget"""
    is_installed = subprocess.call("where winget")
    if is_installed != 0 or force:
        src = get_latest_url()
        dest = "winget.msixbundle"
        download_file(src, dest)
        os.startfile(dest)


# python -m install.install_winget
if __name__ == "__main__":
    install_winget()
