#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI SIDE LAB Editor OS — Phase 1: 収集 + 前処理（トークン消費ゼロ）

RSS取得 → 重複排除 → キーワード分類 → AI SIDE SCORE算出 → data/raw.json

実行: python3 fetch.py
"""
import json, re, hashlib, time
from datetime import datetime, timezone, timedelta
from pathlib import Path

import feedparser
from feeds import FEEDS

JST = timezone(timedelta(hours=9))
OUT = Path(__file__).parent / "data" / "raw.json"
MAX_AGE_HOURS = 72          # 直近3日分のみ
SUMMARY_LIMIT = 180         # 著作権配慮: 要約は180字まで + 必ず元記事リンク

# ────────────────────────────────────────────
# キーワード辞書（分類 & スコアリングの心臓部）
# ────────────────────────────────────────────
KW = {
    "beginner":  ["how to", "guide", "tutorial", "beginner", "getting started", "入門", "初心者",
                  "使い方", "始め方", "とは", "解説", "まとめ", "無料", "free"],
    "monetize":  ["monetize", "revenue", "income", "business", "pricing", "subscription", "api",
                  "副業", "収益", "稼ぐ", "マネタイズ", "ビジネス", "料金", "有料", "販売"],
    "buzz":      ["launch", "release", "announce", "new model", "breakthrough", "viral", "record",
                  "発表", "リリース", "公開", "新機能", "新モデル", "話題", "最新"],
    "note_fit":  ["explain", "compare", "review", "experience", "opinion", "analysis",
                  "比較", "レビュー", "体験", "考察", "検証", "感想"],
    "video_fit": ["video", "image", "generate", "demo", "showcase", "visual",
                  "動画", "画像", "生成", "デモ", "映像"],
    "tool":      ["tool", "app", "extension", "plugin", "workflow", "automation",
                  "ツール", "アプリ", "自動化", "拡張", "効率化"],
}

CATEGORY_RULES = [
    ("model",   ["gpt", "claude", "gemini", "llama", "model", "llm", "モデル", "新モデル"]),
    ("imggen",  ["image", "diffusion", "midjourney", "画像生成", "イラスト"]),
    ("vidgen",  ["video", "sora", "runway", "luma", "pika", "kling", "動画生成"]),
    ("tool",    KW["tool"]),
    ("biz",     KW["monetize"]),
    ("news",    []),  # フォールバック
]

def clean(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text or "")
    text = re.sub(r"\s+", " ", text).strip()
    return text

def kw_score(text: str, keys: list, cap: int = 5) -> int:
    """キーワードヒット数 → 0..cap"""
    t = text.lower()
    hits = sum(1 for k in keys if k in t)
    return min(hits, cap)

def classify(text: str) -> str:
    t = text.lower()
    for cat, keys in CATEGORY_RULES:
        if keys and any(k in t for k in keys):
            return cat
    return "news"

def side_score(text: str, weight: float, age_h: float, lang: str) -> dict:
    """AI SIDE SCORE: 各プラットフォーム適性を0-100で算出"""
    base = 50 + weight * 10
    recency = max(0, 15 - age_h / 6)          # 新しいほど+15まで
    b  = kw_score(text, KW["beginner"])
    m  = kw_score(text, KW["monetize"])
    bz = kw_score(text, KW["buzz"])
    nf = kw_score(text, KW["note_fit"])
    vf = kw_score(text, KW["video_fit"])
    ja_bonus = 6 if lang == "ja" else 0        # 日本語ソースは初心者/note適性UP

    def clamp(v): return int(max(20, min(99, v)))
    return {
        "note":     clamp(base + recency + nf * 6 + b * 4 + ja_bonus),
        "x":        clamp(base + recency + bz * 7 + vf * 3),
        "youtube":  clamp(base + recency + vf * 7 + bz * 3),
        "brain":    clamp(base + m * 8 + nf * 3),
        "monetize": clamp(base + m * 9 + bz * 2),
        "beginner": clamp(base + b * 8 + ja_bonus),
    }

def stars(v: int) -> int:
    """0-100 → 1-5"""
    return max(1, min(5, round(v / 20)))

def entry_time(e) -> datetime:
    for key in ("published_parsed", "updated_parsed"):
        t = getattr(e, key, None)
        if t:
            return datetime.fromtimestamp(time.mktime(t), tz=timezone.utc)
    return datetime.now(timezone.utc)

def main():
    seen, articles = set(), []
    now = datetime.now(timezone.utc)

    for feed in FEEDS:
        try:
            parsed = feedparser.parse(feed["url"])
        except Exception as ex:
            print(f"[skip] {feed['name']}: {ex}")
            continue

        for e in parsed.entries[:15]:
            title = clean(getattr(e, "title", ""))
            link = getattr(e, "link", "")
            if not title or not link:
                continue
            uid = hashlib.md5((title + link).encode()).hexdigest()[:12]
            if uid in seen:
                continue
            seen.add(uid)

            dt = entry_time(e)
            age_h = (now - dt).total_seconds() / 3600
            if age_h > MAX_AGE_HOURS:
                continue

            summary = clean(getattr(e, "summary", ""))[:SUMMARY_LIMIT]
            text = f"{title} {summary}"
            score = side_score(text, feed["weight"], age_h, feed["lang"])

            articles.append({
                "id": uid,
                "title": title,
                "link": link,
                "summary": summary,
                "source": feed["name"],
                "lang": feed["lang"],
                "category": classify(text),
                "published": dt.astimezone(JST).isoformat(),
                "score": score,
                "stars": {
                    "importance": stars(max(score.values())),
                    "beginner":   stars(score["beginner"]),
                    "monetize":   stars(score["monetize"]),
                    "buzz":       stars(score["x"]),
                },
            })
        print(f"[ok] {feed['name']}: {len(parsed.entries)} entries")

    # 総合スコア降順
    articles.sort(key=lambda a: max(a["score"].values()), reverse=True)

    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps({
        "updated": now.astimezone(JST).isoformat(),
        "count": len(articles),
        "articles": articles[:60],
    }, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n→ {OUT} に {len(articles[:60])} 件を書き出しました")

if __name__ == "__main__":
    main()
