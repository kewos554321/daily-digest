#!/usr/bin/env python3
"""Tech Security — CVE, vulnerability, security news. Cron: TBD"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from sources.lib import call_deepseek, fetch_rss, fetch_reddit, write_output, skip

TOPIC   = "tech_security"
HEADING = "## 🔒 Security"

RSS_SOURCES = [
    ("https://feeds.feedburner.com/TheHackersNews", "The Hacker News", 6),
    ("https://www.bleepingcomputer.com/feed/",      "BleepingComputer", 4),
]

REDDIT_KEYWORDS = ["cve", "vulnerability", "breach", "exploit", "patch", "0day", "ransomware", "supply chain"]


def run():
    print("[tech_security] Fetching...")
    all_items = []
    raw_parts = []

    for url, label, limit in RSS_SOURCES:
        items = fetch_rss(url, limit=limit)
        print(f"  {label}: {len(items)}")
        all_items.extend(items)
        md = "\n".join(f"- [{n['title']}]({n['url']})" for n in items) or "_No items_"
        raw_parts.append(f"### {label}\n{md}")

    if not all_items:
        skip(TOPIC, "no security news"); return

    text = "\n".join(f"- {n['title']}: {n['desc']} ({n['url']})" for n in all_items)
    summary = call_deepseek(f"""Summarize today's security news for a software engineer.
Focus on: CVEs affecting common packages/frameworks, major breaches, and patches to apply.
3-5 bullets with links and CVE numbers where available. English.

{text}""", max_tokens=500)

    write_output(TOPIC, HEADING, summary, "\n\n".join(raw_parts))


if __name__ == "__main__":
    run()
