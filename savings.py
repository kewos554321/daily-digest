#!/usr/bin/env python3
"""Savings controller — runs all savings_* sources. Cron: 8:30 AM Taipei"""

import sys, os, traceback
sys.path.insert(0, os.path.dirname(__file__))
import config as cfg

MODULES = [
    ("savings_travel", "sources.savings_travel"),
    ("savings_flight", "sources.savings_flight"),
    ("savings_camera", "sources.savings_camera"),
    ("savings_dive",   "sources.savings_dive"),
]


def main():
    for topic, module_path in MODULES:
        if not cfg.SECTIONS.get(topic, False):
            print(f"[{topic}] skipped (disabled)")
            continue
        try:
            import importlib
            mod = importlib.import_module(module_path)
            mod.run()
        except Exception:
            print(f"[{topic}] ERROR:")
            traceback.print_exc()


if __name__ == "__main__":
    main()
