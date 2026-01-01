# RudyTime/__init__.py

# Expose main functions from State.py
from .State import (
    start_tracker,
    stop_tracker,
    status_tracker,
    show_today,
    show_week,
    purge_data
)

# Expose storage helpers
from .Storage import (
    load_today,
    load_week
)

# Expose tracking helpers
from .Tracker import (
    track_app_usage
)

