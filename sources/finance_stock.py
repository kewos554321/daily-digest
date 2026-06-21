#!/usr/bin/env python3
"""Finance Stock — watchlist fundamentals. Cron: 8:05 AM Taipei"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import config as cfg
from sources.lib import (call_deepseek, fetch_fmp_stock, fetch_twse_stock,
                         fetch_twse_all, fetch_stock_news, write_output, skip)

TOPIC   = "finance_stock"
HEADING = "## 📊 Watchlist"


def run():
    print("[finance_stock] Fetching watchlist...")
    twse_cache = fetch_twse_all()  # 一次抓所有台股
    stocks = []
    for symbol, name in cfg.WATCHLIST:
        print(f"  {symbol}...")
        # 台股用 TWSE，美股用 FMP
        if symbol.endswith(".TW"):
            code = symbol.replace(".TW", "")
            fund = fetch_twse_stock(code, name, twse_cache)
        else:
            fund = fetch_fmp_stock(symbol, name)
        news = fetch_stock_news(symbol, limit=3)
        if fund:
            stocks.append({"fund": fund, "news": news})

    if not stocks:
        skip(TOPIC, "no stock data"); return

    stock_lines = "\n".join(
        f"{s['fund']['name']} ({s['fund']['symbol']}): {s['fund']['price']} | "
        f"P/E {s['fund']['pe_ttm']} | ROE {s['fund']['roe']} | FCF {s['fund']['fcf']}"
        for s in stocks
    )

    summary = call_deepseek(f"""Summarize today's watchlist for a Taiwanese software engineer focused on AI stocks.

{stock_lines}

3-5 bullet points on notable movers and valuation standouts. Include numbers. English.""",
        max_tokens=500)

    raw_md = ""
    for s in stocks:
        f = s["fund"]
        raw_md += f"""
#### {f['name']} ({f['symbol']})
| Metric | Value |
|---|---|
| Price | {f['price']} |
| Market Cap | {f['mktcap']} |
| P/E (TTM / Fwd) | {f['pe_ttm']} / {f['pe_fwd']} |
| EPS (TTM / Fwd) | {f['eps_ttm']} / {f['eps_fwd']} |
| Revenue (TTM) | {f['revenue']} |
| Gross / Op / Net Margin | {f['gm']} / {f['om']} / {f['nm']} |
| Free Cash Flow | {f['fcf']} |
| ROE | {f['roe']} |
| D/E Ratio | {f['de']} |
| P/B | {f['pb']} |
| Beta | {f['beta']} |
| 52-Week | {f['w52l']} – {f['w52h']} |
| Div. Yield | {f['div']} |"""
        if s["news"]:
            raw_md += "\n\n**Recent News:**\n" + "\n".join(
                f"- [{n['title']}]({n['url']}) — {n['source']}" for n in s["news"]
            )
        raw_md += "\n"

    write_output(TOPIC, HEADING, summary, raw_md.strip())


if __name__ == "__main__":
    run()
