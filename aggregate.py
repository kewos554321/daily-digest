#!/usr/bin/env python3
"""
Aggregate — reads today's section outputs, compiles one .md, pushes to obsidian-note-openclaw/inbox, sends LINE.
Cron: 9:00 AM Taipei
"""

import os
import json
import subprocess
import urllib.request
import urllib.parse
from datetime import datetime
import config as cfg

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")


# ── Helpers ───────────────────────────────────────────────────────────────────

def call_deepseek(prompt, max_tokens=2000, temperature=0.3):
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


def load_today_outputs(date_str):
    """Read all output JSON files for today. Returns list of section dicts."""
    if not os.path.exists(OUTPUT_DIR):
        return []
    sections = []
    for fname in sorted(os.listdir(OUTPUT_DIR)):
        if fname.startswith(date_str) and fname.endswith(".json"):
            path = os.path.join(OUTPUT_DIR, fname)
            try:
                with open(path, encoding="utf-8") as f:
                    sections.append(json.load(f))
                print(f"  Loaded: {fname}")
            except Exception as e:
                print(f"  Failed to load {fname}: {e}")
    return sections


# ── Compile ───────────────────────────────────────────────────────────────────

def generate_highlights(sections):
    """Ask AI for top highlights across all sections."""
    combined = "\n\n".join(
        f"=== {s['heading'].upper()} ===\n{s['summary']}"
        for s in sections
    )
    return call_deepseek(f"""You are a personal daily briefing assistant for a Taiwanese software engineer.
Interests: tech/AI, stock fundamentals, world news, travel (Japan/Thailand/Europe/Australia/Egypt),
camera & diving gear deals in Taiwan, Australia immigration.

From today's digest sections, write:

## 🔥 今日重點 Top Highlights
3-5 bullets — the most important or actionable things across ALL sections today.
Include links where available. English or Traditional Chinese OK.

Then add one line per section that was included today, as a quick status:
- 💻 Tech: [one-line summary]
- 📈 Markets: [one-line summary]
- ... (only sections that exist in the input)

Data:
{combined}""", max_tokens=1000)


def generate_line_highlight(sections):
    """ONE sentence in Traditional Chinese — the single most interesting thing today."""
    combined = "\n".join(f"[{s['topic']}] {s['summary'][:300]}" for s in sections)
    try:
        return call_deepseek(
            f"從今日摘要中，挑出對台灣軟體工程師最值得關注的一件事。"
            f"只回覆一句繁體中文，最多60字，開頭加相關emoji。\n\n{combined}",
            max_tokens=80, temperature=0.5
        )
    except Exception:
        return "📋 今日摘要已整理完成"


def compile_markdown(date_str, highlights, sections):
    topics = [s["topic"] for s in sections]
    frontmatter = (
        f"---\ndate: {date_str}\ntags: [daily-digest, automated]\n"
        f"sections: {json.dumps(topics)}\n---"
    )

    # Table of contents
    toc_items = "\n".join(
        f"- {s['heading'].lstrip('#').strip()}" for s in sections
    )
    toc = f"**今日涵蓋 Sections：**\n{toc_items}"

    CATEGORY_LABELS = {
        "tech":        "💻 Tech",
        "finance":     "📈 Finance",
        "news":        "🌍 News",
        "savings":     "✈️ Savings",
        "learning":    "📚 Learning",
        "immigration": "🛂 Immigration",
    }

    # Detailed section content — grouped by category, full raw_md per section
    detail_parts = []
    current_cat = None
    for s in sections:
        cat = next((c for c in CATEGORY_LABELS if s["topic"].startswith(c)), None)
        if cat != current_cat:
            current_cat = cat
            label = CATEGORY_LABELS.get(cat, cat.title())
            detail_parts.append(f"## {label}")
        ts = s.get("generated_at", "")
        ts_line = f"\n> `{ts}`" if ts else ""
        heading = s["heading"].replace("## ", "### ", 1)
        raw_md  = s["raw_md"].replace("### ", "#### ")
        detail_parts.append(f"{heading}{ts_line}\n\n{raw_md}")
    section_details = "\n\n".join(detail_parts)

    return f"""{frontmatter}

# Daily Digest — {date_str}

{toc}

---

{highlights}

---

{section_details}
"""


