@echo off
SET output=%~n1_libx264_8MB.mp4
python %~dp0discord_vid/disvid_libx264.py -i %1 -c:v libx264 -vf scale=1280:-1 -r 30 "%output%"
