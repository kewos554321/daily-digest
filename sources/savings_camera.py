#!/usr/bin/env python3
"""Savings Camera — camera gear deals + photography tips. Cron: 8:40 AM Taipei"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from datetime import datetime
import config as cfg
from sources.lib import call_deepseek, fetch_reddit, write_output, skip

TOPIC   = "savings_camera"
HEADING = "## 📷 Camera Deals"


def run():
    print("[savings_camera] Fetching...")
    date_str = datetime.now(cfg.TZ).strftime("%Y-%m-%d")
    month    = datetime.now(cfg.TZ).strftime("%B")

    posts = fetch_reddit("photomarket", limit=5, keywords=None)
    print(f"  r/photomarket: {len(posts)}")

    ai_tips = call_deepseek(f"""You are a photography expert and deals advisor for Taiwan consumers. Today is {date_str} ({month}).

【購買優惠】
- Best places to buy camera gear in Taiwan (PChome, momo, 光華商場, 日本代購, 二手)
- Any seasonal sale tips for {month}

【今日攝影技巧】
- One practical photography tip (composition, lighting, or camera setting)
- Give a concrete practice exercise

Specific and actionable. Traditional Chinese or English OK.""",
        max_tokens=500, temperature=0.4)

    posts_md = "\n".join(f"- [{p['title']}]({p['url']})" for p in posts) or "_No posts today_"
    summary  = ai_tips
    if posts:
        summary += "\n\nReddit:\n" + "\n".join(p["title"] for p in posts)

    raw_md = f"### AI Tips\n{ai_tips}\n\n### r/photomarket\n{posts_md}"
    write_output(TOPIC, HEADING, summary, raw_md)


if __name__ == "__main__":
    run()
