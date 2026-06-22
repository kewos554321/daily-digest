---
name: line-structured-digest
description: Replace single-sentence LINE notification with a structured per-category mini daily report
metadata:
  type: project
---

# LINE Structured Digest — Design Spec

## Problem

The existing LINE notification sends a single sentence in Traditional Chinese plus a GitHub link. Reading the full digest required clicking through to GitHub every day.

## Solution

Replace the one-liner with a structured mini daily report that shows one line of highlights per category, directly readable in LINE without leaving the app.

## Output Format

```
📋 Daily Digest — 2026-06-22

💻 Tech  Claude 4 釋出新 API，支援更長 context window
📈 Finance  台積電 ▲1.2%，S&P 500 小幅回落
🌍 News  G7 峰會聚焦 AI 監管框架
✈️ Savings  Sony A7C II 二手優惠出現在 r/photomarket
📚 Learning  LeetCode #300 最長遞增子序列；EV/EBITDA 計算與應用
🛂 Immigration  491 邀請門檻降至 70 分

🔗 https://github.com/.../2026-06-22-xxx.md
```

- Each line: `{emoji} {Category}  {≤50 字 繁中摘要}`
- Sections within the same category (e.g. `learning_leetcode` + `learning_finance`) are merged into one line
- GitHub link preserved at the bottom

## Implementation

**File changed: `aggregate.py` only.**

### Added: `CATEGORY_EMOJI` module-level dict
Maps category prefix → display label with emoji. Replaces the duplicate `CATEGORY_LABELS` dict that was previously defined inside `compile_markdown`.

### Added: `generate_line_digest(sections)`
- Groups sections by category prefix
- Sends one DeepSeek call (max_tokens=400) to generate all category lines at once
- Fallback on API failure: plain `{emoji}  今日資料已整理` per category

### Removed: `generate_line_highlight(sections)`
Single-sentence generator replaced entirely.

### Updated: `main()` message assembly
```python
message = f"📋 Daily Digest — {date_str}\n\n{line_digest}\n\n🔗 {github_link}"
```

## Cost Impact

No change in DeepSeek call count (was 1 call for line highlight, still 1 call). Token usage increases slightly (~150 → ~400 output tokens for the line digest).

## Constraints

- LINE text message max: 5000 characters. A 6-category digest is well within limits.
- No changes to GitHub Actions workflow, other source scripts, or Obsidian output.
