"""
User configuration for daily digest.
Edit this file to add/remove topics, stocks, and preferences.
"""

import os
from datetime import timezone, timedelta

# ── Infrastructure ────────────────────────────────────────────────────────────
DEEPSEEK_API_KEY  = os.environ["DEEPSEEK_API_KEY"]
DEEPSEEK_BASE_URL = "https://api.deepseek.com/chat/completions"
FMP_API_KEY       = os.environ["FMP_API_KEY"]
FMP_BASE_URL      = "https://financialmodelingprep.com/stable"
LINE_NOTIFY_TOKEN = os.environ.get("LINE_NOTIFY_TOKEN", "")
OBSIDIAN_DIR      = os.environ.get("OBSIDIAN_DIR", "/root/Documents/obsidian-note-openclaw/inbox")
OBSIDIAN_REPO     = os.environ.get("OBSIDIAN_REPO", "/root/Documents/obsidian-note-openclaw")
TZ                = timezone(timedelta(hours=8))

# ── Section Toggles ───────────────────────────────────────────────────────────
# Set False to skip a section entirely.
SECTIONS = {
    # tech
    "tech_ai":           True,
    "tech_google":       True,
    "tech_ai_companies": True,   # OpenAI / Anthropic / Tesla
    "tech_news":         False,   # TODO: enable when ready
    "tech_product":    False,
    "tech_dev":        False,
    "tech_security":   False,
    "tech_devops":     False,
    "tech_opensource": False,
    "tech_career":     False,
    # finance
    "finance_markets":  True,
    "finance_stock":    True,
    "finance_screener":    True,
    "finance_realestate":  True,
    # learning
    "learning_finance":     True,
    "learning_leetcode":    True,
    "learning_tech":        True,
    "learning_photography": True,
    "learning_youtube":     True,
    # news
    "news_world":       True,
    # savings
    "savings_travel":   True,
    "savings_flight":   True,
    "savings_camera":   True,
    "savings_dive":     True,
    # immigration
    "immigration_au":   True,
}

# ── Stock Watchlist ───────────────────────────────────────────────────────────
# Format: (yahoo_symbol, display_name)
# Indices use ^ prefix (price only, no fundamentals).
# Individual stocks get full fundamental data + recent news.
# Taiwan stocks: "2330.TW", US stocks: "AAPL", "NVDA"
INDICES = [
    ("^GSPC", "S&P 500"),
    ("^TWII", "台股加權"),
    ("^N225", "日經 225"),
]

WATCHLIST = [
    # Taiwan AI stocks
    ("2330.TW", "台積電"),
    ("2454.TW", "聯發科"),
    ("3661.TW", "世芯-KY"),
    ("3035.TW", "智原"),
    ("2382.TW", "廣達"),
    ("2317.TW", "鴻海"),
    ("3231.TW", "緯創"),
    ("2356.TW", "英業達"),
    ("2308.TW", "台達電"),
    # US AI stocks
    ("NVDA",  "NVIDIA"),
    ("AMD",   "AMD"),
    ("MSFT",  "Microsoft"),
    ("GOOGL", "Google"),
    ("AMZN",  "Amazon"),
    ("META",  "Meta"),
    ("AVGO",  "Broadcom"),
    ("ARM",   "Arm Holdings"),
    ("PLTR",  "Palantir"),
    ("SMCI",  "Super Micro"),
    ("TSLA",  "Tesla"),
    ("VOO",   "Vanguard S&P 500 ETF"),
]

# ── Travel ────────────────────────────────────────────────────────────────────
TRAVEL_SUBREDDIT    = "solotravel"
TRAVEL_KEYWORDS     = [
    "japan", "thailand", "europe", "australia", "egypt",
    "paris", "london", "rome", "tokyo", "bangkok", "cairo",
    "deal", "flight", "cheap", "visa",
]
TRAVEL_DESTINATIONS = [
    "Japan (Tokyo, Osaka, Sapporo)",
    "Thailand (Bangkok, Chiang Mai)",
    "Europe (any major city)",
    "USA (West Coast or East Coast)",
    "Egypt (Cairo)",
    "Australia (Sydney, Melbourne)",
]

