# RudyTime/Tracker.py

import subprocess
import time
from RudyTime.Storage import save_data

IDLE_THRESHOLD = 60  # in seconds, ignore activity below this idle time

def get_idle_time():
    """Return idle time in seconds using xprintidle."""
    try:
        idle_ms = int(subprocess.check_output(["xprintidle"]).decode().strip())
        return idle_ms / 1000.0
    except Exception:
        return 0

def get_active_window_name():
    """Return the currently active window's application name."""
    try:
        window_id = subprocess.check_output(["xdotool", "getactivewindow"]).decode().strip()
        pid = subprocess.check_output(["xdotool", "getwindowpid", window_id]).decode().strip()
        # Get process name
        proc_name = subprocess.check_output(["ps", "-p", pid, "-o", "comm="]).decode().strip()
        return proc_name
    except Exception:
        return None

def track_app_usage(data_dir):
    """Track usage for the active window, update today's data."""
    idle_time = get_idle_time()
    if idle_time > IDLE_THRESHOLD:
        # User is idle, don't count
        return

    app_name = get_active_window_name()
    if not app_name:
        return

    # Increment usage by 1 minute
    save_data(app_name, 1)

