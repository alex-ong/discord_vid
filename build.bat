@echo off
uv sync

set PYINSTALLER_ARGS=--noconfirm
set DO_ZIP=0

for %%A in (%*) do (
    if /i "%%A"=="clean" set PYINSTALLER_ARGS=%PYINSTALLER_ARGS% --clean
    if /i "%%A"=="zip" set DO_ZIP=1
)

uv run pyinstaller main.spec %PYINSTALLER_ARGS%

if %DO_ZIP%==1 (
    pwsh -Command "Compress-Archive -Path dist -DestinationPath discord_vid-$((Get-Date).ToString('yyyyMMdd')).zip -Force"
)