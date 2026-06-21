#!/usr/bin/env python3
"""Learning Tech — daily rotating software engineering concept. Cron: TBD"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import random
import config as cfg
from sources.lib import call_deepseek, load_state, save_state, write_output

TOPIC   = "learning_tech"
HEADING = "## 📚 Learning — Tech"


def get_concept(state):
    queue = state.get("tech_queue", [])
    last  = state.get("tech_last")
    if not queue:
        shuffled = cfg.TECH_CONCEPTS[:]
        random.shuffle(shuffled)
        if last and shuffled[0] == last and len(shuffled) > 1:
            shuffled[0], shuffled[1] = shuffled[1], shuffled[0]
        queue = shuffled
    concept = queue.pop(0)
    state["tech_queue"] = queue
    state["tech_last"]  = concept
    return concept


def run():
    state, state_file = load_state()
    concept = get_concept(state)
    print(f"[learning_tech] Concept: {concept}")

    lesson = call_deepseek(f"""You are a senior software engineer. Explain this concept concisely:

Concept: {concept}

Structure:
What it is: [2 sentences]
When to use it: [1-2 sentences with real-world scenario]
Example: [short code snippet or concrete example]
Gotcha: [one common mistake or misconception]

Under 200 words. Practical and direct. English.""", max_tokens=400, temperature=0.4)

    summary = f"Today's concept: {concept}\n{lesson}"
    raw_md  = f"### 📚 Today's Concept: {concept}\n\n{lesson}"

    save_state(state, state_file)
    write_output(TOPIC, HEADING, summary, raw_md)


if __name__ == "__main__":
    run()
