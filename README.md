RudyTime

🕒 RudyTime – Local Time Intelligence Tool for Linux

RudyTime is a simple yet powerful tool to track how you spend your time on your Linux machine. It monitors which applications you use, for how long, and gives you daily & weekly summaries with a stylish, colorful terminal UI.
Built for any Linux user, from beginners to pros, who want insight into their productivity.

Features

📊 Track application usage: Daily & weekly summaries

🎨 Stylish terminal UI: Colored tables, usage bars, emojis

⚡ Fast & local: Everything runs offline, nothing is sent

🛠️ Easy to install: One script installs everything and makes it runnable globally

🖥️ Works everywhere: Start, stop, check status, or view reports from anywhere in your terminal

🧹 Data management: Purge old usage data anytime

Installation

Clone the repository:

git clone https://github.com/RudySilver/RudyTime
cd RudyTime


Run the installer:

bash install.sh


This will:

Copy the RudyTime Python package to ~/.local/lib

Copy the main executable RudyTime.py to ~/.local/bin/RudyTime

Set up your PYTHONPATH so the package works globally

Check for required dependencies (xdotool, xprintidle) and install them if missing

After installation, you can start tracking your time with:

RudyTime start

Usage
RudyTime start      # Start tracking
RudyTime stop       # Stop tracking
RudyTime status     # Check tracker status
RudyTime today      # Show today's summary
RudyTime week       # Show weekly summary
RudyTime purge      # Delete all stored usage data
RudyTime --version  # Show RudyTime version


Example Output – Daily Summary:

╔═════════════════════════════════════════════╗
║   🕒 RudyTime Daily Summary (2026-01-01)    ║
╚═════════════════════════════════════════════╝
╔════════════════════╦══════╦════════════════════╗
║ App                ║ Time ║ Usage Bar          ║
╠════════════════════╬══════╬════════════════════╣
║ mate-terminal 💻   ║ 4 min ║ ███░░░░░░░░░░░░░░ ║
║ firefox-esr 🌐     ║12 min ║ ██████████░░░░░░░ ║
║ caja 📂            ║ 0 min ║ ░░░░░░░░░░░░░░░░░ ║
╚════════════════════╩═══════╩═══════════════════╝


All data is stored locally in:
~/.local/share/rudytime
Nothing is sent anywhere. Your privacy is protected.

Requirements

Python 3.8+

Linux-based system (Parrot OS, Ubuntu, Debian, Kali, etc.)

Optional but recommended: xdotool and xprintidle (for active window tracking and idle detection)

The installer will automatically check/install them.

Directory Structure
RudyTime/
│
├── RudyTime.py              # Main executable
├── install.sh               # Installer script
├── README.md                # This file
├── requirements.txt         # Python dependencies
├── RudyTime/                # Python package
│   ├── __init__.py
│   ├── State.py
│   ├── Storage.py
│   └── Tracker.py
│
└── __pycache__/             # Python cache (auto-generated)

Contributing

Pull requests, issues, and suggestions are welcome!
Help us make RudyTime more intuitive, beautiful, and productive-friendly.

Credits

Made 100% by Rudy Cooper (@RudySilver).

License

MIT License – Use it, modify it, share it, but keep building.

Motivation

“Time is your most valuable asset. RudyTime helps you see where it goes so you can take control of it.”

💡 Star ⭐ the repo, fork it, and improve your productivity with us!
