@echo off
SET output=%~n1_nvenc_8MB.mp4
python %~dp0discord_vid/disvid_nvenc.py -i %1 -c:v h264_nvenc -pix_fmt yuv420p -vf scale=1280:-1 -r 30 -c:a aac -preset slow "%output%"