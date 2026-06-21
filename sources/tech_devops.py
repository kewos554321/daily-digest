#!/usr/bin/env python3
"""Tech DevOps — Cloud, K8s, infra news. Cron: TBD"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from sources.lib import call_deepseek, fetch_rss, fetch_reddit, write_output, skip

TOPIC   = "tech_devops"
HEADING = "## ☁️ DevOps & Cloud"

RSS_SOURCES = [
    ("https://aws.amazon.com/blogs/aws/feed/", "AWS Blog", 4),
]

REDDIT_SOURCES = [
    ("devops",     ["kubernetes", "k8s", "docker", "ci", "cd", "terraform", "aws", "gcp", "azure", "infra"], 4),
    ("kubernetes", None, 3),
]


def run():
    print("[tech_devops] Fetching...")
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

    if not all_items and not any(raw_parts):
        skip(TOPIC, "no data"); return

    text = "\n".join(f"- {n['title']}: {n['desc']} ({n['url']})" for n in all_items)
    summary = call_deepseek(f"""Summarize today's DevOps and cloud infrastructure news for a software engineer.
Focus on: new cloud services, K8s updates, cost optimization tips, CI/CD improvements.
3-5 bullets with links. English.

{text}""", max_tokens=500)

    write_output(TOPIC, HEADING, summary, "\n\n".join(raw_parts))


if __name__ == "__main__":
    run()
