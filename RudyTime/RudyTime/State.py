# RudyTime/State.py

import os
import sys
import signal
import json
import time
from RudyTime.Storage import load_today, load_week, save_data
from RudyTime.Tracker import track_app_usage
from RudyTime.print_summary import print_summary

PID_FILE = os.path.expanduser("~/.local/share/rudytime/rudytime.pid")
DATA_DIR = os.path.expanduser("~/.local/share/rudytime")

def ensure_data_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def start_tracker():
    ensure_data_dir()
    if os.path.exists(PID_FILE):
        print("RudyTime is already running.")
        return

    pid = os.fork()
    if pid > 0:
        # Parent process: save PID and exit
        with open(PID_FILE, "w") as f:
            f.write(str(pid))
        print(f"RudyTime started. PID: {pid}")
        return

    # Child process: start tracking
    try:
        while True:
            track_app_usage(DATA_DIR)
            time.sleep(60)  # Track every 1 minute
    except KeyboardInterrupt:
        pass

def stop_tracker():
    if not os.path.exists(PID_FILE):
        print("RudyTime is not running.")
        return
    with open(PID_FILE) as f:
        pid = int(f.read())
    try:
        os.kill(pid, signal.SIGTERM)
        print("RudyTime stopped.")
    except ProcessLookupError:
        print("RudyTime process not found.")
    os.remove(PID_FILE)

def status_tracker():
    if os.path.exists(PID_FILE):
        with open(PID_FILE) as f:
            pid = f.read()
        print(f"RudyTime status: running (pid {pid})")
    else:
        print("RudyTime status: not running.")
    print(f"Data directory: {DATA_DIR}")
    print("Network access: none")

def show_today(data=None):
    if data is None:
        data = load_today()
    print_summary(f"🕒 RudyTime Daily Summary ({time.strftime('%Y-%m-%d')})", data)

def show_week(week_data=None):
    if week_data is None:
        week_data = load_week()
    print_summary("🕒 RudyTime Weekly Summary", week_data)

def purge_data():
    ensure_data_dir()
    for file in os.listdir(DATA_DIR):
        path = os.path.join(DATA_DIR, file)
        if os.path.isfile(path):
            os.remove(path)
    print("RudyTime data purged.")

