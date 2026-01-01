```markdown
# RudyTime

Privacy-first, terminal-based time tracker for Linux. Tracks active window every minute using xdotool and idle via xprintidle. All data stored locally in JSON at `$HOME/.local/share/rudytime`.

Install (per-user):
1. Run from project root (as your normal user):
   bash install.sh

2. Ensure new PATH for current session:
   export PATH="$HOME/.local/bin:$PATH"

3. Start tracker:
   RudyTime start

Commands:
- RudyTime start
- RudyTime stop
- RudyTime status
- RudyTime today
- RudyTime week
- RudyTime purge

Testing (without running tracker):
- python3 test_seed.py
- RudyTime today
- RudyTime week

Notes:
- Installer will prompt to auto-install system packages (uses sudo when needed).
- If automatic pip install of colorama fails, install manually inside the venv:
  source "$HOME/.rudytime_venv/bin/activate" && pip install colorama
- The tool is robust to missing colorama and to nested dicts in storage.
```