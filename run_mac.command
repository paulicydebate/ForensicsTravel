#!/bin/bash
# Double-click this file (or right-click > Open, the first time) to launch
# the Travel Packet Builder on macOS. It sets up a virtual environment the
# first time it runs (takes a minute or two), then every run after that is
# fast.
set -e
cd "$(dirname "$0")"

if ! command -v python3 &> /dev/null; then
    echo "Python 3 isn't installed."
    echo "Download it from https://www.python.org/downloads/ and run this again."
    read -p "Press Enter to close this window..."
    exit 1
fi

if [ ! -d "venv" ]; then
    echo "First run — setting up, this takes a minute or two..."
    python3 -m venv venv
fi

source venv/bin/activate
pip install -q -r requirements.txt

echo "Starting Travel Packet Builder — your browser will open shortly..."
echo "(Leave this window open while you use the app. Close it, or press Ctrl+C, when you're done.)"
streamlit run app.py

echo
read -p "Press Enter to close this window..."
