@echo off
setlocal
cd /d "%~dp0"

set "VENV_DIR=%~dp0.venv"
set "VENV_PYTHON=%VENV_DIR%\Scripts\python.exe"

where python >nul 2>&1
if errorlevel 1 (
    echo Python was not found. Install Python 3.10 or newer and make sure it is on PATH.
    exit /b 1
)

if not exist "%VENV_PYTHON%" (
    echo Creating project virtual environment...
    python -m venv "%VENV_DIR%"
    if errorlevel 1 (
        echo Failed to create the virtual environment.
        exit /b 1
    )
)

echo Installing or updating Nuitka in the project virtual environment...
"%VENV_PYTHON%" -m pip install --upgrade nuitka
if errorlevel 1 (
    echo Failed to install Nuitka.
    exit /b 1
)

echo Building IPPoint...
"%VENV_PYTHON%" -m nuitka --onefile --enable-plugin=tk-inter --windows-console-mode=disable --output-dir=dist --output-filename=IPPoint.exe ippoint.py
if errorlevel 1 (
    echo Build failed.
    exit /b 1
)

echo.
echo Build complete: dist\IPPoint.exe
endlocal
