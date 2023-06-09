"""
Helpers for installing ffmpeg
"""
import os
import subprocess

from install.helpers import download_file

FFMPEG_PATH = "./ffmpeg/"
FFMPEG_EXE = "ffmpeg/ffmpeg.exe"
FFPROBE_EXE = "ffmpeg/ffprobe.exe"
URL = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-full.7z"
OUT_ZIP = "./ffmpeg/ffmpeg.7z"


def install_ffmpeg(force=False):
    """installs ffmpeg if it doesn't exist"""
    if os.path.exists(FFMPEG_EXE) or force:
        download_ffmpeg()


def download_ffmpeg():
    """Download and unzip ffmpeg"""
    os.makedirs(FFMPEG_PATH, exist_ok=True)
    download_file(URL, OUT_ZIP)
    subprocess.call("./7z/7za e ffmpeg/ffmpeg.7z *.exe -r -aoa -offmpeg")


# python -m install.install_ffmpeg
if __name__ == "__main__":
    download_ffmpeg()
