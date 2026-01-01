#!/usr/bin/env python3
import json
import os
import tempfile
from pathlib import Path
from datetime import datetime, timedelta

DATA_DIR = os.path.expanduser("~/.local/share/rudytime")
DATA_FILE = os.path.join(DATA_DIR, "data.json")
PID_FILE = os.path.join(DATA_DIR, "rudytime.pid")

def get_data_dir():
    return Path(DATA_DIR)

def get_data_file_path():
    return DATA_FILE

def get_pidfile_path():
    return PID_FILE

def today_str(dt=None):
    if dt is None:
        from datetime import datetime as _dt
        dt = _dt.now()
    return dt.strftime("%Y-%m-%d")

def _ensure_data_dir():
    Path(DATA_DIR).mkdir(parents=True, exist_ok=True)

def get_data():
    _ensure_data_dir()
    if not os.path.exists(DATA_FILE):
        return {"days": {}}
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if not isinstance(data, dict):
                return {"days": {}}
            if "days" not in data or not isinstance(data["days"], dict):
                data["days"] = {}
            return data
    except Exception:
        return {"days": {}}

def _atomic_write(path, data):
    _ensure_data_dir()
    fd, tmp = tempfile.mkstemp(dir=DATA_DIR, prefix="tmp-")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        os.replace(tmp, path)
    except Exception:
        try:
            os.remove(tmp)
        except Exception:
            pass
        raise

def save_data(data):
    _ensure_data_dir()
    _atomic_write(DATA_FILE, data)

def add_usage_for_now(app_name, seconds):
    if not app_name:
        app_name = "Unknown"
    data = get_data()
    days = data.setdefault("days", {})
    today = today_str()
    day = days.setdefault(today, {})

    existing = day.get(app_name, 0)
    if isinstance(existing, dict):
        s = 0
        for v in existing.values():
            try:
                s += int(v)
            except Exception:
                continue
        existing = s
    try:
        existing = int(existing)
    except Exception:
        existing = 0

    day[app_name] = existing + int(seconds)
    days[today] = day
    data["days"] = days
    try:
        save_data(data)
    except Exception:
        pass

def add_network_usage(bytes_count):
    data = get_data()
    days = data.setdefault("days", {})
    today = today_str()
    day = days.setdefault(today, {})
    existing = day.get("_network_bytes", 0)
    try:
        existing = int(existing)
    except Exception:
        existing = 0
    day["_network_bytes"] = existing + int(bytes_count)
    days[today] = day
    data["days"] = days
    try:
        save_data(data)
    except Exception:
        pass

def get_last_n_days_totals(n_days, data=None):
    if data is None:
        data = get_data()
    days_map = data.get("days", {})
    result = []
    today = datetime.now().date()
    for i in range(n_days - 1, -1, -1):
        d = today - timedelta(days=i)
        key = d.strftime("%Y-%m-%d")
        day_data = days_map.get(key, {})
        total = 0
        if isinstance(day_data, dict):
            for v in day_data.values():
                try:
                    if isinstance(v, dict):
                        for vv in v.values():
                            total += int(vv)
                    else:
                        # exclude special keys from app totals
                        total += int(v) if not isinstance(v, str) else 0
                except Exception:
                    continue
        result.append((key, total))
    return result

def export_json(path):
    data = get_data()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def import_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, dict):
                save_data(data)
                return True
    except Exception:
        pass
    return False