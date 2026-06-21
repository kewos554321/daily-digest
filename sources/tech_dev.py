#!/usr/bin/env python3
"""Tech Dev — developer tools & GitHub trending. Cron: TBD"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import urllib.request
import json
from sources.lib import call_deepseek, fetch_rss, write_output, skip

TOPIC   = "tech_dev"
HEADING = "## 🛠️ Dev Tools"

GITHUB_TRENDING_URL = "https://github-trending-api.wakatime.com/repositories?language=&since=daily"

DEV_RSS = [
    ("https://github.blog/feed/", "GitHub Blog", 4),
]


def fetch_github_trending(limit=8):
    try:
        req = urllib.request.Request(
            GITHUB_TRENDING_URL,
            headers={"User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(req, timeout=15) as r:
            repos = json.loads(r.read())
        return [
            {"name": repo.get("name", ""),
             "desc": repo.get("description", "")[:120],
             "url":  repo.get("url", ""),
             "lang": repo.get("language", ""),
             "stars": repo.get("stars", 0)}
            for repo in repos[:limit]
        ]
    except Exception as e:
        print(f"  GitHub trending error: {e}")
        return []


def run():
    print("[tech_dev] Fetching...")
    repos = fetch_github_trending()
    print(f"  GitHub trending: {len(repos)}")

    rss_items = []
    for url, label, limit in DEV_RSS:
        items = fetch_rss(url, limit=limit)
        print(f"  {label}: {len(items)}")
        rss_items.extend(items)

    if not repos and not rss_items:
        skip(TOPIC, "no data"); return

    repos_text = "\n".join(
        f"- {r['name']} ({r['lang']}): {r['desc']} ⭐{r['stars']} {r['url']}"
        for r in repos
    )
    summary = call_deepseek(f"""Summarize today's developer tools and GitHub trending repos for a software engineer.
Highlight any AI/dev productivity tools, notable new libraries, or interesting projects.
3-5 bullets with links. English.

GitHub Trending:
{repos_text}""", max_tokens=500)

    repos_md = "\n".join(
        f"- [{r['name']}]({r['url']}) `{r['lang']}` ⭐{r['stars']} — {r['desc']}"
        for r in repos
    )
    raw_md = f"### GitHub Trending\n{repos_md}"
    if rss_items:
        rss_md = "\n".join(f"- [{n['title']}]({n['url']})" for n in rss_items)
        raw_md += f"\n\n### GitHub Blog\n{rss_md}"

    write_output(TOPIC, HEADING, summary, raw_md)


if __name__ == "__main__":
    run()
