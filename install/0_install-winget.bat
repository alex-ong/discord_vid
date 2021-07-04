@echo off

echo "Trying to find winget.exe..."
WHERE winget

IF %ERRORLEVEL% EQU 0 (
 echo winget is already installed
 pause
 exit /B 0
)

echo Installation of this program is manual :(
echo.
echo Please go to https://github.com/microsoft/winget-cli/releases
echo and install the ".msixbundle"
echo.
echo Press any key to open your browser at that address.
echo This window will close as soon as we open that browser tab :)
pause
start https://github.com/microsoft/winget-cli/releases
