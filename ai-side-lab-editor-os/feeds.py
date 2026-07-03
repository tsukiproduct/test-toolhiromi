# -*- coding: utf-8 -*-
"""
AI SIDE LAB Editor OS — RSSソース定義
すべて無料で取得できる公式RSS / Atomフィード。
weight: ソース信頼度（スコアリングに使用、1.0が基準）
lang:   ja / en（表示バッジと初心者スコアに影響）
"""

FEEDS = [
    # ── 公式ブログ（一次情報・最重要）──
    {"name": "OpenAI News",        "url": "https://openai.com/news/rss.xml",                          "cat": "official", "weight": 1.5, "lang": "en"},
    {"name": "Anthropic News",     "url": "https://www.anthropic.com/rss.xml",                        "cat": "official", "weight": 1.5, "lang": "en"},
    {"name": "Google AI Blog",     "url": "https://blog.google/technology/ai/rss/",                   "cat": "official", "weight": 1.4, "lang": "en"},
    {"name": "DeepMind Blog",      "url": "https://deepmind.google/blog/rss.xml",                     "cat": "official", "weight": 1.4, "lang": "en"},
    {"name": "Microsoft AI Blog",  "url": "https://blogs.microsoft.com/ai/feed/",                     "cat": "official", "weight": 1.3, "lang": "en"},
    {"name": "Hugging Face Blog",  "url": "https://huggingface.co/blog/feed.xml",                     "cat": "official", "weight": 1.3, "lang": "en"},
    {"name": "Stability AI",       "url": "https://stability.ai/news?format=rss",                     "cat": "official", "weight": 1.2, "lang": "en"},

    # ── テックメディア ──
    {"name": "TechCrunch AI",      "url": "https://techcrunch.com/category/artificial-intelligence/feed/", "cat": "media", "weight": 1.2, "lang": "en"},
    {"name": "VentureBeat AI",     "url": "https://venturebeat.com/category/ai/feed/",                "cat": "media", "weight": 1.1, "lang": "en"},
    {"name": "The Verge AI",       "url": "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml", "cat": "media", "weight": 1.1, "lang": "en"},
    {"name": "MIT Tech Review",    "url": "https://www.technologyreview.com/feed/",                   "cat": "media", "weight": 1.1, "lang": "en"},

    # ── 日本語メディア（初心者向けスコアが上がりやすい）──
    {"name": "ITmedia AI+",        "url": "https://rss.itmedia.co.jp/rss/2.0/aiplus.xml",             "cat": "media_ja", "weight": 1.2, "lang": "ja"},
    {"name": "ASCII AI",           "url": "https://ascii.jp/rss.xml",                                 "cat": "media_ja", "weight": 0.9, "lang": "ja"},
    {"name": "Ledge.ai",           "url": "https://ledge.ai/feed/",                                   "cat": "media_ja", "weight": 1.1, "lang": "ja"},
    {"name": "Zenn AI",            "url": "https://zenn.dev/topics/ai/feed",                          "cat": "dev_ja",   "weight": 1.0, "lang": "ja"},
    {"name": "Qiita 生成AI",       "url": "https://qiita.com/tags/生成ai/feed",                        "cat": "dev_ja",   "weight": 0.9, "lang": "ja"},

    # ── コミュニティ / トレンド ──
    {"name": "HackerNews AI",      "url": "https://hnrss.org/newest?q=AI+OR+LLM&points=100",          "cat": "community", "weight": 1.0, "lang": "en"},
    {"name": "r/StableDiffusion",  "url": "https://www.reddit.com/r/StableDiffusion/top/.rss?t=day",  "cat": "community", "weight": 0.9, "lang": "en"},
    {"name": "r/LocalLLaMA",       "url": "https://www.reddit.com/r/LocalLLaMA/top/.rss?t=day",       "cat": "community", "weight": 0.9, "lang": "en"},
    {"name": "Product Hunt",       "url": "https://www.producthunt.com/feed",                         "cat": "product",  "weight": 0.9, "lang": "en"},
]
