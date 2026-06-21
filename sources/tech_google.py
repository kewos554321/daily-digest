#!/usr/bin/env python3
"""Tech Google — Google Blog + Google AI Blog RSS. Cron: 7:50 AM Taipei"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from sources.lib import fetch_rss, call_deepseek, write_output, skip

TOPIC   = "tech_google"
HEADING = "## 🔵 Google 動態"

FEEDS = [
    ("https://blog.google/technology/ai/rss/",  "Google AI Blog"),
    ("https://blog.google/rss/",                "Google Blog"),
    ("https://developers.googleblog.com/feeds/posts/default?alt=rss", "Google Developers"),
]


def run():
    print("[tech_google] Fetching...")
    items = []
    for url, label in FEEDS:
        posts = fetch_rss(url, limit=5)
        for p in posts:
            if p.get("title"):
                items.append({"label": label, "title": p["title"], "url": p["url"], "desc": p["desc"]})
        print(f"  {label}: {len(posts)}")

    if not items:
        skip(TOPIC, "no Google posts fetched"); return

    text = "\n".join(f"[{i['label']}] {i['title']} — {i['desc']} ({i['url']})" for i in items)
    summary = call_deepseek(f"""Summarize today's Google updates for a software engineer.

Posts:
{text}

Write 3-5 bullet points covering the most important announcements (AI, developer tools, products).
Include links. English. Be concise.""", max_tokens=600)

    raw_md = ""
    for label in [l for _, l in FEEDS]:
        section_items = [i for i in items if i["label"] == label]
        if section_items:
            raw_md += f"\n### {label}\n"
            raw_md += "\n".join(f"- [{i['title']}]({i['url']})" for i in section_items)
    raw_md = raw_md.strip()

    write_output(TOPIC, HEADING, summary, raw_md)


if __name__ == "__main__":
    run()
