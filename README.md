# Discord Video Resizer
Calculate and forward FFMPEG commands, staying under Discords 8MB limit.

* You can just drag and drop a file into `dv.bat`.

You can also add `discord_vid` to `PATH`, enabling you to run: 

* `dv filename.mp4` from command line.

# Nitro 
If you have Nitro, go to `discord_vid/disvid_lib.py` and change the line
`NITRO=False` to `NITRO=True`

# Resolution
| Variable      | 8MB(default) | 50MB(Nitro=True) |
|---------------|--------------|------------------|
| Framerate     | 30           | Untouched        |
| Resolution    | 1280:-1      | Untouched        |
| Video Bitrate | Calculated   | Calculated       |
| Audio Bitrate | 64kbps       | 128kbps          |


# Requirements
* `ffmpeg` must be installed, on your path https://ffmpeg.org/download.html
	* this means you should be able to type `ffmpeg` into cmd and get a response
* `Python 3.x` installed and on your path
	* this means you sohiuld be able to type `python` into cmd and get a python3 terminal

# Installation

Installation will install a few tools to aid the installation process.

1) `winget` - this tool allows command line installation of common programs
2) `7-zip` - this is required to unzip ffmpeg
3) `ffmpeg` - this is required to re-encode the video
4) `python` - this is required to run the program itself.

Go inside the installation folder and run the scripts in order; you can read the `README.md` inside
that folder for more information