@echo off
setlocal
cd /d "%~dp0"

where python >nul 2>&1
if errorlevel 1 (
    echo Python was not found. Install Python 3.10 or newer and make sure it is on PATH.
    exit /b 1
)

python -m nuitka --version >nul 2>&1
if errorlevel 1 (
    echo Nuitka is not installed for this Python interpreter.
    echo Install it with: python -m pip install nuitka
    exit /b 1
)

python -m nuitka --onefile --enable-plugin=tk-inter --windows-console-mode=disable --output-dir=dist --output-filename=IPPoint.exe ippoint.py
if errorlevel 1 (
    echo Build failed.
    exit /b 1
)

echo.
echo Build complete: dist\IPPoint.exe
endlocal
