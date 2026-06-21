#!/usr/bin/env python3
"""Learning Photography — daily rotating photography concept. Cron: 8:40 AM Taipei"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import random
import config as cfg
from sources.lib import call_deepseek, load_state, save_state, write_output

TOPIC   = "learning_photography"
HEADING = "## 📷 Learning — Photography"


def get_concept(state):
    queue = state.get("photography_queue", [])
    last  = state.get("photography_last")
    if not queue:
        shuffled = cfg.PHOTOGRAPHY_CONCEPTS[:]
        random.shuffle(shuffled)
        if last and shuffled[0] == last and len(shuffled) > 1:
            shuffled[0], shuffled[1] = shuffled[1], shuffled[0]
        queue = shuffled
    concept = queue.pop(0)
    state["photography_queue"] = queue
    state["photography_last"]  = concept
    return concept


def run():
    state, state_file = load_state()
    concept = get_concept(state)
    print(f"[learning_photography] Concept: {concept}")

    # Strip the [Category] tag for cleaner prompt
    clean = concept.split("[")[0].strip()

    lesson = call_deepseek(f"""You are a professional photographer and educator. The user shoots with a Sony A7C and is interested in portrait, street, landscape, and cinematic video.

Today's concept: {clean}

Explain it practically:
**What it is:** [2 sentences — what this technique/concept is]
**Why it matters:** [1-2 sentences — the visual impact or practical benefit]
**How to apply it:** [3-5 numbered steps, specific and actionable]
**Sony A7C tip:** [one specific setting, menu item, or lens recommendation relevant to this concept, if applicable — skip if not relevant]
**Common mistake:** [one mistake beginners make and how to avoid it]

Under 250 words. Concrete, visual, and practical.""", max_tokens=500, temperature=0.4)

    summary = f"Today's concept: {clean}\n{lesson}"
    raw_md  = f"### 📷 Today's Concept: {clean}\n\n{lesson}"

    save_state(state, state_file)
    write_output(TOPIC, HEADING, summary, raw_md)


if __name__ == "__main__":
    run()
