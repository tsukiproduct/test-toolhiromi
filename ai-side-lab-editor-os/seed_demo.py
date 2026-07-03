#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""デモデータ生成: fetch.pyと同じ形式のraw.jsonを作る（動作確認用）"""
import json
from datetime import datetime, timezone, timedelta
from pathlib import Path
from fetch import side_score, stars, classify

JST = timezone(timedelta(hours=9))
now = datetime.now(JST)

DEMO = [
    ("次世代マルチモーダルモデルが発表、動画理解と長文処理が大幅強化", "OpenAI News", "en", 1.5,
     "新モデルは動画・音声・テキストを統合的に処理し、長時間コンテキストの保持性能が向上。APIは段階的に提供予定。", 2),
    ("エージェント機能の一般公開を開始、日常タスクの自動化が可能に", "Anthropic News", "en", 1.5,
     "ブラウザ操作やファイル処理を含む一連のタスクをAIが自律実行。無料プランでも一部機能が利用可能に。", 5),
    ("動画生成AIの新バージョン、1080p・10秒生成に対応し商用利用も許可", "TechCrunch AI", "en", 1.2,
     "生成速度が従来比3倍に。クリエイター向けの新料金プランと収益化プログラムも同時発表された。", 8),
    ("【解説】生成AIの副業活用、初心者が最初に押さえるべき3つのポイント", "ITmedia AI+", "ja", 1.2,
     "無料ツールの選び方、著作権の注意点、収益化までのロードマップを初心者向けにまとめて解説する。", 12),
    ("ローカルLLMの量子化手法に進展、家庭用GPUで大規模モデルが動作", "r/LocalLLaMA", "en", 0.9,
     "新しい量子化フォーマットにより、メモリ使用量を半減しつつ精度低下を最小限に抑えることに成功。", 18),
    ("画像生成AIの新機能でキャラクターの一貫性保持が可能に", "Hugging Face Blog", "en", 1.3,
     "参照画像1枚から同一キャラクターを異なるポーズ・構図で生成できる技術がオープンソースで公開。", 22),
    ("AI自動化ツールの無料枠が拡大、個人開発者の参入障壁が低下", "Product Hunt", "en", 0.9,
     "ワークフロー自動化サービスが無料プランの実行回数を大幅に拡大。副業・個人利用での活用が加速しそうだ。", 30),
    ("プロンプトエンジニアリング実践ガイド：業務効率化の具体例10選", "Zenn AI", "ja", 1.0,
     "現場で使えるプロンプト設計のコツを、実例とともに初心者にもわかりやすく解説した記事が話題に。", 40),
]

articles = []
for i, (title, source, lang, weight, summary, age_h) in enumerate(DEMO):
    text = f"{title} {summary}"
    score = side_score(text, weight, age_h, lang)
    articles.append({
        "id": f"demo{i:03d}", "title": title,
        "link": "https://example.com/article", "summary": summary,
        "source": source, "lang": lang, "category": classify(text),
        "published": (now - timedelta(hours=age_h)).isoformat(),
        "score": score,
        "stars": {"importance": stars(max(score.values())), "beginner": stars(score["beginner"]),
                  "monetize": stars(score["monetize"]), "buzz": stars(score["x"])},
    })

articles.sort(key=lambda a: max(a["score"].values()), reverse=True)
out = Path(__file__).parent / "data" / "raw.json"
out.parent.mkdir(exist_ok=True)
out.write_text(json.dumps({"updated": now.isoformat(), "count": len(articles),
                           "articles": articles}, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"→ {out} にデモデータ {len(articles)} 件")
