#!/usr/bin/env python3
import time
import threading
import subprocess
import re
from . import Storage, Config

IDLE_THRESHOLD_MS = 60 * 1000
TICK_SECONDS = 60

def _get_idle_ms():
    conf = Config.load_config()
    thr = int(conf.get("idle_threshold_seconds", 60)) * 1000
    try:
        out = subprocess.check_output(["xprintidle"], stderr=subprocess.DEVNULL)
        return int(out.strip())
    except Exception:
        return 0

def _get_active_window_name():
    candidates = [
        ["xdotool", "getactivewindow", "getwindowname"],
        ["xdotool", "getwindowfocus", "getwindowname"],
        ["xdotool", "getactivewindow", "getwindowclassname"],
    ]
    for cmd in candidates:
        try:
            out = subprocess.check_output(cmd, stderr=subprocess.DEVNULL, timeout=1)
            name = out.decode("utf-8", errors="ignore").strip()
            if name:
                return name
        except Exception:
            continue
    return "Unknown"

def _extract_website_from_title(title):
    # crude heuristic: look for domain-like substrings in window title
    # e.g. "Example Domain - Mozilla Firefox"
    dom = re.search(r"([a-z0-9\-]+\.[a-z]{2,})(/[^ ]*)?", title, re.IGNORECASE)
    if dom:
        return dom.group(1)
    # common patterns " - Google Chrome" with page title first; try parentheses or first token with dot
    tok = title.split(" - ")[0]
    if "." in tok and " " not in tok:
        return tok
    return None

def _get_total_net_bytes():
    # sum rx+tx across all interfaces from /proc/net/dev
    try:
        with open("/proc/net/dev", "r") as f:
            lines = f.readlines()[2:]
        total = 0
        for line in lines:
            parts = line.split()
            if len(parts) >= 17:
                rx = int(parts[1])
                tx = int(parts[9])
                total += rx + tx
        return total
    except Exception:
        return 0

class Tracker:
    def __init__(self):
        self._stop_event = threading.Event()
        self._thread = None

    def run_loop(self):
        last_net = _get_total_net_bytes()
        while True:
            try:
                idle = _get_idle_ms()
                conf = Config.load_config()
                thr_ms = int(conf.get("idle_threshold_seconds", 60)) * 1000
                if idle < thr_ms:
                    name = _get_active_window_name()
                    # check ignore list
                    ignore = conf.get("ignore_list", [])
                    skip = False
                    for ig in ignore:
                        if ig and ig.lower() in name.lower():
                            skip = True
                            break
                    if not skip:
                        # website extraction
                        site = _extract_website_from_title(name)
                        if site:
                            app_label = f"{name} [{site}]"
                        else:
                            app_label = name
                        # track network delta
                        now_net = _get_total_net_bytes()
                        net_delta = max(0, now_net - last_net)
                        if net_delta > 0:
                            Storage.add_network_usage(net_delta)
                        last_net = now_net
                        Storage.add_usage_for_now(app_label, TICK_SECONDS)
                time.sleep(TICK_SECONDS)
            except KeyboardInterrupt:
                break
            except Exception:
                time.sleep(TICK_SECONDS)
                continue

    def start_background(self):
        if self._thread and self._thread.is_alive():
            return
        self._stop_event.clear()
        self._thread = threading.Thread(target=self.run_loop, daemon=True)
        self._thread.start()

    def stop(self):
        self._stop_event.set()
        if self._thread:
            self._thread.join(timeout=1)