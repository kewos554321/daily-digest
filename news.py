#!/usr/bin/env python3
"""News controller — runs all news_* sources. Cron: 8:20 AM Taipei"""

import sys, os, traceback
sys.path.insert(0, os.path.dirname(__file__))
import config as cfg

MODULES = [
    ("news_world", "sources.news_world"),
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
