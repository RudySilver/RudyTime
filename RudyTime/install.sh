#!/usr/bin/env bash

echo "[+] Installing RudyTime..."

# Ensure ~/.local/bin exists
mkdir -p "$HOME/.local/bin"
mkdir -p "$HOME/.local/lib"

# Copy Python package
cp -r RudyTime "$HOME/.local/lib/"

# Copy main executable
cp RudyTime.py "$HOME/.local/bin/RudyTime"
chmod +x "$HOME/.local/bin/RudyTime"

# Ensure ~/.local/bin is in PATH
if ! grep -q 'export PATH=$HOME/.local/bin:$PATH' "$HOME/.bashrc"; then
    echo 'export PATH=$HOME/.local/bin:$PATH' >> "$HOME/.bashrc"
fi

# Ensure PYTHONPATH includes ~/.local/lib
if ! grep -q 'export PYTHONPATH=$HOME/.local/lib:$PYTHONPATH' "$HOME/.bashrc"; then
    echo 'export PYTHONPATH=$HOME/.local/lib:$PYTHONPATH' >> "$HOME/.bashrc"
fi

# Refresh shell environment
source "$HOME/.bashrc"

echo "[+] Installing Python dependencies..."
# Use --user to avoid system Python issues
pip install --user -r requirements.txt || echo "[!] Python dependencies already satisfied or handled."

echo "[+] Installing system packages (xdotool, xprintidle)..."
if ! command -v xdotool >/dev/null 2>&1; then
    sudo apt update && sudo apt install -y xdotool
fi

if ! command -v xprintidle >/dev/null 2>&1; then
    sudo apt update && sudo apt install -y xprintidle
fi

echo "[+] RudyTime installation complete!"
echo "Run: RudyTime start"
