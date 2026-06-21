#!/usr/bin/env python3
"""Learning controller — runs all learning_* sources. Cron: 8:40 AM Taipei"""

import sys, os, traceback
sys.path.insert(0, os.path.dirname(__file__))
import config as cfg

MODULES = [
    ("learning_finance",     "sources.learning_finance"),
    ("learning_leetcode",    "sources.learning_leetcode"),
    ("learning_tech",        "sources.learning_tech"),
    ("learning_photography", "sources.learning_photography"),
    ("learning_youtube",     "sources.learning_youtube"),
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
