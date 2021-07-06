@echo off
SetLocal EnableDelayedExpansion

echo "Trying to find 7z.exe..."
WHERE 7z

IF %ERRORLEVEL% EQU 0 (
 echo 7zip is already installed
 pause
 exit /B 0
)

echo.
echo We can't find 7z. It might be installed; we just have to
echo add it to path so that we can run it from command-line
echo We are going to try adding 7-zip to the path.
echo.


For /F "Skip=2Tokens=1-2*" %%A In ('Reg Query HKCU\Environment /V PATH 2^>Nul') Do set USERPATH=%%C
echo New PATH variable (user, not system):
echo "%USERPATH%C:\Program Files\7-Zip;"

echo.
echo Would you like to add 7z to the path?

CHOICE /C YN /M "Press Y for Yes, N for No:"

if %ERRORLEVEL% EQU 1 (
	
	setx Path "!USERPATH!C:\Program Files\7-Zip;"
	rem sets path in this local window
	rem echo.
	rem echo %PATH%
	rem echo.
	pause
	set PATH=!PATH!C:\Program Files\7-Zip;
  
	echo.
	echo Trying to find 7z now that we've added it to path
	WHERE 7z
	IF !ERRORLEVEL! EQU 0 (
		echo 7zip is installed and found!
		pause
		exit /B 0
	)
) 

echo 7zip is not installed. Installing...
SetLocal DisableDelayedExpansion

winget install 7zip.7zip

echo Trying to find 7z now that we've actually installed it
WHERE 7z
IF %ERRORLEVEL% EQU 0 (
	echo 7zip is installed and found!
	pause
	exit /B 0
)

echo Failed to find 7-zip! Shit!
pause
exit /B 1