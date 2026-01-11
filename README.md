# 🕒 RudyTime  
**Privacy First Linux App Usage Tracker**

![License](https://img.shields.io/badge/license-MIT-green.svg)
![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)
![Platform](https://img.shields.io/badge/platform-Linux-important.svg)
![Status](https://img.shields.io/badge/status-stable-success.svg)
![Privacy](https://img.shields.io/badge/privacy-100%25%20local-critical.svg)

**RudyTime** is a lightweight, terminal-based time tracking tool for Linux.  
It shows you exactly **where your time goes** by tracking active applications in real time.

**No cloud.**  
**No tracking.**  
**No bullshit.**

Everything stays **local, offline, and under your control**.

---

## ✨ Features

**✅ Tracks active applications**  
**✅ Ignores idle time**  
**✅ Daily and weekly summaries**  
**✅ Clean terminal output with usage bars**  
**✅ Runs quietly in the background**  
**✅ Per-user installation (PEP 668 safe)**  
**✅ No internet access**  
**✅ No telemetry**  
**✅ Simple and hackable codebase**

---

## 🧠 How It Works

**RudyTime** monitors the currently focused window using Linux X11 tools and records usage time **only when you are active**.

All data is stored **locally in your home directory** and never leaves your machine.

You can inspect, delete, or modify your data **at any time**.

---

## 📁 Project Structure

```
RudyTime/
├── install.sh
├── README.md
├── requirements.txt
├── RudyTime
│ ├── Config.py
│ ├── init.py
│ ├── print_summary.py
│ ├── State.py
│ ├── Storage.py
│ └── Tracker.py
├── RudyTime.py
└── test_seed.py``
```

---

## 📦 Installation

Clone the repository and run the installer:

```bash
git clone https://github.com/RudySilver/RudyTime.git
cd RudyTime
bash install.sh

The installer will automatically:

✔ Install required s```ystem packages
✔ Set up a safe Python environment
✔ Install RudyTime per-user
✔ Make the RudyTime command available globally
🚀 Usage
```
Start tracking

```RudyTime start```

Stop tracking

``RudyTime stop``

Show today’s usage

```RudyTime today```

Show weekly summary

```RudyTime week```

Check status

```RudyTime status```

Delete all stored data

```RudyTime purge```

📊 Example Output
```
╔════════════════════════════════════════════╗
║🕒 RudyTime Daily Summary                   ║
╚════════════════════════════════════════════╝
╔══════════════════╦══════╦══════════════════╗
║App               ║Time  ║Usage Bar         ║
╠══════════════════╬══════╬══════════════════╣
║firefox-esr       ║12 min║██████░░░░░░░░░░░░║
║mate-terminal     ║8 min ║████░░░░░░░░░░░░░░║
╚══════════════════╩══════╩══════════════════╝
```
🔐 Privacy & Security

Your data:

✔ Never leaves your machine
✔ Is never uploaded
✔ Has zero network usage
✔ Lives in readable local files

RudyTime is offline by design.
🧪 Requirements

Linux with X11
Python 3.10 or newer
xdotool
xprintidle

Wayland support may be added later.
🤝 Contributing

Pull requests, issues, and suggestions are welcome!
Help make RudyTime more intuitive, beautiful, and productivity-friendly 😉

How to contribute:

1. Fork the repository
2. Create a feature branch
3. Commit clean, readable code
4. Open a pull request

Check CONTRIBUTING.md for guidelines.
💎 Credits

Made 100% by Rudy Cooper
GitHub: https://github.com/RudySilver
📜 License

*MIT License
*Use it, modify it, share it, but keep building.*
💡 Motivation*

Time is your most valuable asset.
RudyTime helps you see where it goes so you can take control of it 😉

**⭐ Star the repo, fork it, and improve your productivity with us!**
