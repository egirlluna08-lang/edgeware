@echo off
echo.
echo Checking for Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python not found! Installing Pillow requirements...
    echo.
    echo Please download Python from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    echo Then run this file again
    pause
    exit /b 1
)

echo Installing Pillow...
pip install Pillow --quiet

echo.
echo Starting edgeware...
echo.
python edgeware.py

pause
