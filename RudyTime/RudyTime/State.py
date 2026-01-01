#!/usr/bin/env python3
import os
import sys
import subprocess
import time
from pathlib import Path
from . import Storage, Tracker, print_summary, Config

try:
    from colorama import init as colorama_init, Fore, Style
    colorama_init(autoreset=True)
except Exception:
    class _F: CYAN=GREEN=YELLOW=RED=""; 
    class _S: RESET_ALL=""
    Fore=_F(); Style=_S()

PIDFILE = Storage.get_pidfile_path()

def _is_pid_running(pid):
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    return True

def start():
    pidf = Path(PIDFILE)
    if pidf.exists():
        try:
            pid = int(pidf.read_text().strip())
            if _is_pid_running(pid):
                print(Fore.YELLOW + f"RudyTime is already running (pid {pid})." + Style.RESET_ALL)
                return
            else:
                pidf.unlink(missing_ok=True)
        except Exception:
            pidf.unlink(missing_ok=True)
    exe = sys.executable
    cli_path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "RudyTime.py")
    try:
        proc = subprocess.Popen([exe, cli_path, "--run-daemon"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL, close_fds=True)
        # give it a moment
        time.sleep(0.2)
        print(Fore.GREEN + "RudyTime started." + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"Failed to start RudyTime: {e}" + Style.RESET_ALL)

def stop():
    pidf = Path(PIDFILE)
    if not pidf.exists():
        print(Fore.YELLOW + "RudyTime is not running." + Style.RESET_ALL)
        return
    try:
        pid = int(pidf.read_text().strip())
    except Exception:
        pidf.unlink(missing_ok=True)
        print(Fore.YELLOW + "Removed stale pidfile." + Style.RESET_ALL)
        return
    try:
        os.kill(pid, 15)
        for _ in range(20):
            if not _is_pid_running(pid):
                break
            time.sleep(0.1)
        pidf.unlink(missing_ok=True)
        print(Fore.GREEN + "RudyTime stopped." + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"Failed to stop RudyTime: {e}" + Style.RESET_ALL)

def status():
    pidf = Path(PIDFILE)
    running = False
    pid = None
    if pidf.exists():
        try:
            pid = int(pidf.read_text().strip())
            if _is_pid_running(pid):
                running = True
        except Exception:
            pass
    data_dir = Storage.get_data_dir()
    print(Fore.CYAN + "RudyTime status:" + Style.RESET_ALL)
    print("  Running: " + (Fore.GREEN + f"yes (pid {pid})" + Style.RESET_ALL if running else Fore.YELLOW + "no" + Style.RESET_ALL))
    print("  Data path: " + Fore.CYAN + str(data_dir) + Style.RESET_ALL)
    conf = Config.load_config()
    print("  Idle threshold: " + Fore.CYAN + f"{conf.get('idle_threshold_seconds', 60)}s" + Style.RESET_ALL)
    print("  Network: " + Fore.CYAN + "none (privacy-first)" + Style.RESET_ALL)

def today():
    data = Storage.get_data()
    today_str = Storage.today_str()
    day_data = data.get("days", {}).get(today_str, {})
    # exclude special keys from daily app list
    cleaned = {}
    for app, val in day_data.items():
        if app == "_network_bytes":
            continue
        if isinstance(val, dict):
            s = 0
            for v in val.values():
                try:
                    s += int(v)
                except Exception:
                    continue
            cleaned[app] = s
        else:
            try:
                cleaned[app] = int(val)
            except Exception:
                cleaned[app] = 0
    # add network usage info as a pseudo-app
    net = day_data.get("_network_bytes", 0)
    if net:
        # bytes -> human approximate
        mb = net / (1024*1024)
        cleaned["_network_bytes"] = int(net)
        # present in printout as separate info below
    print_summary.print_daily(cleaned, today_str)
    if net:
        print(Fore.CYAN + f"\nNetwork usage today: {mb:.2f} MB (approx)" + Style.RESET_ALL)

def week():
    data = Storage.get_data()
    totals = Storage.get_last_n_days_totals(7, data)
    print_summary.print_week(totals)

def purge():
    path = Storage.get_data_file_path()
    try:
        answer = input(Fore.RED + "This will delete all RudyTime data. Type 'yes' to confirm: " + Style.RESET_ALL)
    except KeyboardInterrupt:
        print("\nAborted.")
        return
    if answer.strip().lower() == "yes":
        try:
            if os.path.exists(path):
                os.remove(path)
            print(Fore.GREEN + "All RudyTime data removed." + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f"Failed to purge data: {e}" + Style.RESET_ALL)
    else:
        print("Aborted.")

def export(path=None):
    if not path:
        path = os.path.expanduser("~/rudytime-export.json")
    try:
        Storage.export_json(path)
        print(Fore.GREEN + f"Exported data to {path}" + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"Export failed: {e}" + Style.RESET_ALL)

def import_data(path):
    if not path:
        print(Fore.YELLOW + "Usage: RudyTime import /path/to/file.json" + Style.RESET_ALL)
        return
    ok = Storage.import_json(path)
    if ok:
        print(Fore.GREEN + "Import successful." + Style.RESET_ALL)
    else:
        print(Fore.RED + "Import failed; file invalid." + Style.RESET_ALL)

def edit_config():
    cfg = Config.load_config()
    cfg_path = os.path.expanduser("~/.config/rudytime/config.json")
    editor = os.environ.get("EDITOR", "nano")
    print(Fore.CYAN + f"Opening config in {editor}: {cfg_path}" + Style.RESET_ALL)
    # ensure config saved
    Config.save_config(cfg)
    try:
        subprocess.call([editor, cfg_path])
    except Exception as e:
        print(Fore.RED + f"Failed to open editor: {e}" + Style.RESET_ALL)

def seed_example():
    # convenience wrapper for test_seed.py functionality
    from . import Storage as _S
    from datetime import datetime, timedelta
    DATA_DIR = _S.get_data_dir()
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    today = datetime.now().date()
    days = {}
    for i in range(7):
        d = today - timedelta(days=i)
        k = d.strftime("%Y-%m-%d")
        days[k] = {
            "Firefox": (i + 1) * 60 * 10,
            "Terminal": (7 - i) * 60 * 5,
            "Code": (i % 2) * 60 * 15,
        }
    _S.save_data({"days": days})
    print(Fore.GREEN + "Seeded example data." + Style.RESET_ALL)

def _run_daemon_foreground():
    pidfile = Path(PIDFILE)
    try:
        pidfile.parent.mkdir(parents=True, exist_ok=True)
        pidfile.write_text(str(os.getpid()))
    except Exception:
        pass
    def _cleanup(signum, frame):
        try:
            pidfile.unlink(missing_ok=True)
        except Exception:
            pass
        sys.exit(0)
    import signal
    signal.signal(signal.SIGTERM, _cleanup)
    signal.signal(signal.SIGINT, _cleanup)
    tracker = Tracker.Tracker()
    try:
        tracker.run_loop()
    except Exception as e:
        print(f"[RudyTime daemon] fatal error: {e}")
    finally:
        try:
            pidfile.unlink(missing_ok=True)
        except Exception:
            pass