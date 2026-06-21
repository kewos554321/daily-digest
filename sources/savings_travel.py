#!/usr/bin/env python3
"""Savings Travel — Reddit solotravel tips & deals. Cron: 8:30 AM Taipei"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import config as cfg
from sources.lib import call_deepseek, fetch_reddit, write_output, skip

TOPIC   = "savings_travel"
HEADING = "## 🗺️ Travel Deals"


def run():
    print("[savings_travel] Fetching Reddit...")
    posts = fetch_reddit(cfg.TRAVEL_SUBREDDIT, limit=6, keywords=cfg.TRAVEL_KEYWORDS)
    print(f"  Reddit: {len(posts)} posts")

    if not posts:
        skip(TOPIC, "no relevant posts"); return

    titles = "\n".join(f"- {p['title']} ({p['url']})" for p in posts)
    summary = call_deepseek(f"""Summarize these travel posts for a Taiwanese traveler looking for deals and tips.
Focus on practical info: visa, cost, seasonal tips. 3-5 bullets with links. English.

{titles}""", max_tokens=400)

    raw_md = f"### r/{cfg.TRAVEL_SUBREDDIT}\n" + "\n".join(
        f"- [{p['title']}]({p['url']})" for p in posts
    )
    write_output(TOPIC, HEADING, summary, raw_md)


if __name__ == "__main__":
    run()
