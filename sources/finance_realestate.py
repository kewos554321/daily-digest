#!/usr/bin/env python3
"""Finance Realestate — 台灣房市資訊. Cron: 隨 finance.py"""

import sys, os, io, zipfile, csv
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from datetime import datetime
import urllib.request
import xml.etree.ElementTree as ET
import config as cfg
from sources.lib import call_deepseek, fetch_rss, write_output, skip

TOPIC   = "finance_realestate"
HEADING = "## 🏠 台灣房市"


def fetch_591_rss(limit=8):
    """591 RSS — 最新掛牌物件與新聞"""
    try:
        url = "https://www.591.com.tw/rss.xml"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as r:
            root = ET.fromstring(r.read())
        items = []
        for item in root.findall(".//item")[:limit]:
            title = (item.findtext("title") or "").strip()
            link  = (item.findtext("link")  or "").strip()
            desc  = (item.findtext("description") or "").strip()[:150]
            items.append({"title": title, "url": link, "desc": desc})
        return items
    except Exception as e:
        print(f"  591 RSS error: {e}")
        return []


def fetch_lvr_recent(limit=5):
    """內政部實價登錄 — 最近一季台北市成交資料 (a=台北市)"""
    try:
        # 計算最近一季：113年 = 2024年
        now = datetime.now(cfg.TZ)
        year_roc = now.year - 1911
        quarter  = (now.month - 1) // 3  # 當季還未完，取上一季
        if quarter == 0:
            year_roc -= 1
            quarter = 4
        season = f"{year_roc}S{quarter}"
        url = (f"https://plvr.land.moi.gov.tw/DownloadSeason"
               f"?season={season}&type=zip&fileName=a_lvr_land_a.csv")
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=20) as r:
            raw = r.read()

        # 嘗試解析 CSV（內政部有時直接回 CSV，有時是 zip）
        try:
            zf = zipfile.ZipFile(io.BytesIO(raw))
            csv_name = [n for n in zf.namelist() if n.endswith(".csv")][0]
            content  = zf.read(csv_name).decode("utf-8-sig")
        except Exception:
            content = raw.decode("utf-8-sig")

        reader = csv.DictReader(io.StringIO(content))
        rows   = []
        for i, row in enumerate(reader):
            if i >= 200:  # 只取前200筆避免太重
                break
            rows.append(row)

        if not rows:
            return [], season

        # 整理最近成交：取高總價物件
        def safe_float(v):
            try:
                return float(str(v).replace(",", ""))
            except Exception:
                return 0

        rows.sort(key=lambda r: safe_float(r.get("總價元", 0)), reverse=True)
        result = []
        for row in rows[:limit]:
            addr   = row.get("土地區段位置或建物區門牌", "")
            type_  = row.get("建物型態", "")
            area   = row.get("建物移轉總面積平方公尺", "")
            price  = row.get("總價元", "")
            unit   = row.get("單價元平方公尺", "")
            date   = row.get("交易年月日", "")
            result.append({
                "addr": addr, "type": type_,
                "area": f"{float(area):.1f}㎡" if area else "N/A",
                "price": f"{safe_float(price)/1e4:.0f}萬" if price else "N/A",
                "unit": f"{safe_float(unit):.0f}元/㎡" if unit else "N/A",
                "date": date,
            })
        return result, season

    except Exception as e:
        print(f"  實價登錄 error: {e}")
        return [], "N/A"


def run():
    print("[finance_realestate] Fetching...")
    date_str = datetime.now(cfg.TZ).strftime("%Y-%m-%d")
    month    = datetime.now(cfg.TZ).strftime("%B %Y")

    # 591 RSS
    listings = fetch_591_rss(limit=8)
    print(f"  591 RSS: {len(listings)} items")

    # 實價登錄
    lvr, season = fetch_lvr_recent(limit=5)
    print(f"  實價登錄 ({season}): {len(lvr)} records")

    if not listings and not lvr:
        skip(TOPIC, "no data"); return

    listings_text = "\n".join(f"- {l['title']} ({l['url']})" for l in listings)
    lvr_text = "\n".join(
        f"- {r['addr']} | {r['type']} | {r['area']} | 總價:{r['price']} | 單價:{r['unit']} | {r['date']}"
        for r in lvr
    ) if lvr else "_無資料_"

    summary = call_deepseek(f"""你是台灣房地產市場分析師。今天是 {date_str}。

以下是台灣房市最新資訊：

【591 最新掛牌/新聞】
{listings_text}

【內政部實價登錄 ({season}) 近期高總價成交】
{lvr_text}

請提供：
1. 目前台灣房市整體趨勢（2-3行）
2. 值得注意的地區或物件類型
3. 對自住或投資者的建議

繁體中文，3-5個重點，簡潔具體。""", max_tokens=600, temperature=0.4)

    listings_md = "\n".join(f"- [{l['title']}]({l['url']})" for l in listings)
    lvr_md = "\n".join(
        f"| {r['addr']} | {r['type']} | {r['area']} | {r['price']} | {r['unit']} |"
        for r in lvr
    )

    raw_md = f"### AI 分析\n{summary}\n\n### 591 最新\n{listings_md}"
    if lvr:
        raw_md += (f"\n\n### 實價登錄 ({season}) 近期成交\n"
                   f"| 地址 | 類型 | 面積 | 總價 | 單價 |\n|---|---|---|---|---|\n{lvr_md}")

    write_output(TOPIC, HEADING, summary, raw_md)


if __name__ == "__main__":
    run()
