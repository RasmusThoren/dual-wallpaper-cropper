#!/bin/bash
set -e

APP_NAME="dual-wallpaper-cropper"

# Ensure required system packages exist
if ! command -v xrandr &> /dev/null; then
    echo "❌ xrandr not found. Please install with: sudo apt install x11-xserver-utils"
    exit 1
fi

if ! python3 -c "import tkinter" &> /dev/null; then
    echo "❌ Tkinter not available. Please install with: sudo apt install python3-tk"
    exit 1
fi

# Clean old builds
rm -rf build/ dist/ __pycache__

# Run PyInstaller
pyinstaller --onefile --noconsole \
  --name "$APP_NAME" \
  --hidden-import=PIL._tkinter_finder \
  wallpapercropper/app.py

echo "✅ Build complete!"
echo "Run it with: ./dist/$APP_NAME"
