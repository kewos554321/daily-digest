#!/usr/bin/env python3
"""Tech Career — software job market, salary, hiring trends. Cron: TBD"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from datetime import datetime
import config as cfg
from sources.lib import call_deepseek, fetch_reddit, write_output, skip

TOPIC   = "tech_career"
HEADING = "## 💼 Career Trends"

REDDIT_SOURCES = [
    ("cscareerquestions", ["salary", "layoff", "hiring", "interview", "job", "offer", "remote", "ai", "market"], 5),
    ("ExperiencedDevs",   ["market", "hiring", "salary", "layoff", "trend"], 3),
]


def run():
    print("[tech_career] Fetching...")
    date_str = datetime.now(cfg.TZ).strftime("%Y-%m-%d")
    month    = datetime.now(cfg.TZ).strftime("%B %Y")

    all_posts = []
    raw_parts = []

    for subreddit, keywords, limit in REDDIT_SOURCES:
        posts = fetch_reddit(subreddit, limit=limit, keywords=keywords)
        print(f"  r/{subreddit}: {len(posts)}")
        all_posts.extend(posts)
        md = "\n".join(f"- [{p['title']}]({p['url']})" for p in posts) or "_No posts_"
        raw_parts.append(f"### r/{subreddit}\n{md}")

    # AI market pulse (always runs)
    market_pulse = call_deepseek(f"""You are a tech career advisor. Today is {date_str} ({month}).

Provide a brief software engineering job market pulse:
- Current hiring sentiment (hot/cold/mixed) for AI/backend/full-stack roles
- Key skills in demand right now
- Any notable layoffs or hiring surges this month
- Salary trend direction (US market, remote-friendly)

3-4 bullet points. Be direct and specific. English.""",
        max_tokens=350, temperature=0.4)

    posts_text = "\n".join(f"- {p['title']} ({p['url']})" for p in all_posts)
    summary = f"Market Pulse:\n{market_pulse}"
    if all_posts:
        summary += f"\n\nReddit:\n{posts_text}"

    raw_md = f"### AI Market Pulse — {month}\n{market_pulse}\n\n" + "\n\n".join(raw_parts)
    write_output(TOPIC, HEADING, summary, raw_md)


if __name__ == "__main__":
    run()
