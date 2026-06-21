#!/usr/bin/env python3
"""Tech News — tech industry news (HN, TechCrunch, Wired). Cron: TBD"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from sources.lib import call_deepseek, fetch_rss, write_output, skip

TOPIC   = "tech_news"
HEADING = "## 📱 Tech News"

SOURCES = [
    ("https://feeds.feedburner.com/TechCrunch", "TechCrunch", 5),
    ("https://www.wired.com/feed/rss",          "Wired",       5),
]


def run():
    print("[tech_news] Fetching...")
    all_items = []
    raw_parts = []

    for url, label, limit in SOURCES:
        items = fetch_rss(url, limit=limit)
        print(f"  {label}: {len(items)}")
        all_items.extend(items)
        md = "\n".join(f"- [{n['title']}]({n['url']})" for n in items) or "_No items_"
        raw_parts.append(f"### {label}\n{md}")

    if not all_items:
        skip(TOPIC, "no items"); return

    text = "\n".join(f"- {n['title']}: {n['desc']} ({n['url']})" for n in all_items)
    summary = call_deepseek(f"""Summarize today's top tech industry news for a software engineer.
Focus on product launches, company strategy, and industry shifts.
3-5 bullets with links. English.

{text}""", max_tokens=500)

    write_output(TOPIC, HEADING, summary, "\n\n".join(raw_parts))


if __name__ == "__main__":
    run()
