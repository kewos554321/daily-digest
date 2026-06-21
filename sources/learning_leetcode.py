#!/usr/bin/env python3
"""Learning LeetCode — Blind 100 rotation + daily challenge note. Cron: 8:40 AM Taipei"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import json
import random
import urllib.request
import config as cfg
from sources.lib import call_deepseek, load_state, save_state, write_output, skip

TOPIC   = "learning_leetcode"
HEADING = "## 🧩 LeetCode Blind 100"

GRAPHQL_URL = "https://leetcode.com/graphql"
DAILY_QUERY = """
query {
  activeDailyCodingChallengeQuestion {
    date
    link
    question { questionId title difficulty topicTags { name } }
  }
}
"""


# ── Blind 100 rotation ────────────────────────────────────────────────────────

def get_blind_problem(state):
    queue = state.get("leetcode_queue", [])
    last  = state.get("leetcode_last")
    if not queue:
        shuffled = cfg.LEETCODE_BLIND100[:]
        random.shuffle(shuffled)
        if last and shuffled[0] == last and len(shuffled) > 1:
            shuffled[0], shuffled[1] = shuffled[1], shuffled[0]
        queue = shuffled
    problem = queue.pop(0)
    state["leetcode_queue"] = queue
    state["leetcode_last"]  = problem
    return problem


# ── LeetCode daily challenge (bonus reference) ────────────────────────────────

def fetch_daily():
    try:
        payload = json.dumps({"query": DAILY_QUERY}).encode()
        req = urllib.request.Request(
            GRAPHQL_URL,
            data=payload,
            headers={
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0",
                "Referer": "https://leetcode.com",
            },
        )
        with urllib.request.urlopen(req, timeout=20) as r:
            data = json.loads(r.read())
        d = data["data"]["activeDailyCodingChallengeQuestion"]
        q = d["question"]
        tags = ", ".join(t["name"] for t in q.get("topicTags", []))
        return (f"#{q['questionId']} {q['title']} [{q['difficulty']}]"
                f" — Tags: {tags} — https://leetcode.com{d['link']}")
    except Exception as e:
        print(f"  Daily challenge fetch error: {e}")
        return None


# ── Main ──────────────────────────────────────────────────────────────────────

def run():
    state, state_file = load_state()
    problem = get_blind_problem(state)
    print(f"[learning_leetcode] Blind 100 problem: {problem}")

    # Parse "number. Title [Category]" for the URL slug
    try:
        num = problem.split(".")[0].strip()
        lc_url = f"https://leetcode.com/problems/{problem.split('.')[1].strip().split('[')[0].strip().lower().replace(' ', '-')}/"
    except Exception:
        num, lc_url = "?", "https://leetcode.com/problemset/"

    daily_note = fetch_daily()
    daily_line = f"\n> 📅 **Today's Daily Challenge:** {daily_note}" if daily_note else ""

    lesson = call_deepseek(f"""You are a competitive programming coach. The user does LeetCode contests using Python3 and is studying the Blind 75 / NeetCode 150 list.

Today's focus problem:
{problem}
Link: {lc_url}

Provide a complete contest-ready breakdown:

**Problem Type:** [pattern / technique]
**Key Insight:** [the core observation, 1-2 sentences]
**Approach:** [numbered steps]
**Python3 Solution:**
```python
# Clean, efficient Python3 — optimized for contest speed
```
**Complexity:** Time O(...) | Space O(...)
**Blind 100 Note:** [why this problem is on the list, what pattern it represents, similar problems to practice]
**Contest Tips:** [edge cases, Python-specific tricks, common mistakes]

Be concise and practical.""", max_tokens=1000, temperature=0.3)

    summary = f"Blind 100: {problem}\n{lc_url}{daily_line}\n\n{lesson}"
    raw_md  = (
        f"### 🧩 Blind 100 — {problem}\n"
        f"**連結:** {lc_url}{daily_line}\n\n"
        f"{lesson}"
    )

    save_state(state, state_file)
    write_output(TOPIC, HEADING, summary, raw_md)


if __name__ == "__main__":
    run()
