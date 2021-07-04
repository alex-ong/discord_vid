@echo off
SET output=%~n1_nvenc_DISCORD.mp4
rem -preset slow gives us 2 pass automatically!
python %~dp0discord_vid/disvid_nvenc.py -i %1 -c:v h264_nvenc -pix_fmt yuv420p -c:a aac -preset slow "%output%"