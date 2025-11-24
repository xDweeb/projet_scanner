@echo off
title Cyber Scanner PRO - Launcher
echo.
echo ========================================
echo    CYBER SCANNER PRO - LAUNCHER
echo ========================================
echo.

cd /d "%~dp0"

echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

echo Starting Cyber Scanner PRO...
echo.

python main.py

if errorlevel 1 (
    echo.
    echo Error occurred while running the scanner.
    echo Make sure all dependencies are installed:
    echo pip install -r requirements.txt
    echo.
    echo You can also try running: python src\gui\main_window.py
    pause
)
