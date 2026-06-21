"""Shared utilities for all digest source scripts."""

import os
import sys
import json
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime

# Allow importing config from parent directory
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import config as cfg

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "output")


# ── Output helpers ────────────────────────────────────────────────────────────

def write_output(topic, heading, summary, raw_md):
    """Write section output JSON for today. Called when content is notable."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    date_str = datetime.now(cfg.TZ).strftime("%Y-%m-%d")
    path = os.path.join(OUTPUT_DIR, f"{date_str}_{topic}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump({
            "topic":        topic,
            "heading":      heading,
            "summary":      summary,
            "raw_md":       raw_md,
            "generated_at": datetime.now(cfg.TZ).strftime("%Y-%m-%d %H:%M:%S"),
        }, f, ensure_ascii=False, indent=2)
    print(f"[{topic}] Output written → {os.path.basename(path)}")


def skip(topic, reason="nothing notable today"):
    print(f"[{topic}] Skipped — {reason}")


# ── API helpers ───────────────────────────────────────────────────────────────

def call_deepseek(prompt, max_tokens=1000, temperature=0.3):
    payload = json.dumps({
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": temperature,
    }).encode()
    req = urllib.request.Request(
        cfg.DEEPSEEK_BASE_URL,
        data=payload,
        headers={"Content-Type": "application/json",
                 "Authorization": f"Bearer {cfg.DEEPSEEK_API_KEY}"},
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        result = json.loads(r.read())
    return result["choices"][0]["message"]["content"].strip()


def fetch_rss(url, limit=8):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as r:
            root = ET.fromstring(r.read())
        return [
            {"title": (i.findtext("title") or "").strip(),
             "url":   (i.findtext("link")  or "").strip(),
             "desc":  (i.findtext("description") or "").strip()[:200]}
            for i in root.findall(".//item")[:limit]
        ]
    except Exception as e:
        print(f"  RSS error: {e}")
        return []


def fetch_reddit(subreddit, limit=6, keywords=None):
    try:
        url = f"https://www.reddit.com/r/{subreddit}/hot.rss?limit=25"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 daily-brief/1.0"})
        with urllib.request.urlopen(req, timeout=15) as r:
            root = ET.fromstring(r.read())
        ns = {"a": "http://www.w3.org/2005/Atom"}
        posts = []
        for entry in root.findall("a:entry", ns):
            title    = (entry.findtext("a:title", "", ns) or "").strip()
            link_el  = entry.find("a:link", ns)
            url_post = link_el.get("href", "") if link_el is not None else ""
            if keywords and not any(k.lower() in title.lower() for k in keywords):
                continue
            posts.append({"title": title, "url": url_post})
            if len(posts) >= limit:
                break
        return posts
    except Exception as e:
        print(f"  Reddit error (r/{subreddit}): {e}")
        return []


def fetch_index_quote(symbol, name):
    try:
        url = (f"https://query1.finance.yahoo.com/v8/finance/chart/"
               f"{urllib.parse.quote(symbol)}?interval=1d&range=2d")
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            meta = json.loads(r.read())["chart"]["result"][0]["meta"]
        price = meta.get("regularMarketPrice", 0)
        prev  = meta.get("previousClose") or meta.get("chartPreviousClose") or price
        pct   = (price - prev) / prev * 100 if prev else 0
        arrow = "▲" if pct >= 0 else "▼"
        return {"name": name, "symbol": symbol, "price": price,
                "pct": pct, "line": f"{name}: {price:,.2f} {arrow}{abs(pct):.2f}%"}
    except Exception as e:
        print(f"  Index error ({symbol}): {e}")
        return None


def _raw(d, key):
    v = d.get(key)
    return v.get("raw") if isinstance(v, dict) else v


def _fmt(val, fmt=".2f", scale=1):
    if val is None:
        return "N/A"
    try:
        v = float(val) * scale
        if abs(v) >= 1e12: return f"${v/1e12:.2f}T"
        if abs(v) >= 1e9:  return f"${v/1e9:.2f}B"
        if abs(v) >= 1e6:  return f"${v/1e6:.2f}M"
        return f"{v:{fmt}}"
    except Exception:
        return "N/A"


def fetch_stock_fundamentals(symbol, name):
    try:
        modules = "price,summaryDetail,financialData,defaultKeyStatistics"
        url = (f"https://query1.finance.yahoo.com/v10/finance/quoteSummary/"
               f"{urllib.parse.quote(symbol)}?modules={urllib.parse.quote(modules)}")
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as r:
            data = json.loads(r.read())["quoteSummary"]["result"][0]
        pr = data.get("price", {})
        sd = data.get("summaryDetail", {})
        fd = data.get("financialData", {})
        ks = data.get("defaultKeyStatistics", {})
        price = _raw(pr, "regularMarketPrice")
        prev  = _raw(pr, "regularMarketPreviousClose") or price
        pct   = (price - prev) / prev * 100 if price and prev else 0
        arrow = "▲" if pct >= 0 else "▼"
        gm  = _raw(fd, "grossMargins")
        om  = _raw(fd, "operatingMargins")
        nm  = _raw(fd, "profitMargins")
        roe = _raw(fd, "returnOnEquity")
        div = _raw(sd, "dividendYield")
        de  = _raw(fd, "debtToEquity")
        pb  = _raw(ks, "priceToBook")
        beta = _raw(ks, "beta")
        return {
            "name": name, "symbol": symbol,
            "price":   f"{price:,.2f} {arrow}{abs(pct):.2f}%" if price else "N/A",
            "mktcap":  _fmt(_raw(pr, "marketCap")),
            "pe_ttm":  _fmt(_raw(sd, "trailingPE"), ".1f"),
            "pe_fwd":  _fmt(_raw(sd, "forwardPE"),  ".1f"),
            "eps_ttm": _fmt(_raw(ks, "trailingEps"), ".2f"),
            "eps_fwd": _fmt(_raw(ks, "forwardEps"),  ".2f"),
            "revenue": _fmt(_raw(fd, "totalRevenue")),
            "gm":  f"{gm*100:.1f}%"  if gm  else "N/A",
            "om":  f"{om*100:.1f}%"  if om  else "N/A",
            "nm":  f"{nm*100:.1f}%"  if nm  else "N/A",
            "fcf": _fmt(_raw(fd, "freeCashflow")),
            "roe": f"{roe*100:.1f}%" if roe else "N/A",
            "de":  f"{de:.2f}"       if de  else "N/A",
            "pb":  f"{pb:.2f}"       if pb  else "N/A",
            "beta": f"{beta:.2f}"    if beta else "N/A",
            "w52h": _fmt(_raw(sd, "fiftyTwoWeekHigh"), ".2f"),
            "w52l": _fmt(_raw(sd, "fiftyTwoWeekLow"),  ".2f"),
            "div":  f"{div*100:.2f}%" if div else "—",
        }
    except Exception as e:
        print(f"  Fundamentals error ({symbol}): {e}")
        return None


def fetch_twse_all():
    """Fetch all TWSE stocks' latest closing price. Returns dict {code: data}."""
    try:
        url = "https://www.twse.com.tw/rwd/zh/afterTrading/STOCK_DAY_ALL?response=json"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as r:
            data = json.loads(r.read())
        # fields: 證券代號, 證券名稱, 成交股數, 成交金額, 開盤價, 最高價, 最低價, 收盤價, 漲跌價差, 本益比
        fields = data.get("fields", [])
        result = {}
        for row in data.get("data", []):
            d = dict(zip(fields, row))
            code = d.get("證券代號", "").strip()
            if code:
                result[code] = d
        return result
    except Exception as e:
        print(f"  TWSE STOCK_DAY_ALL error: {e}")
        return {}


