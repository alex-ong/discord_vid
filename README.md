# Discord Video Resizer
Calculate and forward FFMPEG commands, staying under Discords 8MB limit.

* You can just drag and drop a file into discord-vid.bat.
* Otherwise, write your own version of discord-vid.bat

You can also add `discord_vid` to `PATH`, enabling you to run: 
`dv filename.mp4`

# Resolution

If you have Nitro, go to `discord_vid/disvid_lib.py` and change this line
`NITRO=False` to `NITRO=True`

| Preset        | 8MB(default) | 50MB(Nitro=True) |
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
* Download and unzip https://ffmpeg.org/download.html
	* Add it to your path.
* Download and install Python 3 https://www.python.org/downloads/windows/
* (Optional) You can run `ADD_TO_PATH.bat` to add this directory to your path.