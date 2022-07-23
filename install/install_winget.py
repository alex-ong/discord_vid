import subprocess
import requests

import os
from install.helpers import download_file
WINGET_URL = "https://github.com/microsoft/winget-cli/releases/"
GITHUB_URL = "https://github.com"

def get_latest_url():
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
    is_installed = subprocess.call("where winget")
    if (is_installed != 0 or force):
        src = get_latest_url()
        dest = "winget.msixbundle"
        download_file(src, dest)
        os.startfile(dest)


if __name__ == "__main__":
    install_winget(True)