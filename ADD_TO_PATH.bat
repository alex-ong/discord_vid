@echo off
echo Adding this directory to path: %cd%

For /F "Skip=2Tokens=1-2*" %%A In ('Reg Query HKCU\Environment /V PATH 2^>Nul') Do set USERPATH=%%C
echo New path:
echo %USERPATH%%cd%
echo Press enter to set your path, or close this prompt to cancel
pause
setx Path "%USERPATH%%cd%;"
echo All done!
pause