@echo off

echo Trying to see if python is there
echo Trying to find python
WHERE /Q python 
IF %ERRORLEVEL% EQU 0 (
	echo python is already installed and found!
	pause
	exit /B 0
) ELSE (
	echo We got problems; cant find ffmpeg even though we tried our best :(
)
goto eof

mkdir C:\Python39
winget install python.python.3 --version 3.9.5150.0 --override "InstallAllUsers=1 TargetDir=C:\Python39 DefaultCustomTargetDir=C:\Python39 PrependPath=1 CompileAll=1"

echo Installed!
pause