def fetch_twse_stock(code, name, twse_cache=None):
    """Get Taiwan stock data from TWSE. Uses cache if provided."""
    try:
        cache = twse_cache or fetch_twse_all()
        d = cache.get(code)
        if not d:
            return None

        def to_float(s):
            try:
                return float(str(s).replace(",", ""))
            except Exception:
                return None

        close  = to_float(d.get("收盤價"))
        change = to_float(d.get("漲跌價差"))
        prev   = (close - change) if close is not None and change is not None else None
        pct    = (change / prev * 100) if prev and prev != 0 else 0
        arrow  = "▲" if pct >= 0 else "▼"
        pe     = to_float(d.get("本益比"))

        return {
            "name": name, "symbol": code,
            "price":   f"{close:,.2f} {arrow}{abs(pct):.2f}%" if close else "N/A",
            "mktcap":  "N/A",
            "pe_ttm":  f"{pe:.1f}" if pe else "N/A",
            "pe_fwd":  "N/A", "eps_ttm": "N/A", "eps_fwd": "N/A",
            "revenue": "N/A", "gm": "N/A", "om": "N/A", "nm": "N/A",
            "fcf": "N/A", "roe": "N/A", "de": "N/A", "pb": "N/A", "beta": "N/A",
            "w52h": "N/A", "w52l": "N/A", "div": "—",
            "_price": close, "_w52h": None,
            "_roe": None, "_de": None, "_fcf_ps": None, "_pct": pct,
        }
    except Exception as e:
        print(f"  TWSE error ({code}): {e}")
        return None


