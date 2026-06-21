#!/usr/bin/env python3
"""Learning YouTube — daily rotating YT content creation concept. Cron: 8:40 AM Taipei"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import random
import config as cfg
from sources.lib import call_deepseek, load_state, save_state, write_output

TOPIC   = "learning_youtube"
HEADING = "## 🎬 Learning — YouTube"


def get_concept(state):
    queue = state.get("youtube_queue", [])
    last  = state.get("youtube_last")
    if not queue:
        shuffled = cfg.YOUTUBE_CONCEPTS[:]
        random.shuffle(shuffled)
        if last and shuffled[0] == last and len(shuffled) > 1:
            shuffled[0], shuffled[1] = shuffled[1], shuffled[0]
        queue = shuffled
    concept = queue.pop(0)
    state["youtube_queue"] = queue
    state["youtube_last"]  = concept
    return concept


def run():
    state, state_file = load_state()
    concept = get_concept(state)
    print(f"[learning_youtube] Concept: {concept}")

    clean    = concept.split("[")[0].strip()
    category = concept.split("[")[1].replace("]", "").strip() if "[" in concept else ""

    lesson = call_deepseek(f"""你是一位 YouTube 頻道顧問，同時也是影片製作教練。使用者剛開始經營 YouTube，使用 Sony A7C 拍攝，對剪輯不熟悉，想試試 AI 剪輯工具，頻道方向考慮攝影 Vlog、旅遊、科技開箱或生活日常。

今日主題：{clean}
類別：{category}

請用繁體中文說明，結構如下：

**是什麼：** [2 句話解釋這個概念]
**為什麼重要：** [1-2 句話，對初學 YouTuber 的實際影響]
**怎麼做：** [3-5 個具體可執行步驟]
**新手常犯的錯：** [1 個常見錯誤與如何避免]
**延伸 idea：** [1 個可以直接拍的影片點子，符合攝影/旅遊/科技/生活方向]

250 字以內。具體、實用、針對剛起步的創作者。""", max_tokens=600, temperature=0.5)

    summary = f"今日主題：{clean}\n{lesson}"
    raw_md  = f"### 🎬 今日主題：{clean}\n**類別：** {category}\n\n{lesson}"

    save_state(state, state_file)
    write_output(TOPIC, HEADING, summary, raw_md)


if __name__ == "__main__":
    run()
