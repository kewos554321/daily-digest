#!/usr/bin/env python3
"""Immigration AU — r/AusVisa. Cron: 8:45 AM Taipei"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import config as cfg
from sources.lib import call_deepseek, fetch_reddit, write_output, skip

TOPIC   = "immigration_au"
HEADING = "## 🇦🇺 Australia Immigration"


def run():
    print("[immigration_au] Fetching r/AusVisa...")
    posts = fetch_reddit(cfg.AU_SUBREDDIT, limit=cfg.AU_LIMIT, keywords=cfg.AU_KEYWORDS)
    print(f"  {len(posts)} posts")

    if not posts:
        skip(TOPIC, "no relevant posts"); return

    titles  = "\n".join(f"- {p['title']} ({p['url']})" for p in posts)
    summary = call_deepseek(f"""Summarize these Australia visa/immigration Reddit posts for someone planning to migrate from Taiwan.
Focus on skilled migration (189/190/491), processing times, and any policy changes.
3-4 bullets with links. English.

{titles}""", max_tokens=400)

    raw_md = "\n".join(f"- [{p['title']}]({p['url']})" for p in posts)
    write_output(TOPIC, HEADING, summary, raw_md)


if __name__ == "__main__":
    run()
