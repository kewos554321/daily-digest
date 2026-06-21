#!/usr/bin/env python3
"""Tech AI Companies — OpenAI / Anthropic / Tesla news. Cron: 7:50 AM Taipei"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import json
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from sources.lib import fetch_rss, call_deepseek, write_output, skip

TOPIC   = "tech_ai_companies"
HEADING = "## 🤖 AI 公司動態 (OpenAI / Anthropic / Tesla)"

# RSS / public feeds
FEEDS = [
    ("https://openai.com/blog/rss/",              "OpenAI"),
    ("https://www.anthropic.com/feed.xml",         "Anthropic"),
    ("https://www.tesla.com/blog/rss.xml",         "Tesla"),
]

# Fallback: Yahoo Finance news for tickers when RSS is unavailable
TICKERS = [
    ("TSLA",  "Tesla"),
    ("GOOGL", "Google/DeepMind"),  # bonus: covers Google AI news from finance angle
]


def fetch_yahoo_news(symbol, limit=3):
    try:
        url = (f"https://query1.finance.yahoo.com/v1/finance/search"
               f"?q={urllib.parse.quote(symbol)}&newsCount={limit}&quotesCount=0")
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            items = json.loads(r.read()).get("news", [])
        return [{"title": n.get("title", ""), "url": n.get("link", "")} for n in items]
    except Exception as e:
        print(f"  Yahoo news error ({symbol}): {e}")
        return []


def run():
    print("[tech_ai_companies] Fetching...")
    items = []

    for url, label in FEEDS:
        posts = fetch_rss(url, limit=4)
        for p in posts:
            if p.get("title"):
                items.append({"label": label, "title": p["title"], "url": p["url"]})
        print(f"  {label} RSS: {len(posts)}")

    # Fallback to Yahoo Finance news for companies with unreliable RSS
    # Only use if that company has 0 items from RSS
    rss_labels = {i["label"] for i in items}
    for symbol, label in [("TSLA", "Tesla")]:
        if label not in rss_labels:
            news = fetch_yahoo_news(symbol, limit=4)
            for n in news:
                if n.get("title"):
                    items.append({"label": label, "title": n["title"], "url": n["url"]})
            if news:
                print(f"  {label} (Yahoo fallback): {len(news)}")

    if not items:
        skip(TOPIC, "no AI company posts fetched"); return

    text = "\n".join(f"[{i['label']}] {i['title']} ({i['url']})" for i in items)
    summary = call_deepseek(f"""Summarize today's updates from major AI companies for a software engineer.

Posts:
{text}

Write 3-5 bullet points covering the most important news from OpenAI, Anthropic, and Tesla.
Focus on product releases, research breakthroughs, and business developments.
Include links. English. Be concise.""", max_tokens=600)

    raw_md = ""
    for label in ["OpenAI", "Anthropic", "Tesla"]:
        section_items = [i for i in items if i["label"] == label]
        if section_items:
            raw_md += f"\n### {label}\n"
            raw_md += "\n".join(f"- [{i['title']}]({i['url']})" for i in section_items)
    raw_md = raw_md.strip()

    write_output(TOPIC, HEADING, summary, raw_md)


if __name__ == "__main__":
    run()