# ── Tech / AI ─────────────────────────────────────────────────────────────────
HN_KEYWORDS = {
    "ai", "llm", "gpt", "claude", "gemini", "openai", "anthropic",
    "machine learning", "deep learning", "neural", "transformer",
    "diffusion", "agent", "rag", "fine-tun",
}
HN_LIMIT     = 10
ARXIV_LIMIT  = 6
HF_LIMIT     = 6

# ── Gear ──────────────────────────────────────────────────────────────────────
# (subreddit, label, limit)
GEAR_SOURCES = [
    ("photomarket", "Camera Gear", 4),
    ("scuba",       "Diving Gear", 4),
]

# ── Australia Immigration ─────────────────────────────────────────────────────
AU_SUBREDDIT = "AusVisa"
AU_KEYWORDS  = [
    "visa", "pr", "permanent", "skilled", "migration",
    "189", "190", "491", "subclass", "points",
    "invitation", "eoi", "skillselect",
]
AU_LIMIT = 5

# ── LeetCode Blind 100 Rotation ───────────────────────────────────────────────
# Curated Blind 75 / NeetCode 150 problems for contest & interview prep.
# Format: "number. Title [Category]"
LEETCODE_BLIND100 = [
    # Arrays & Hashing
    "1. Two Sum [Arrays & Hashing]",
    "217. Contains Duplicate [Arrays & Hashing]",
    "242. Valid Anagram [Arrays & Hashing]",
    "49. Group Anagrams [Arrays & Hashing]",
    "347. Top K Frequent Elements [Arrays & Hashing]",
    "238. Product of Array Except Self [Arrays & Hashing]",
    "128. Longest Consecutive Sequence [Arrays & Hashing]",
    # Two Pointers
    "125. Valid Palindrome [Two Pointers]",
    "15. 3Sum [Two Pointers]",
    "11. Container With Most Water [Two Pointers]",
    "42. Trapping Rain Water [Two Pointers]",
    # Sliding Window
    "121. Best Time to Buy and Sell Stock [Sliding Window]",
    "3. Longest Substring Without Repeating Characters [Sliding Window]",
    "424. Longest Repeating Character Replacement [Sliding Window]",
    "567. Permutation in String [Sliding Window]",
    "76. Minimum Window Substring [Sliding Window]",
    "239. Sliding Window Maximum [Sliding Window]",
    # Stack
    "20. Valid Parentheses [Stack]",
    "155. Min Stack [Stack]",
    "150. Evaluate Reverse Polish Notation [Stack]",
    "22. Generate Parentheses [Stack]",
    "739. Daily Temperatures [Stack]",
    "84. Largest Rectangle in Histogram [Stack]",
    # Binary Search
    "704. Binary Search [Binary Search]",
    "74. Search a 2D Matrix [Binary Search]",
    "875. Koko Eating Bananas [Binary Search]",
    "153. Find Minimum in Rotated Sorted Array [Binary Search]",
    "33. Search in Rotated Sorted Array [Binary Search]",
    "4. Median of Two Sorted Arrays [Binary Search]",
    # Linked List
    "206. Reverse Linked List [Linked List]",
    "21. Merge Two Sorted Lists [Linked List]",
    "143. Reorder List [Linked List]",
    "19. Remove Nth Node From End of List [Linked List]",
    "138. Copy List with Random Pointer [Linked List]",
    "2. Add Two Numbers [Linked List]",
    "141. Linked List Cycle [Linked List]",
    "146. LRU Cache [Linked List]",
    "23. Merge K Sorted Lists [Linked List]",
    "25. Reverse Nodes in K-Group [Linked List]",
    # Trees
    "226. Invert Binary Tree [Trees]",
    "104. Maximum Depth of Binary Tree [Trees]",
    "543. Diameter of Binary Tree [Trees]",
    "110. Balanced Binary Tree [Trees]",
    "100. Same Tree [Trees]",
    "572. Subtree of Another Tree [Trees]",
    "235. Lowest Common Ancestor of BST [Trees]",
    "102. Binary Tree Level Order Traversal [Trees]",
    "199. Binary Tree Right Side View [Trees]",
    "98. Validate Binary Search Tree [Trees]",
    "230. Kth Smallest Element in BST [Trees]",
    "105. Construct Binary Tree from Preorder and Inorder [Trees]",
    "124. Binary Tree Maximum Path Sum [Trees]",
    "297. Serialize and Deserialize Binary Tree [Trees]",
    # Tries
    "208. Implement Trie [Tries]",
    "211. Design Add and Search Words Data Structure [Tries]",
    "212. Word Search II [Tries]",
    # Heap / Priority Queue
    "703. Kth Largest Element in a Stream [Heap]",
    "1046. Last Stone Weight [Heap]",
    "973. K Closest Points to Origin [Heap]",
    "621. Task Scheduler [Heap]",
    "295. Find Median from Data Stream [Heap]",
    # Backtracking
    "78. Subsets [Backtracking]",
    "39. Combination Sum [Backtracking]",
    "46. Permutations [Backtracking]",
    "90. Subsets II [Backtracking]",
    "40. Combination Sum II [Backtracking]",
    "79. Word Search [Backtracking]",
    "131. Palindrome Partitioning [Backtracking]",
    "17. Letter Combinations of a Phone Number [Backtracking]",
    "51. N-Queens [Backtracking]",
    # Graphs
    "200. Number of Islands [Graphs]",
    "695. Max Area of Island [Graphs]",
    "417. Pacific Atlantic Water Flow [Graphs]",
    "994. Rotting Oranges [Graphs]",
    "207. Course Schedule [Graphs]",
    "210. Course Schedule II [Graphs]",
    "684. Redundant Connection [Graphs]",
    "323. Number of Connected Components in an Undirected Graph [Graphs]",
    "127. Word Ladder [Graphs]",
    # 1D Dynamic Programming
    "70. Climbing Stairs [1D DP]",
    "198. House Robber [1D DP]",
    "213. House Robber II [1D DP]",
    "5. Longest Palindromic Substring [1D DP]",
    "322. Coin Change [1D DP]",
    "152. Maximum Product Subarray [1D DP]",
    "139. Word Break [1D DP]",
    "300. Longest Increasing Subsequence [1D DP]",
    "416. Partition Equal Subset Sum [1D DP]",
    # 2D Dynamic Programming
    "62. Unique Paths [2D DP]",
    "1143. Longest Common Subsequence [2D DP]",
    "309. Best Time to Buy and Sell Stock with Cooldown [2D DP]",
    "518. Coin Change II [2D DP]",
    "72. Edit Distance [2D DP]",
    "312. Burst Balloons [2D DP]",
    # Greedy
    "53. Maximum Subarray [Greedy]",
    "55. Jump Game [Greedy]",
    "45. Jump Game II [Greedy]",
    "134. Gas Station [Greedy]",
    "678. Valid Parenthesis String [Greedy]",
    # Intervals
    "57. Insert Interval [Intervals]",
    "56. Merge Intervals [Intervals]",
    "435. Non-overlapping Intervals [Intervals]",
    "252. Meeting Rooms [Intervals]",
    "253. Meeting Rooms II [Intervals]",
    # Math & Geometry
    "48. Rotate Image [Math & Geometry]",
    "54. Spiral Matrix [Math & Geometry]",
    "73. Set Matrix Zeroes [Math & Geometry]",
    "50. Pow(x, n) [Math & Geometry]",
    # Bit Manipulation
    "136. Single Number [Bit Manipulation]",
    "191. Number of 1 Bits [Bit Manipulation]",
    "338. Counting Bits [Bit Manipulation]",
    "190. Reverse Bits [Bit Manipulation]",
    "268. Missing Number [Bit Manipulation]",
    "371. Sum of Two Integers [Bit Manipulation]",
]

