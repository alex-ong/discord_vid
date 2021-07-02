@echo off
echo %~dp0
SET output=%~n1_8MB.mp4
python %~dp0disvid.py -i %1 -c:v libx264 -vf scale=1280:-1 -r 30 %output%
pause