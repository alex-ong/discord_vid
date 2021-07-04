@echo off
SetLocal EnableDelayedExpansion

echo "Trying to find ffmpeg.exe..."
WHERE ffmpeg

IF %ERRORLEVEL% EQU 0 (
 echo ffmpeg is already installed
 echo You may want to double check that it's up to date.
 echo Generally if its within a few months its up to date enough.
 echo.
 echo ffmpeg has a new version every week~
 echo Here is it's current version:
 echo.
 ffmpeg -version
 pause
 where ffmpeg > ffmpeg_path.txt
 set /p ffmpeg_path=<ffmpeg_path.txt
 call :file_name_from_path ff_folder !ffmpeg_path!
 del ffmpeg_path.txt
  
 echo.
 echo Would you like to update ffmpeg in this folder:
 echo !ff_folder!
 
 echo If not sure, don't do it man!
 CHOICE /C YN /M "Press Y for Yes, N for No:"
 if !ERRORLEVEL! EQU 1 (
   echo hi
   chdir /d "!ff_folder!"
   goto install_app
 )
 exit /B 0
)

echo.
echo.
echo.
echo ffmpeg not found!
echo We are going to add ffmpeg to the path (before its installed)
echo then install it.
echo adding to path...

For /F "Skip=2Tokens=1-2*" %%A In ('Reg Query HKCU\Environment /V PATH 2^>Nul') Do set USERPATH=%%C
echo New PATH variable (user, not system):
echo "%USERPATH%%cd%\ffmpeg\;"
	setx Path "!USERPATH!%cd%\ffmpeg\;"	
	set PATH=!PATH!%cd%\ffmpeg\;
) 

:install_app

echo Downloading ffmpeg from https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-full.7z
echo.
echo.


rem download ffmpeg
powershell -command "wget https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-full.7z -OutFile ffmpeg.7z"
rem this will only extract .exe to ffmpeg folder
7z e ffmpeg.7z -offmpeg *.exe -r
del ffmpeg.7z

echo Trying to find ffmpeg now that we've fully installed it
WHERE ffmpeg
IF !ERRORLEVEL! EQU 0 (
	echo ffmpeg is installed and found!
	pause
	exit /B 0
) ELSE (
	echo We got problems; cant find ffmpeg even though we tried our best :(
)
goto eof


:file_name_from_path <resultVar> <pathVar>
(
    set "%~1=%~dp2"
	echo %~dp2
    exit /b
)

endlocal