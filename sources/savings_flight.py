#!/usr/bin/env python3
"""Savings Flight — AI flight booking tips from Taiwan. Cron: 8:35 AM Taipei"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from datetime import datetime
import config as cfg
from sources.lib import call_deepseek, write_output

TOPIC   = "savings_flight"
HEADING = "## ✈️ Flight Tips"


def run():
    print("[savings_flight] Generating flight tips...")
    month    = datetime.now(cfg.TZ).strftime("%B")
    date_str = datetime.now(cfg.TZ).strftime("%Y-%m-%d")
    dest_list = "\n".join(f"- {d}" for d in cfg.TRAVEL_DESTINATIONS)

    tips = call_deepseek(f"""You are a flight deals expert. Today is {date_str} ({month}).
Practical flight booking tips departing from Taiwan (TPE/TSA) to:
{dest_list}

For each destination:
- Peak/off-peak status for {month}
- Best booking window (how many weeks in advance)
- Cheapest airline or route tip
- Any current deals or seasonal promotions to watch

2-3 lines per destination. Be specific and actionable.""",
        max_tokens=700, temperature=0.4)

    raw_md = f"### AI Flight Tips — {month}\n{tips}"
    write_output(TOPIC, HEADING, tips, raw_md)


if __name__ == "__main__":
    run()