# ── Finance Learning Rotation ─────────────────────────────────────────────────
# Concepts rotate in order, reshuffled when exhausted.
# Add any concept here to include it in the rotation.
# ── Tech Learning Rotation ────────────────────────────────────────────────────
TECH_CONCEPTS = [
    "CAP Theorem",
    "Event-Driven Architecture",
    "Database Indexing Strategies",
    "Consistent Hashing",
    "Rate Limiting Algorithms (Token Bucket, Leaky Bucket)",
    "Circuit Breaker Pattern",
    "CQRS and Event Sourcing",
    "gRPC vs REST vs GraphQL",
    "Distributed Transactions and the Saga Pattern",
    "Message Queues (Kafka vs RabbitMQ)",
    "Kubernetes Pod Scheduling",
    "Blue-Green vs Canary Deployments",
    "OAuth 2.0 and JWT internals",
    "Database Connection Pooling",
    "Caching Strategies (Cache-aside, Write-through, Write-back)",
    "Vector Databases and Embeddings",
    "LLM RAG Architecture",
    "Observability: Metrics, Logs, Traces",
    "Zero-downtime Database Migrations",
    "API Versioning Strategies",
]

# ── YouTube Learning Rotation ─────────────────────────────────────────────────
YOUTUBE_CONCEPTS = [
    # 腳本寫作
    "Script — Hook 開場的 3 種公式：問題、衝突、反直覺陳述 [腳本]",
    "Script — 影片結構：開場 / 中段 / CTA 的黃金比例 [腳本]",
    "Script — 如何用一句話定義影片核心訊息 [腳本]",
    "Script — 說故事結構：英雄旅程套用在 Vlog [腳本]",
    "Script — 轉場口播技巧：如何讓觀眾一直看下去 [腳本]",
    "Script — 撰寫標題與縮圖文字的一致性邏輯 [腳本]",
    "Script — 如何在 60 秒內完成完整 Short 腳本 [腳本]",
    "Script — 口語化腳本 vs 逐字稿的選擇時機 [腳本]",
    # AI 剪輯工具
    "AI 剪輯 — CapCut AI 自動字幕與一鍵剪輯功能教學 [AI剪輯]",
    "AI 剪輯 — Descript：用文字編輯影片的工作流程 [AI剪輯]",
    "AI 剪輯 — Runway Gen-2：AI 生成 B-Roll 補足畫面 [AI剪輯]",
    "AI 剪輯 — Adobe Premiere Auto Reframe 與 AI 語音降噪 [AI剪輯]",
    "AI 剪輯 — ElevenLabs AI 配音：製作旁白不需出鏡 [AI剪輯]",
    "AI 剪輯 — Topaz Video AI：低畫質素材升解析度 [AI剪輯]",
    "AI 剪輯 — ChatGPT 輔助腳本：從主題到逐字稿的流程 [AI剪輯]",
    "AI 剪輯 — VidIQ / TubeBuddy：AI SEO 標題與標籤建議 [AI剪輯]",
    # Filmora
    "Filmora — 介面導覽與基本剪輯工作流程 [Filmora]",
    "Filmora — AI 自動字幕與字幕樣式設計 [Filmora]",
    "Filmora — AI 降噪與人聲增強功能 [Filmora]",
    "Filmora — 色彩校正：LUT 套用與 Color Wheels 使用 [Filmora]",
    "Filmora — 轉場效果的選擇與克制使用原則 [Filmora]",
    "Filmora — 關鍵影格動畫：標題與圖層動態效果 [Filmora]",
    "Filmora — 分割螢幕與多畫面排版 [Filmora]",
    "Filmora — 音樂與音效庫：免版權素材直接使用 [Filmora]",
    "Filmora — 匯出設定：YouTube 最佳解析度與碼率 [Filmora]",
    "Filmora — AI 文字轉影片（Text to Video）功能試玩 [Filmora]",
    # 攝影 Vlog
    "攝影Vlog — 如何用 Sony A7C 拍出 Cinematic Vlog 感 [攝影Vlog]",
    "攝影Vlog — 攝影 Vlog 的敘事結構：出發 / 拍攝 / 反思 [攝影Vlog]",
    "攝影Vlog — Behind the Shot：解析一張照片的拍攝決策 [攝影Vlog]",
    "攝影Vlog — Gear 開箱類攝影影片的腳本框架 [攝影Vlog]",
    "攝影Vlog — Photo Walk 影片：路線規劃與剪輯節奏 [攝影Vlog]",
    "攝影Vlog — 攝影後製直播 / 螢幕錄製教學影片的技巧 [攝影Vlog]",
    "攝影Vlog — 如何展示攝影作品集讓觀眾感興趣 [攝影Vlog]",
    # 旅遊內容
    "旅遊 — 旅遊影片的 3 幕結構：期待 / 現場 / 反思 [旅遊]",
    "旅遊 — 一個人旅遊 Vlog 的自拍技巧與腳架使用 [旅遊]",
    "旅遊 — 旅遊影片的 B-Roll 清單：到一個地方要拍什麼 [旅遊]",
    "旅遊 — 如何在旅途中快速剪輯發短影片 [旅遊]",
    "旅遊 — 旅遊頻道定位：背包客 vs 精緻旅遊 vs 本地探索 [旅遊]",
    "旅遊 — 旅遊縮圖設計：臉部表情 + 地標 + 文字公式 [旅遊]",
    "旅遊 — 旅遊 Vlog 的音樂選擇與版權注意事項 [旅遊]",
    "旅遊 — 日本 / 泰國 / 歐洲各地常見爆款旅遊影片分析 [旅遊]",
    # 科技開箱
    "開箱 — 科技開箱影片的 5 段腳本公式 [開箱]",
    "開箱 — 開箱燈光佈置：讓產品看起來像廣告的技巧 [開箱]",
    "開箱 — 如何用 Sony A7C 拍出質感開箱影片 [開箱]",
    "開箱 — 開箱影片的 Thumbnail 設計：對比 / 表情 / 文字 [開箱]",
    "開箱 — 評測 vs 開箱 vs 使用心得的定位差異 [開箱]",
    "開箱 — 開箱影片的 Amazon / 聯盟行銷 CTA 策略 [開箱]",
    "開箱 — 如何做「一個月後使用心得」系列追蹤影片 [開箱]",
    # 生活日常
    "生活 — Day in the Life 影片的腳本與節奏設計 [生活]",
    "生活 — 生活 Vlog 如何讓日常變得有趣且有觀看價值 [生活]",
    "生活 — Morning Routine / Night Routine 影片公式 [生活]",
    "生活 — 生活頻道如何建立個人品牌與辨識度 [生活]",
    "生活 — 如何拍「一個人生活」Vlog：獨居 / 自炊 / 日常 [生活]",
    "生活 — 生活 Vlog 的剪輯節奏：快切 vs 留白 [生活]",
    # 頻道策略
    "策略 — 頻道定位：如何找到你的 Niche [策略]",
    "策略 — 第一支影片要拍什麼：冷啟動策略 [策略]",
    "策略 — YouTube SEO：標題 / 描述 / 標籤 / 章節 [策略]",
    "策略 — Thumbnail 設計心理學：點擊率 CTR 優化 [策略]",
    "策略 — 上傳頻率 vs 影片品質的平衡策略 [策略]",
    "策略 — YouTube Analytics 解讀：觀看時長 / CTR / 流量來源 [策略]",
    "策略 — Shorts 與長影片的搭配策略 [策略]",
    "策略 — 社群媒體導流：IG / TikTok 與 YouTube 聯動 [策略]",
    "策略 — 如何做頻道競品分析找出內容缺口 [策略]",
    "策略 — 如何用第一個 1000 訂閱打基礎 [策略]",
    # 剪輯技術
    "剪輯 — J-Cut 和 L-Cut：讓影片剪輯流暢的技巧 [剪輯]",
    "剪輯 — 色彩校正 vs 色彩分級的差異與流程 [剪輯]",
    "剪輯 — 字幕設計：字型 / 位置 / 動畫風格 [剪輯]",
    "剪輯 — BGM 選擇與情緒匹配：免版權音樂來源 [剪輯]",
    "剪輯 — 音頻處理：人聲 EQ / 降噪 / 壓縮基礎 [剪輯]",
    "剪輯 — 轉場的克制使用：何時不要加特效 [剪輯]",
    "剪輯 — 4K 素材剪輯工作流程與代理檔設定 [剪輯]",
    "剪輯 — End Screen 和 Cards 的策略性放置 [剪輯]",
]

