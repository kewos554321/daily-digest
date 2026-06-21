#!/usr/bin/env python3
"""Tech controller — runs all tech_* sources. Cron: 7:50 AM Taipei"""

import sys, os, traceback
sys.path.insert(0, os.path.dirname(__file__))
import config as cfg

MODULES = [
    ("tech_ai",           "sources.tech_ai"),
    ("tech_google",       "sources.tech_google"),
    ("tech_ai_companies", "sources.tech_ai_companies"),
    ("tech_news",         "sources.tech_news"),
    ("tech_product",    "sources.tech_product"),
    ("tech_dev",        "sources.tech_dev"),
    ("tech_security",   "sources.tech_security"),
    ("tech_devops",     "sources.tech_devops"),
    ("tech_opensource", "sources.tech_opensource"),
    ("tech_career",     "sources.tech_career"),
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
