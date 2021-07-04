@echo off
SET output=%~n1_libx264_DISCORD.mp4
python %~dp0discord_vid/disvid_libx264.py -i %1 -c:v libx264 "%output%"
