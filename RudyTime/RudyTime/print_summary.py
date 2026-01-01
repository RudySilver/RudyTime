#!/usr/bin/env python3
from math import ceil

try:
    from colorama import Fore, Style
except Exception:
    class _S: RESET_ALL = ""
    class _F: CYAN = GREEN = YELLOW = RED = ""
    Fore = _F(); Style = _S()

BLOCK = "█"
SPARK = ["▁","▂","▃","▄","▅","▆","▇","█"]

def _format_minutes_to_hm(seconds):
    mins = int(round(seconds / 60.0))
    h = mins // 60
    m = mins % 60
    if h:
        return f"{h}h{m:02d}m"
    return f"{m}m"

def _percent_of_day(seconds):
    mins = seconds / 60.0
    return (mins / 1440.0) * 100.0

def _make_bar(seconds, max_seconds, segment_seconds=1800, max_width=40):
    try:
        seconds = int(seconds); max_seconds = int(max_seconds)
    except Exception:
        return ""
    if max_seconds <= 0 or seconds <= 0:
        return ""
    max_segments = max_seconds // segment_seconds
    if max_segments == 0:
        max_segments = 1
    if max_segments > max_width:
        segment_seconds = int(ceil(max_seconds / max_width))
        if segment_seconds <= 0:
            segment_seconds = 1
    segs = int(round(seconds / segment_seconds))
    if segs <= 0:
        segs = 1
    return BLOCK * segs

def _sparkline(values):
    if not values:
        return ""
    mx = max(values)
    if mx == 0:
        return "".join(SPARK[0] for _ in values)
    res = []
    for v in values:
        idx = int((v / mx) * (len(SPARK)-1))
        res.append(SPARK[idx])
    return "".join(res)

def print_daily(day_map, date_str):
    print(Fore.CYAN + f"Usage for {date_str}" + Style.RESET_ALL)
    if not day_map:
        print(Fore.YELLOW + "  No data for this day." + Style.RESET_ALL)
        return
    rows = sorted(day_map.items(), key=lambda x: -int(x[1]) if isinstance(x[1], (int, str)) else 0)
    max_seconds = max(int(s) for _, s in rows) if rows else 0
    print(Style.RESET_ALL + f"{'App':40} | {'Time':>10} | {'%day':>6} | Usage Bar")
    print("-" * 90)
    top = 0
    for app, sec in rows:
        sec = int(sec)
        top += 1
        time_hm = _format_minutes_to_hm(sec)
        pct = _percent_of_day(sec)
        bar = _make_bar(sec, max_seconds)
        emoji = ""
        if top == 1: emoji = " 🔥"
        elif top == 2: emoji = " ⭐"
        elif top == 3: emoji = " ✨"
        print(f"{app[:40]:40} | {time_hm:>10} | {pct:6.1f}% | {Fore.GREEN}{bar}{Style.RESET_ALL}{emoji}")

def print_week(totals):
    print(Fore.CYAN + f"Weekly overview (last {len(totals)} days)" + Style.RESET_ALL)
    if not totals:
        print(Fore.YELLOW + "  No data." + Style.RESET_ALL)
        return
    max_seconds = max(total for _, total in totals) if totals else 0
    print(Style.RESET_ALL + f"{'Date':12} | {'Time':>10} | {'%day':>6} | Usage Bar | Spark")
    print("-" * 100)
    values = [sec for _, sec in totals]
    spark = _sparkline(values)
    for i, (date_str, sec) in enumerate(totals):
        time_hm = _format_minutes_to_hm(sec)
        pct = _percent_of_day(sec)
        bar = _make_bar(sec, max_seconds)
        s = spark[i] if i < len(spark) else ""
        print(f"{date_str:12} | {time_hm:>10} | {pct:6.1f}% | {Fore.GREEN}{bar}{Style.RESET_ALL} | {s}")