def fetch_fmp_stock(symbol, name):
    """Fetch price + fundamentals from FMP stable API. Falls back to v8 price-only if FMP fails."""
    try:
        sym = urllib.parse.quote(symbol)
        key = cfg.FMP_API_KEY
        base = cfg.FMP_BASE_URL

        # Quote
        with urllib.request.urlopen(
            urllib.request.Request(f"{base}/quote?symbol={sym}&apikey={key}",
                                   headers={"User-Agent": "Mozilla/5.0"}), timeout=15) as r:
            quotes = json.loads(r.read())
        if not quotes:
            raise ValueError("empty quote response")
        q = quotes[0]

        # Profile (beta, 52w range)
        with urllib.request.urlopen(
            urllib.request.Request(f"{base}/profile?symbol={sym}&apikey={key}",
                                   headers={"User-Agent": "Mozilla/5.0"}), timeout=15) as r:
            profiles = json.loads(r.read())
        pr = profiles[0] if profiles else {}

        # Ratios TTM (margins, ROE, D/E, P/B)
        with urllib.request.urlopen(
            urllib.request.Request(f"{base}/ratios-ttm?symbol={sym}&apikey={key}",
                                   headers={"User-Agent": "Mozilla/5.0"}), timeout=15) as r:
            ratios_list = json.loads(r.read())
        rt = ratios_list[0] if ratios_list else {}

        # Key metrics TTM (FCF, EV metrics)
        with urllib.request.urlopen(
            urllib.request.Request(f"{base}/key-metrics-ttm?symbol={sym}&apikey={key}",
                                   headers={"User-Agent": "Mozilla/5.0"}), timeout=15) as r:
            metrics_list = json.loads(r.read())
        km = metrics_list[0] if metrics_list else {}

        price = q.get("price", 0)
        pct   = q.get("changePercentage", 0)
        arrow = "▲" if pct >= 0 else "▼"

        # Parse 52w range from profile "range" field "86.62-212.19"
        w52l, w52h = None, None
        rng = pr.get("range", "")
        if "-" in str(rng):
            parts = str(rng).split("-")
            try:
                w52l, w52h = float(parts[0]), float(parts[1])
            except Exception:
                pass

        def pct_fmt(v):
            return f"{float(v)*100:.1f}%" if v is not None else "N/A"

        def val_fmt(v):
            if v is None: return "N/A"
            try:
                v = float(v)
                if abs(v) >= 1e12: return f"${v/1e12:.2f}T"
                if abs(v) >= 1e9:  return f"${v/1e9:.2f}B"
                if abs(v) >= 1e6:  return f"${v/1e6:.2f}M"
                return f"{v:.2f}"
            except Exception:
                return "N/A"

        roe    = rt.get("returnOnEquityTTM")
        de     = rt.get("debtEquityRatioTTM")
        gm     = rt.get("grossProfitMarginTTM")
        om     = rt.get("operatingProfitMarginTTM")
        nm     = rt.get("netProfitMarginTTM")
        pb     = rt.get("priceToBookRatioTTM")
        pe     = rt.get("priceEarningsRatioTTM")
        beta   = pr.get("beta")
        mktcap = q.get("marketCap") or pr.get("marketCap")
        fcf    = km.get("freeCashFlowPerShareTTM")
        rev    = km.get("revenuePerShareTTM")

        return {
            "name": name, "symbol": symbol,
            "price":   f"{price:,.2f} {arrow}{abs(pct):.2f}%",
            "mktcap":  val_fmt(mktcap),
            "pe_ttm":  f"{float(pe):.1f}" if pe else "N/A",
            "pe_fwd":  "N/A",
            "eps_ttm": "N/A",
            "eps_fwd": "N/A",
            "revenue": val_fmt(rev),
            "gm":  pct_fmt(gm),
            "om":  pct_fmt(om),
            "nm":  pct_fmt(nm),
            "fcf": val_fmt(fcf),
            "roe": pct_fmt(roe),
            "de":  f"{float(de):.2f}" if de is not None else "N/A",
            "pb":  f"{float(pb):.2f}" if pb is not None else "N/A",
            "beta": f"{float(beta):.2f}" if beta else "N/A",
            "w52h": f"{w52h:.2f}" if w52h else "N/A",
            "w52l": f"{w52l:.2f}" if w52l else "N/A",
            "div":  "—",
            "_price": price,
            "_w52h":  w52h,
            "_roe":   float(roe) if roe is not None else None,
            "_de":    float(de)  if de  is not None else None,
            "_fcf_ps": float(fcf) if fcf is not None else None,
            "_pct":   pct,
        }
    except Exception as e:
        print(f"  FMP error ({symbol}): {e}")
        # fallback: v8 price only
        try:
            q = fetch_index_quote(symbol, name)
            if q:
                return {
                    "name": name, "symbol": symbol,
                    "price": q["line"], "mktcap": "N/A",
                    "pe_ttm": "N/A", "pe_fwd": "N/A",
                    "eps_ttm": "N/A", "eps_fwd": "N/A",
                    "revenue": "N/A", "gm": "N/A", "om": "N/A", "nm": "N/A",
                    "fcf": "N/A", "roe": "N/A", "de": "N/A",
                    "pb": "N/A", "beta": "N/A",
                    "w52h": "N/A", "w52l": "N/A", "div": "—",
                    "_price": q["price"], "_w52h": None,
                    "_roe": None, "_de": None, "_fcf_ps": None, "_pct": q["pct"],
                }
        except Exception:
            pass
        return None


def fetch_stock_news(symbol, limit=3):
    try:
        url = (f"https://query1.finance.yahoo.com/v1/finance/search"
               f"?q={urllib.parse.quote(symbol)}&newsCount={limit}&quotesCount=0")
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            items = json.loads(r.read()).get("news", [])
        return [{"title": n.get("title", ""), "url": n.get("link", ""),
                 "source": n.get("publisher", "")} for n in items]
    except Exception as e:
        print(f"  Stock news error ({symbol}): {e}")
        return []


# ── State helpers (for finance rotation) ─────────────────────────────────────

def load_state():
    state_file = os.path.join(os.path.dirname(__file__), "..", "state.json")
    if os.path.exists(state_file):
        with open(state_file, encoding="utf-8") as f:
            return json.load(f), state_file
    return {"finance_queue": [], "finance_last": None}, state_file


def save_state(state, state_file):
    with open(state_file, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
