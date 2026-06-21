#!/usr/bin/env python3
"""Finance Screener — 錯殺優質股掃描. Cron: 8:15 AM Taipei"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import config as cfg
from sources.lib import (call_deepseek, fetch_fmp_stock, fetch_twse_stock,
                         fetch_twse_all, fetch_index_quote, write_output, skip)

TOPIC   = "finance_screener"
HEADING = "## 🔍 Screener — Quality Dip"

# Thresholds
DROP_THRESHOLD  = 0.10   # 10% drop from 52-week high
MIN_ROE         = 0.12   # 12% ROE minimum
MAX_DE          = 2.0    # D/E ratio max


def run():
    print("[finance_screener] Scanning for quality dips...")

    # Benchmark: get S&P500 daily move for comparison
    sp = fetch_index_quote("^GSPC", "S&P 500")
    sp_pct = sp["pct"] if sp else 0
    print(f"  S&P 500 today: {sp_pct:+.2f}%")

    twse_cache = fetch_twse_all()
    candidates = []
    for symbol, name in cfg.WATCHLIST:
        if symbol.endswith(".TW"):
            d = fetch_twse_stock(symbol.replace(".TW", ""), name, twse_cache)
        else:
            d = fetch_fmp_stock(symbol, name)
        if not d:
            continue

        price = d.get("_price")
        w52h  = d.get("_w52h")
        roe   = d.get("_roe")
        de    = d.get("_de")
        fcf   = d.get("_fcf_ps")
        pct_day = d.get("_pct", 0)
        drop_from_high = (w52h - price) / w52h if w52h and price else 0

        # Filter criteria
        roe_ok  = roe is not None and roe >= MIN_ROE
        de_ok   = de is None or de <= MAX_DE
        fcf_ok  = fcf is not None and fcf > 0
        drop_ok = drop_from_high >= DROP_THRESHOLD
        macro_driven = pct_day >= sp_pct * 0.5  # falls with market, not worse

        if drop_ok and roe_ok and de_ok and fcf_ok:
            candidates.append({
                "name": name, "symbol": symbol,
                "drop_from_high": drop_from_high,
                "roe": roe, "de": de,
                "pct_day": pct_day, "macro_driven": macro_driven,
            })
            print(f"  ✓ {symbol}: -{drop_from_high*100:.1f}% from 52wH, ROE={roe*100:.1f}%")

    if not candidates:
        skip(TOPIC, "no quality dip candidates today"); return

    cand_text = "\n".join(
        f"- {c['name']} ({c['symbol']}): "
        f"drop {c['drop_from_high']*100:.1f}% from 52wH, "
        f"ROE {c['roe']*100:.1f}%, "
        f"D/E {c['de']:.2f if c['de'] is not None else 'N/A'}, "
        f"today {c['pct_day']:+.2f}% vs market {sp_pct:+.2f}%, "
        f"macro-driven: {c['macro_driven']}"
        for c in candidates
    )

    summary = call_deepseek(f"""You are a fundamental analyst. Today S&P 500 moved {sp_pct:+.2f}%.

These quality stocks have dropped significantly from their 52-week high but maintain strong fundamentals:

{cand_text}

For each candidate:
- Assess whether the drop looks macro-driven or company-specific
- Note if it's a potential buying opportunity based on fundamentals
- Flag any concern

3-5 bullet points. Be direct and specific. English.""", max_tokens=500)

    raw_md = f"S&P 500 today: {sp_pct:+.2f}%\n\n### Quality Dip Candidates\n" + "\n".join(
        f"- **{c['name']}** ({c['symbol']}) | "
        f"Drop from 52wH: {c['drop_from_high']*100:.1f}% | "
        f"ROE: {c['roe']*100:.1f}% | "
        f"Today: {c['pct_day']:+.2f}% | "
        f"Macro-driven: {'✓' if c['macro_driven'] else '✗'}"
        for c in candidates
    )
    write_output(TOPIC, HEADING, summary, raw_md)


if __name__ == "__main__":
    run()
