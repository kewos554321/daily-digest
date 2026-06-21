#!/usr/bin/env python3
"""Savings Dive — diving gear deals. Cron: 8:42 AM Taipei"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from datetime import datetime
import config as cfg
from sources.lib import call_deepseek, fetch_reddit, write_output, skip

TOPIC   = "savings_dive"
HEADING = "## 🤿 Dive Gear Deals"

DIVE_KEYWORDS = ["deal", "sale", "discount", "buy", "sell", "gear", "equipment", "wetsuit", "bcd", "regulator"]


def run():
    print("[savings_dive] Fetching...")
    date_str = datetime.now(cfg.TZ).strftime("%Y-%m-%d")
    month    = datetime.now(cfg.TZ).strftime("%B")

    posts = fetch_reddit("scuba", limit=5, keywords=DIVE_KEYWORDS)
    print(f"  r/scuba: {len(posts)}")

    ai_tips = call_deepseek(f"""You are a diving gear expert for Taiwan consumers. Today is {date_str} ({month}).

【購買優惠】
- Best places to buy diving equipment in Taiwan (潛水用品店, online, Facebook社團)
- Any {month} seasonal sale tips or diving season notes for Taiwan/Asia

【裝備建議】
- One practical gear tip or maintenance advice for recreational divers

Specific and actionable. Traditional Chinese or English OK.""",
        max_tokens=400, temperature=0.4)

    posts_md = "\n".join(f"- [{p['title']}]({p['url']})" for p in posts) or "_No posts today_"
    summary  = ai_tips
    if posts:
        summary += "\n\nReddit:\n" + "\n".join(p["title"] for p in posts)

    raw_md = f"### AI Tips\n{ai_tips}\n\n### r/scuba\n{posts_md}"
    write_output(TOPIC, HEADING, summary, raw_md)


if __name__ == "__main__":
    run()
