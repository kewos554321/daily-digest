#!/usr/bin/env python3
"""Learning Finance — daily rotating finance concept. Cron: 8:50 AM Taipei"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import random
import config as cfg
from sources.lib import call_deepseek, load_state, save_state, write_output

TOPIC   = "learning_finance"
HEADING = "## 📚 Learning — Finance"


def get_concept(state):
    queue = state.get("finance_queue", [])
    last  = state.get("finance_last")
    if not queue:
        shuffled = cfg.FINANCE_CONCEPTS[:]
        random.shuffle(shuffled)
        if last and shuffled[0] == last and len(shuffled) > 1:
            shuffled[0], shuffled[1] = shuffled[1], shuffled[0]
        queue = shuffled
    concept = queue.pop(0)
    state["finance_queue"] = queue
    state["finance_last"]  = concept
    return concept


def run():
    state, state_file = load_state()
    concept = get_concept(state)
    print(f"[learning_finance] Concept: {concept}")

    lesson = call_deepseek(f"""You are a finance educator. Explain this concept for a software engineer learning stock analysis:

Concept: {concept}

Plain text, no markdown headers. Structure:
What it is: [2 sentences]
Why it matters: [1-2 sentences, practical use]
Example: [worked example with realistic numbers]
Rule of thumb: [one actionable insight or warning sign]

Under 200 words. Concrete and specific.""", max_tokens=400, temperature=0.4)

    summary = f"Today's concept: {concept}\n{lesson}"
    raw_md  = f"### 📚 Today's Concept: {concept}\n\n{lesson}"

    save_state(state, state_file)
    write_output(TOPIC, HEADING, summary, raw_md)


if __name__ == "__main__":
    run()
