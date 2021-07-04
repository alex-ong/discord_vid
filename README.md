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

* ffmpeg must be on your path https://ffmpeg.org/download.html
* Python 3.x

# Installation
You can run `ADD_TO_PATH.bat` to add this directory to your path.