def generate_slug(sections):
    tech = next((s for s in sections if s["topic"] == "tech_ai"), None)
    if not tech:
        return "daily-digest"
    try:
        slug = call_deepseek(
            "Based on this text, generate a 3-5 word slug for today's theme. "
            "Lowercase, hyphens only. Reply with ONLY the slug.\n\n" + tech["summary"][:500],
            max_tokens=20
        ).strip().lower()
        slug = "".join(c if c.isalnum() or c == "-" else "-" for c in slug)
        return "-".join(filter(None, slug.split("-")))[:50]
    except Exception:
        return "daily-digest"


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    now      = datetime.now(cfg.TZ)
    date_str = now.strftime("%Y-%m-%d")
    print(f"[{date_str}] Running aggregate...")

    sections = load_today_outputs(date_str)
    if not sections:
        print("No output files found for today. Nothing to aggregate.")
        return

    # Group sections by category prefix
    CATEGORY_ORDER = ["tech", "finance", "news", "savings", "learning", "immigration"]
    def section_sort_key(s):
        topic = s["topic"]
        for i, cat in enumerate(CATEGORY_ORDER):
            if topic.startswith(cat):
                return (i, topic)
        return (len(CATEGORY_ORDER), topic)
    sections.sort(key=section_sort_key)

    print(f"\nSections ready: {[s['topic'] for s in sections]}")

    print("\nGenerating highlights...")
    highlights = generate_highlights(sections)

    print("Generating LINE highlight...")
    line_msg = generate_line_highlight(sections)
    print(f"  {line_msg}")

    print("Generating slug...")
    slug = generate_slug(sections)

    print("Compiling markdown...")
    md_content = compile_markdown(date_str, highlights, sections)
    os.makedirs(cfg.OBSIDIAN_DIR, exist_ok=True)
    # Remove any existing digest for today before writing
    for old in os.listdir(cfg.OBSIDIAN_DIR):
        if old.startswith(date_str) and old.endswith(".md"):
            os.remove(os.path.join(cfg.OBSIDIAN_DIR, old))
            print(f"  Removed old: {old}")
    md_path = os.path.join(cfg.OBSIDIAN_DIR, f"{date_str}-{slug}.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"Saved: {md_path}")

    print("Pushing to obsidian-note-openclaw repo...")
    repo = cfg.OBSIDIAN_REPO
    cmds = [
        ["git", "-C", repo, "add", md_path],
        ["git", "-C", repo, "commit", "-m", f"digest: {date_str} {slug}"],
        ["git", "-C", repo, "push"],
    ]
    for cmd in cmds:
        r = subprocess.run(cmd, capture_output=True, text=True)
        label = " ".join(cmd[3:])
        print(f"  {label}: ok" if r.returncode == 0 else f"  {label} failed: {r.stderr.strip()}")

    print("Sending LINE notification...")
    github_link = (
        f"https://github.com/kewos554321/obsidian-note-openclaw/blob/main/inbox"
        f"/{date_str}-{slug}.md"
    )
    message = f"{line_msg}\n\n📁 {date_str} 完整摘要已推送至 obsidian-note-openclaw/inbox\n🔗 {github_link}"
    try:
        payload = json.dumps({
            "to": cfg.LINE_USER_ID,
            "messages": [{"type": "text", "text": message}],
        }).encode()
        req = urllib.request.Request(
            "https://api.line.me/v2/bot/message/push",
            data=payload,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {cfg.LINE_NOTIFY_TOKEN}",
            },
        )
        with urllib.request.urlopen(req, timeout=15) as r:
            result = json.loads(r.read())
        print("LINE sent." if result.get("message") == "ok" else f"LINE failed: {result}")
    except Exception as e:
        print(f"LINE failed: {e}")
    print("\nDone.")


if __name__ == "__main__":
    main()
