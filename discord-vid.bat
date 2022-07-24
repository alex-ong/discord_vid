@echo off
echo %~dp0
cd /d %~dp0
python -m discord_vid.disvid 1 %1

