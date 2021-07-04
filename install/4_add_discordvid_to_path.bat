@echo off

echo "Trying to find dv.bat..."
WHERE dv

IF %ERRORLEVEL% EQU 0 (
 echo discord_vid is already installed
 pause
 exit /B 0
)

setlocal enableextensions disabledelayedexpansion

set "newDir=..\"

rem With a subroutine   
call :resolve "%newDir%" resolvedDir

For /F "Skip=2Tokens=1-2*" %%A In ('Reg Query HKCU\Environment /V PATH 2^>Nul') Do set USERPATH=%%C
echo New path:
echo %USERPATH%%resolvedDir%;
echo Press enter to set your path, or close this prompt to cancel
pause
setx Path "%USERPATH%%resolvedDir%;"
set PATH=%PATH%%resolvedDir%;

echo All done!


echo Trying to find dv now that we've fully installed it
WHERE dv
IF %ERRORLEVEL% EQU 0 (
	echo dv is installed and found!
	pause
	exit /B 0
) ELSE (
	echo We got problems; cant find dv even though we tried our best :(
	pause
)

goto :eof

:resolve file/folder returnVarName
    rem Set the second argument (variable name) 
    rem to the full path to the first argument (file/folder)
    set "%~2=%~f1"
    goto :EOF