#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

PYTHON="${PYTHON:-python3}"
if ! command -v "$PYTHON" >/dev/null 2>&1; then
    echo "Python 3 was not found. Install Python 3.10 or newer."
    exit 1
fi

VENV_DIR="$PWD/.venv"
VENV_PYTHON="$VENV_DIR/bin/python"

if [ ! -x "$VENV_PYTHON" ]; then
    echo "Creating project virtual environment..."
    "$PYTHON" -m venv "$VENV_DIR"
fi

echo "Installing or updating Nuitka in the project virtual environment..."
"$VENV_PYTHON" -m pip install --upgrade nuitka

echo "Building IPPoint for Linux..."
"$VENV_PYTHON" -m nuitka \
    --onefile \
    --enable-plugin=tk-inter \
    --output-dir=dist \
    --output-filename=IPPoint \
    ippoint.py

echo
echo "Build complete: dist/IPPoint"
