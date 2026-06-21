#!/usr/bin/env python3
"""Finance Markets — indices overview. Cron: 8:00 AM Taipei"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import config as cfg
from sources.lib import call_deepseek, fetch_index_quote, write_output, skip

TOPIC   = "finance_markets"
HEADING = "## 📈 Markets Overview"


def run():
    print("[finance_markets] Fetching indices...")
    indices = [q for sym, name in cfg.INDICES if (q := fetch_index_quote(sym, name))]
    print(f"  Indices: {[i['line'] for i in indices]}")

    if not indices:
        skip(TOPIC, "no index data"); return

    idx_lines = "\n".join(i["line"] for i in indices)
    summary = call_deepseek(f"""Summarize today's major market indices for a Taiwanese investor.

Indices:
{idx_lines}

2-3 bullet points covering notable moves and overall sentiment. Include numbers. English.""",
        max_tokens=300)

    raw_md = "### Indices\n" + "\n".join(f"- {i['line']}" for i in indices)
    write_output(TOPIC, HEADING, summary, raw_md)


if __name__ == "__main__":
    run()
