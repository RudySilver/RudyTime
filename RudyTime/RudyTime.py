#!/usr/bin/env python3
import sys
from RudyTime.State import start_tracker, stop_tracker, status_tracker, show_today, show_week, purge_data
from RudyTime.Storage import load_today, load_week

def main():
    args = sys.argv[1:]

    if not args:
        print("RudyTime - Local time intelligence tool")
        print("Usage: RudyTime {start|stop|status|today|week|purge|--version}")
        sys.exit()

    command = args[0].lower()

    if command == 'start':
        start_tracker()
    elif command == 'stop':
        stop_tracker()
    elif command == 'status':
        status_tracker()
    elif command == 'today':
        data = load_today()
        show_today(data)
    elif command == 'week':
        week_data = load_week()
        show_week(week_data)
    elif command == 'purge':
        purge_data()
    elif command == '--version':
        print("RudyTime v0.2")
    else:
        print(f"Unknown command: {command}")
        print("Usage: RudyTime {start|stop|status|today|week|purge|--version}")

if __name__ == "__main__":
    main()

