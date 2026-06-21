#!/usr/bin/env python3
"""News World — BBC RSS. Cron: 8:20 AM Taipei"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from sources.lib import call_deepseek, fetch_rss, write_output, skip

TOPIC   = "news_world"
HEADING = "## 🌍 World News"


def run():
    print("[news_world] Fetching BBC...")
    items = fetch_rss("https://feeds.bbci.co.uk/news/world/rss.xml", limit=8)
    print(f"  {len(items)} items")

    if not items:
        skip(TOPIC, "no items"); return

    text = "\n".join(f"- {n['title']}: {n['desc']} ({n['url']})" for n in items)
    summary = call_deepseek(f"""Summarize today's top world news in 3-5 bullets with links. English.

{text}""", max_tokens=500)

    raw_md = "\n".join(f"- [{n['title']}]({n['url']})" for n in items)
    write_output(TOPIC, HEADING, summary, raw_md)


if __name__ == "__main__":
    run()
