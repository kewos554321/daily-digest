#!/usr/bin/env python3
"""Tech Product — new product launches & hardware. Cron: TBD"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from sources.lib import call_deepseek, fetch_rss, fetch_reddit, write_output, skip

TOPIC   = "tech_product"
HEADING = "## 🖥️ New Products"

RSS_SOURCES = [
    ("https://www.theverge.com/rss/index.xml", "The Verge", 6),
]
REDDIT_SOURCES = [
    ("hardware", ["release", "launch", "new", "announced", "review"], 4),
]


def run():
    print("[tech_product] Fetching...")
    all_items = []
    raw_parts = []

    for url, label, limit in RSS_SOURCES:
        items = fetch_rss(url, limit=limit)
        print(f"  {label}: {len(items)}")
        all_items.extend(items)
        md = "\n".join(f"- [{n['title']}]({n['url']})" for n in items) or "_No items_"
        raw_parts.append(f"### {label}\n{md}")

    for subreddit, keywords, limit in REDDIT_SOURCES:
        posts = fetch_reddit(subreddit, limit=limit, keywords=keywords)
        print(f"  r/{subreddit}: {len(posts)}")
        md = "\n".join(f"- [{p['title']}]({p['url']})" for p in posts) or "_No posts_"
        raw_parts.append(f"### r/{subreddit}\n{md}")

    if not all_items:
        skip(TOPIC, "no items"); return

    text = "\n".join(f"- {n['title']}: {n['desc']} ({n['url']})" for n in all_items)
    summary = call_deepseek(f"""Summarize today's notable tech product launches or hardware releases.
Focus on specs, pricing, and relevance to developers/engineers.
3-5 bullets with links. English.

{text}""", max_tokens=400)

    write_output(TOPIC, HEADING, summary, "\n\n".join(raw_parts))


if __name__ == "__main__":
    run()
