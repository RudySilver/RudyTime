#!/usr/bin/env python3
import json
import os
import tempfile
from pathlib import Path

CONFIG_DIR = os.path.expanduser("~/.config/rudytime")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")

DEFAULT = {
    "idle_threshold_seconds": 60,
    "ignore_list": [
        "Desktop", "Lock", "sddm", "LightDM"
    ],
    "tags": {}  # app_name -> ["work","browser"]
}

def _ensure_dir():
    Path(CONFIG_DIR).mkdir(parents=True, exist_ok=True)

def load_config():
    _ensure_dir()
    if not os.path.exists(CONFIG_FILE):
        save_config(DEFAULT)
        return dict(DEFAULT)
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if not isinstance(data, dict):
                data = dict(DEFAULT)
            # ensure keys
            for k, v in DEFAULT.items():
                if k not in data:
                    data[k] = v
            return data
    except Exception:
        return dict(DEFAULT)

def _atomic_write(path, data):
    _ensure_dir()
    fd, tmp = tempfile.mkstemp(dir=CONFIG_DIR, prefix="tmp-")
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

def save_config(data):
    _atomic_write(CONFIG_FILE, data)