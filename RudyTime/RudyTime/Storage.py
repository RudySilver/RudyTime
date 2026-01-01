# RudyTime/Storage.py

import os
import json
import time

DATA_DIR = os.path.expanduser("~/.local/share/rudytime")

def ensure_data_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def get_today_file():
    ensure_data_dir()
    return os.path.join(DATA_DIR, f"{time.strftime('%Y-%m-%d')}.json")

def load_today():
    """Load today's usage data."""
    today_file = get_today_file()
    if os.path.exists(today_file):
        with open(today_file, "r") as f:
            return json.load(f)
    return {}

def save_today(data):
    """Save today's usage data."""
    today_file = get_today_file()
    with open(today_file, "w") as f:
        json.dump(data, f, indent=2)

def load_week():
    """Load the last 7 days usage data."""
    ensure_data_dir()
    week_data = {}
    for i in range(7):
        day_file = os.path.join(DATA_DIR, f"{time.strftime('%Y-%m-%d', time.localtime(time.time() - i*86400))}.json")
        if os.path.exists(day_file):
            with open(day_file, "r") as f:
                day_data = json.load(f)
                week_data[time.strftime('%Y-%m-%d', time.localtime(time.time() - i*86400))] = day_data
    return week_data

def save_data(app_name, minutes):
    """Update usage for an app today."""
    data = load_today()
    if app_name in data:
        data[app_name] += minutes
    else:
        data[app_name] = minutes
    save_today(data)

