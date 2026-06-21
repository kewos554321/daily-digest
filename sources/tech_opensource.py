#!/usr/bin/env python3
"""Tech Opensource — open source project releases & updates. Cron: TBD"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from sources.lib import call_deepseek, fetch_rss, fetch_reddit, write_output, skip

TOPIC   = "tech_opensource"
HEADING = "## 🔓 Open Source"

REDDIT_SOURCES = [
    ("opensource",  None, 4),
    ("programming", ["release", "open source", "library", "framework", "v1", "v2", "launched"], 4),
]

RSS_SOURCES = [
    ("https://opensource.com/feed", "Opensource.com", 4),
]


def run():
    print("[tech_opensource] Fetching...")
    all_posts = []
    raw_parts = []

    for url, label, limit in RSS_SOURCES:
        items = fetch_rss(url, limit=limit)
        print(f"  {label}: {len(items)}")
        md = "\n".join(f"- [{n['title']}]({n['url']})" for n in items) or "_No items_"
        raw_parts.append(f"### {label}\n{md}")

    for subreddit, keywords, limit in REDDIT_SOURCES:
        posts = fetch_reddit(subreddit, limit=limit, keywords=keywords)
        print(f"  r/{subreddit}: {len(posts)}")
        all_posts.extend(posts)
        md = "\n".join(f"- [{p['title']}]({p['url']})" for p in posts) or "_No posts_"
        raw_parts.append(f"### r/{subreddit}\n{md}")

    if not all_posts and not raw_parts:
        skip(TOPIC, "no data"); return

    posts_text = "\n".join(f"- {p['title']} ({p['url']})" for p in all_posts)
    summary = call_deepseek(f"""Summarize today's notable open source releases and updates for a software engineer.
Highlight major version releases, new tools, and community-driven projects worth watching.
3-5 bullets with links. English.

{posts_text}""", max_tokens=400)

    write_output(TOPIC, HEADING, summary, "\n\n".join(raw_parts))


if __name__ == "__main__":
    run()
