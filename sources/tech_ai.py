#!/usr/bin/env python3
"""Tech & AI — HN + HuggingFace + ArXiv. Cron: 7:50 AM Taipei"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import json
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import config as cfg
from sources.lib import call_deepseek, write_output, skip

TOPIC   = "tech_ai"
HEADING = "## 💻 Tech & AI"


def fetch_hn():
    try:
        with urllib.request.urlopen(
            "https://hacker-news.firebaseio.com/v0/topstories.json", timeout=15
        ) as r:
            ids = json.loads(r.read())[:100]
        stories = []
        for sid in ids:
            if len(stories) >= cfg.HN_LIMIT:
                break
            try:
                with urllib.request.urlopen(
                    f"https://hacker-news.firebaseio.com/v0/item/{sid}.json", timeout=10
                ) as r:
                    item = json.loads(r.read())
                if any(k in (item.get("title") or "").lower() for k in cfg.HN_KEYWORDS):
                    stories.append({"title": item.get("title",""),
                                    "url": item.get("url", f"https://news.ycombinator.com/item?id={sid}"),
                                    "score": item.get("score", 0)})
            except Exception:
                continue
        return stories
    except Exception as e:
        print(f"  HN error: {e}"); return []


def fetch_arxiv():
    try:
        q = urllib.parse.urlencode({
            "search_query": "cat:cs.AI OR cat:cs.LG OR cat:cs.CL",
            "start": 0, "max_results": cfg.ARXIV_LIMIT,
            "sortBy": "submittedDate", "sortOrder": "descending",
        })
        with urllib.request.urlopen(f"https://export.arxiv.org/api/query?{q}", timeout=15) as r:
            root = ET.fromstring(r.read())
        ns = {"a": "http://www.w3.org/2005/Atom"}
        return [{"title": e.find("a:title", ns).text.strip().replace("\n"," "),
                 "summary": e.find("a:summary", ns).text.strip().replace("\n"," ")[:300],
                 "url": e.find("a:id", ns).text.strip()}
                for e in root.findall("a:entry", ns)]
    except Exception as e:
        print(f"  ArXiv error: {e}"); return []


def fetch_hf():
    try:
        req = urllib.request.Request("https://huggingface.co/api/daily_papers",
                                     headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as r:
            data = json.loads(r.read())
        return [{"title": p.get("paper",{}).get("title",""),
                 "summary": p.get("paper",{}).get("summary","")[:300],
                 "url": f"https://huggingface.co/papers/{p.get('paper',{}).get('id','')}"}
                for p in data[:cfg.HF_LIMIT]]
    except Exception as e:
        print(f"  HuggingFace error: {e}"); return []


def run():
    print("[tech_ai] Fetching...")
    hn    = fetch_hn();    print(f"  HN: {len(hn)}")
    arxiv = fetch_arxiv(); print(f"  ArXiv: {len(arxiv)}")
    hf    = fetch_hf();    print(f"  HuggingFace: {len(hf)}")

    if not hn and not arxiv and not hf:
        skip(TOPIC, "all sources returned empty"); return

    # AI summary
    hn_text    = "\n".join(f"- [{s['score']}pts] {s['title']} ({s['url']})" for s in hn)
    hf_text    = "\n".join(f"- {p['title']}: {p['summary']} ({p['url']})" for p in hf)
    arxiv_text = "\n".join(f"- {p['title']}: {p['summary']} ({p['url']})" for p in arxiv)

    summary = call_deepseek(f"""Summarize today's AI/tech highlights for a software engineer.

HN:
{hn_text}

HuggingFace:
{hf_text}

ArXiv:
{arxiv_text}

Write 3-5 bullet points. Include links. English. Be concise.""", max_tokens=800)

    raw_md = (
        "### Hacker News\n" + "\n".join(f"- [{s['title']}]({s['url']}) ⭐{s['score']}" for s in hn) +
        "\n\n### HuggingFace\n" + "\n".join(f"- [{p['title']}]({p['url']})" for p in hf) +
        "\n\n### ArXiv\n" + "\n".join(f"- [{p['title']}]({p['url']})" for p in arxiv)
    )
    write_output(TOPIC, HEADING, summary, raw_md)


if __name__ == "__main__":
    run()
