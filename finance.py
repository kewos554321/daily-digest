#!/usr/bin/env python3
"""Finance controller — runs all finance_* sources. Cron: 8:00 AM Taipei"""

import sys, os, traceback
sys.path.insert(0, os.path.dirname(__file__))
import config as cfg

MODULES = [
    ("finance_markets",    "sources.finance_markets"),
    ("finance_stock",      "sources.finance_stock"),
    ("finance_screener",   "sources.finance_screener"),
    ("finance_realestate", "sources.finance_realestate"),
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
