#!/usr/bin/env python3
"""
Seed example data for quick testing of 'today' and 'week' outputs.
"""
import json
import os
from datetime import datetime, timedelta

DATA_DIR = os.path.expanduser("~/.local/share/rudytime")
DATA_FILE = os.path.join(DATA_DIR, "data.json")

def seed():
    os.makedirs(DATA_DIR, exist_ok=True)
    days = {}
    today = datetime.now().date()
    for i in range(7):
        d = today - timedelta(days=i)
        k = d.strftime("%Y-%m-%d")
        days[k] = {
            "Firefox": (i + 1) * 60 * 10,
            "Terminal": (7 - i) * 60 * 5,
            "Code": (i % 2) * 60 * 15,
        }
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump({"days": days}, f, indent=2)
    print("Seeded example data to", DATA_FILE)

if __name__ == "__main__":
    seed()