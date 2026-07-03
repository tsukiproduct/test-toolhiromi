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
    # ---- 2026-07 verified additions (HTTP 200 / feedparser ok / updated within 90 days) ----
    {"name": "Ars Technica AI",          "url": "https://arstechnica.com/tag/artificial-intelligence/feed/", "cat": "media",     "weight": 1.2, "lang": "en"},
    {"name": "The Decoder",             "url": "https://the-decoder.com/feed/",                         "cat": "media",     "weight": 1.1, "lang": "en"},
    {"name": "Ben's Bites",             "url": "https://www.bensbites.com/feed",                       "cat": "media",     "weight": 1.0, "lang": "en"},
    {"name": "TLDR AI",                 "url": "https://tldr.tech/api/rss/ai",                         "cat": "media",     "weight": 1.0, "lang": "en"},
    {"name": "Simon Willison Weblog",   "url": "https://simonwillison.net/atom/everything/",            "cat": "community", "weight": 1.0, "lang": "en"},
    {"name": "arXiv cs.AI",             "url": "https://export.arxiv.org/api/query?search_query=cat:cs.AI&sortBy=submittedDate&sortOrder=descending&max_results=25", "cat": "official", "weight": 1.3, "lang": "en"},
    {"name": "arXiv cs.CL",             "url": "https://export.arxiv.org/api/query?search_query=cat:cs.CL&sortBy=submittedDate&sortOrder=descending&max_results=25", "cat": "official", "weight": 1.3, "lang": "en"},
    {"name": "Google News 生成AI",       "url": "https://news.google.com/rss/search?q=%E7%94%9F%E6%88%90AI&hl=ja&gl=JP&ceid=JP:ja", "cat": "media_ja", "weight": 1.0, "lang": "ja"},
    {"name": "AINOW",                   "url": "https://ainow.ai/feed/",                              "cat": "media_ja", "weight": 1.1, "lang": "ja"},
    {"name": "GIGAZINE",                "url": "https://gigazine.net/news/rss_2.0/",                   "cat": "media_ja", "weight": 1.0, "lang": "ja"},
    {"name": "Publickey",               "url": "https://www.publickey1.jp/atom.xml",                   "cat": "dev_ja",   "weight": 1.0, "lang": "ja"},
    {"name": "PC Watch",                "url": "https://pc.watch.impress.co.jp/data/rss/1.0/pcw/feed.rdf", "cat": "media_ja", "weight": 1.0, "lang": "ja"},
    {"name": "はてブ テクノロジー人気", "url": "https://b.hatena.ne.jp/hotentry/it.rss",               "cat": "community", "weight": 0.9, "lang": "ja"},
    {"name": "note AI hashtag",         "url": "https://note.com/hashtag/AI/rss",                     "cat": "community", "weight": 0.8, "lang": "ja"},
    {"name": "AWS Machine Learning Blog","url": "https://aws.amazon.com/blogs/machine-learning/feed/",  "cat": "official",  "weight": 1.4, "lang": "en"},
    {"name": "GitHub AI and ML Blog",   "url": "https://github.blog/ai-and-ml/feed/",                  "cat": "official",  "weight": 1.3, "lang": "en"},
    {"name": "Replicate Blog",          "url": "https://replicate.com/blog/rss",                       "cat": "product",   "weight": 1.0, "lang": "en"},
    {"name": "Cloudflare AI Blog",      "url": "https://blog.cloudflare.com/tag/ai/rss/",              "cat": "official",  "weight": 1.3, "lang": "en"},
    {"name": "Machine Learning Mastery", "url": "https://machinelearningmastery.com/feed/",            "cat": "media",     "weight": 1.0, "lang": "en"},
    {"name": "Hacker News LLM",         "url": "https://hnrss.org/newest?q=LLM&points=50",             "cat": "community", "weight": 0.9, "lang": "en"},
]
