@echo off
uv sync

set PYINSTALLER_ARGS=--noconfirm
if /i "%~1"=="clean" set PYINSTALLER_ARGS=%PYINSTALLER_ARGS% --clean

uv run pyinstaller main.spec %PYINSTALLER_ARGS%