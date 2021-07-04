# Discord Video Resizer
Calculate and forward FFMPEG commands, staying under Discords 8MB limit.


* You can just drag and drop a file into discord-vid.bat.
* Otherwise, write your own version of discord-vid.bat

You can also add `discord_vid` to `PATH`, enabling you to run: 

`dv filename.mp4`

It uses fixed 64Kbit for Audio, and Dynamic Kbit for Video. 

If filesize is way too small (<7.5MB) then it will dynamically change target bitrate to get closer to 8MB.

After this, if the filesize is still too big after generation, it will reduce Target File Size by 100Kb until RealFileSize is under 8MB

# Requirements

* ffmpeg must be on your path https://ffmpeg.org/download.html
* Python 3.x