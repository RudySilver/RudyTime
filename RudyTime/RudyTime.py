#!/usr/bin/env python3
import argparse
import os
import sys

# allow running in-place
here = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, here)

from RudyTime import State

def main():
    parser = argparse.ArgumentParser(prog="RudyTime", description="RudyTime - simple local time tracker")
    parser.add_argument("command", nargs="?", default="status",
                        choices=["start", "stop", "status", "today", "week", "purge", "export", "import", "config", "seed"],
                        help="Command")
    parser.add_argument("path", nargs="?", help="Path for import/export")
    parser.add_argument("--run-daemon", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()

    try:
        if args.run_daemon:
            State._run_daemon_foreground()
            return

        cmd = args.command
        if cmd == "start":
            State.start()
        elif cmd == "stop":
            State.stop()
        elif cmd == "status":
            State.status()
        elif cmd == "today":
            State.today()
        elif cmd == "week":
            State.week()
        elif cmd == "purge":
            State.purge()
        elif cmd == "export":
            State.export(args.path)
        elif cmd == "import":
            State.import_data(args.path)
        elif cmd == "config":
            State.edit_config()
        elif cmd == "seed":
            State.seed_example()
    except Exception as e:
        print(f"[RudyTime] Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()