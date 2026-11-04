@echo off
rem Double-click this file to launch the Travel Packet Builder on Windows.
rem It sets up a virtual environment the first time it runs (takes a minute
rem or two), then every run after that is fast.
cd /d "%~dp0"

where python >nul 2>nul
if errorlevel 1 (
    echo Python isn't installed.
    echo Download it from https://www.python.org/downloads/ and run this again.
    echo IMPORTANT: on the Python installer's first screen, check "Add python.exe to PATH".
    pause
    exit /b 1
)

if not exist venv (
    echo First run -- setting up, this takes a minute or two...
    python -m venv venv
)

call venv\Scripts\activate.bat
pip install -q -r requirements.txt

echo Starting Travel Packet Builder -- your browser will open shortly...
echo (Leave this window open while you use the app. Close it when you're done.)
streamlit run app.py

pause
