@echo off
echo %~dp0
SET output=%~n1_8MB.mp4

rem This finds out what your GPU name is:
python %~dp0discord_vid\disvid_lib.py --check_nvidia

rem if you use "ERRORLVEL 0" rather than %ERRORLEVEL% EQU 0
rem it returns true for 1 and 5 and 64, wtf.
if %ERRORLEVEL% EQU 0 (
	%~dp0discord-vid-nvenc.bat %1
) else (
	%~dp0discord-vid-libx264.bat %1
)
