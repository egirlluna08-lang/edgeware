#!/bin/bash

echo "Checking for Python..."
if ! command -v python3 &> /dev/null; then
    echo "Python3 not found! Please install Python 3.7+"
    exit 1
fi

echo "Installing Pillow..."
pip3 install Pillow --quiet

echo ""
echo "Starting edgeware..."
echo ""
python3 edgeware.py