# ── Photography Learning Rotation ────────────────────────────────────────────
PHOTOGRAPHY_CONCEPTS = [
    # Portrait
    "Portrait — Shallow Depth of Field and Bokeh Control [Portrait]",
    "Portrait — Sony A7C Eye AF and Face Tracking Technique [Portrait]",
    "Portrait — Rembrandt Lighting Setup [Portrait]",
    "Portrait — Butterfly / Clamshell Lighting for Beauty Shots [Portrait]",
    "Portrait — Window Light and Natural Diffusion [Portrait]",
    "Portrait — Posing Techniques for Flattering Angles [Portrait]",
    "Portrait — Skin Tone Rendering and White Balance [Portrait]",
    "Portrait — Loop Lighting vs Split Lighting [Portrait]",
    # Street Photography
    "Street — Zone Focusing for Fast Candid Shots [Street]",
    "Street — Candid Shooting Mindset and Ethics [Street]",
    "Street — Reading Urban Light and Shadows [Street]",
    "Street — Shooting in Busy Environments without Detection [Street]",
    "Street — Lens Choice for Street: 28mm vs 35mm vs 50mm [Street]",
    "Street — Black & White Conversion for Street Impact [Street]",
    "Street — Layering and Depth in Street Compositions [Street]",
    # Landscape
    "Landscape — Golden Hour and Blue Hour Timing [Landscape]",
    "Landscape — Long Exposure with ND Filters [Landscape]",
    "Landscape — Focus Stacking for Maximum Sharpness [Landscape]",
    "Landscape — Hyperfocal Distance Explained [Landscape]",
    "Landscape — Foreground Interest and Depth [Landscape]",
    "Landscape — Shooting Waterfalls and Silky Water [Landscape]",
    "Landscape — Astro / Night Sky Photography Basics [Landscape]",
    "Landscape — GND Filter Usage for Exposure Balance [Landscape]",
    # Composition
    "Composition — Rule of Thirds in Practice [Composition]",
    "Composition — Leading Lines and Visual Flow [Composition]",
    "Composition — Frame within a Frame Technique [Composition]",
    "Composition — Negative Space and Minimalism [Composition]",
    "Composition — Symmetry and Reflections [Composition]",
    "Composition — Golden Ratio vs Rule of Thirds [Composition]",
    "Composition — Breaking the Rules Intentionally [Composition]",
    # Light
    "Light — Hard Light vs Soft Light Characteristics [Light]",
    "Light — Direction of Light: Front / Side / Back [Light]",
    "Light — Overcast Sky as a Natural Softbox [Light]",
    "Light — Histogram Reading and Expose to the Right [Light]",
    "Light — Dynamic Range and Avoiding Blown Highlights [Light]",
    "Light — Using Reflectors and Diffusers [Light]",
    # Exposure & Camera Settings
    "Exposure — The Exposure Triangle: Aperture, Shutter, ISO [Exposure]",
    "Exposure — Metering Modes: Spot vs Matrix vs Center-Weighted [Exposure]",
    "Exposure — Shutter Speed for Motion Freeze vs Blur [Exposure]",
    "Exposure — ISO Noise and Sony A7C High-ISO Performance [Exposure]",
    "Exposure — Aperture Priority vs Manual Mode in the Field [Exposure]",
    "Exposure — Exposure Compensation in Tricky Situations [Exposure]",
    # Sony A7C Specific
    "Sony A7C — S-Log2 vs S-Log3: When to Use Each [Sony A7C]",
    "Sony A7C — S-Cinetone Color Profile for Cinematic Look [Sony A7C]",
    "Sony A7C — IBIS In-Body Stabilization Tips and Limits [Sony A7C]",
    "Sony A7C — Custom Button Setup for Efficient Shooting [Sony A7C]",
    "Sony A7C — Silent Shooting and Anti-Distortion Shutter [Sony A7C]",
    "Sony A7C — Best Lens Pairings: FE 85mm, 50mm, 35mm, 24mm [Sony A7C]",
    "Sony A7C — 4K Video Settings and Overheating Management [Sony A7C]",
    "Sony A7C — AF Tracking Sensitivity and Subject Switch Settings [Sony A7C]",
    # Video / Cinematic Movement
    "Video — Gimbal Operation: Pan, Tilt, Follow Modes [Video]",
    "Video — IBIS + OIS Combo for Handheld Smoothness [Video]",
    "Video — Dolly Zoom (Vertigo Effect) Technique [Video]",
    "Video — B-Roll Strategy and Coverage Ratios [Video]",
    "Video — 180-Degree Shutter Rule for Natural Motion Blur [Video]",
    "Video — Rack Focus and Pull Focus Techniques [Video]",
    "Video — Tracking Shot vs Static Shot Storytelling [Video]",
    "Video — Audio Basics: On-Camera Mic vs External Recorder [Video]",
    # Post-Processing
    "Post — Lightroom RAW Editing Workflow [Post-Processing]",
    "Post — Color Grading with HSL and Tone Curves [Post-Processing]",
    "Post — Skin Retouching without Overdoing It [Post-Processing]",
    "Post — Creating a Consistent Personal Style / Preset [Post-Processing]",
    "Post — RAW vs JPEG: Pros and Cons in Practice [Post-Processing]",
    "Post — Noise Reduction: Lightroom AI vs Topaz DeNoise [Post-Processing]",
    "Post — LUT Application for Cinematic Color Grades [Post-Processing]",
    "Post — Sharpening and Clarity vs Texture [Post-Processing]",
    # Color Theory
    "Color — Complementary Colors in Photography [Color Theory]",
    "Color — Warm vs Cool Color Temperature Mood [Color Theory]",
    "Color — Color Grading for Skin Tones [Color Theory]",
    "Color — Teal and Orange Look: Why It Works [Color Theory]",
    "Color — Monochromatic Color Schemes in Visual Storytelling [Color Theory]",
    # Gear & Accessories
    "Gear — CPL Filter: How and When to Use It [Gear]",
    "Gear — ND Filter Strengths: 3-Stop vs 6-Stop vs 10-Stop [Gear]",
    "Gear — Tripod Selection: Weight, Head Type, Stability [Gear]",
    "Gear — Flash Photography: TTL vs Manual Mode [Gear]",
    "Gear — Speedlight vs Strobe for Location Portraits [Gear]",
    # Special Topics
    "Special — Macro Photography: Extension Tubes vs Macro Lens [Special]",
    "Special — Food and Product Still Life Lighting [Special]",
    "Special — Shooting Coffee and Beverages (Splash, Steam) [Special]",
    "Special — Underwater Housing and Wet Lenses Basics [Special]",
    "Special — Film Photography Aesthetic and Grain Simulation [Special]",
    "Special — Double Exposure: In-Camera vs Post [Special]",
]

# ── Finance Learning Rotation ─────────────────────────────────────────────────
# Concepts rotate in order, reshuffled when exhausted.
# Add any concept here to include it in the rotation.
FINANCE_CONCEPTS = [
    "Price-to-Earnings (P/E) Ratio",
    "Earnings Per Share (EPS)",
    "Revenue vs. Net Income",
    "Gross Margin and Operating Margin",
    "Free Cash Flow (FCF)",
    "Return on Equity (ROE)",
    "Debt-to-Equity Ratio",
    "Dividend Yield and Payout Ratio",
    "Enterprise Value (EV) and EV/EBITDA",
    "Price-to-Book (P/B) Ratio",
    "Beta and Volatility",
    "52-Week High/Low and Moving Averages",
    "Short Interest and Days to Cover",
    "Dollar-Cost Averaging (DCA)",
    "Market Capitalization tiers (Large/Mid/Small cap)",
    "Index Fund vs. ETF differences",
    "Bond yield and its inverse relationship with price",
    "The VIX (Fear Index)",
    "Sector rotation strategy",
    "How to read an earnings report",
]
