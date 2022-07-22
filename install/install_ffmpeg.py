import os
import subprocess

from install.modify_path import download_file

FFMPEG_PATH = "./ffmpeg/"
FFMPEG_EXE = FFMPEG_PATH + "ffmpeg.exe"
URL = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-full.7z"
OUT_ZIP = "./ffmpeg/ffmpeg.7z"
def install_ffmpeg(force=False):
    if os.path.exists(FFMPEG_EXE) or force:
        download_ffmpeg()
    
def download_ffmpeg():
    os.makedirs(FFMPEG_PATH,exist_ok=True)
    download_file(URL, OUT_ZIP)
    subprocess.call("7z e ffmpeg/ffmpeg.7z *.exe -r -aoa -offmpeg")

# python -m install.install_ffmpeg
if __name__ == '__main__':
    download_ffmpeg()