# AI SIDE LAB — Editor OS

RSSからAI副業ニュースを収集し、**note記事の材料一式**（記事ネタ5案 / note設計書 / LLM投入用プロンプト×4 / タイトル20案 / SNS投稿 / 育成ロードマップLv1→6）まで自動生成するツール。

**運用コストゼロ設計**（signal-newsと同アーキテクチャ）
- Phase 1: Python（RSS収集・重複排除・キーワード分類・AI SIDE SCORE算出）
- Phase 2: Python（テンプレート方式で編集材料を生成 — API課金なし）
- Phase 3: 静的HTML + GitHub Pages（1日3回自動更新）

## 使い方

```bash
./run.sh              # 収集→生成→プレビュー作成まで一発
python3 -m http.server 8000   # → http://localhost:8000
```

RSSが取得できない環境では自動でデモデータに切り替わります。

## note運用について

noteには公式の投稿APIがないため、**自動投稿ではなくコピー運用**が前提です。
Editor OSの「プロンプト」タブをコピー → 任意のLLM（Claude / GPT / Gemini / Grok）に貼る → 生成された本文をnoteに貼り付け。

## 著作権配慮

- 要約は180字までに切り詰め、必ず出典リンクを表示
- note上のコンテンツを学習・複製する設計は含まない
- 記事構成テンプレートは一般的な読みやすい構成論をベースに自作

## ファイル構成

| ファイル | 役割 |
|---|---|
| `feeds.py` | RSSソース定義（20ソース、重み付き） |
| `fetch.py` | 収集・分類・AI SIDE SCORE算出 → `data/raw.json` |
| `generate.py` | 編集材料の生成 → `data/articles.json` |
| `index.html` | Editor OS ダッシュボード（単一ファイル） |
| `seed_demo.py` | デモデータ生成（動作確認用） |
| `build_demo.py` | データ埋め込み済み `preview.html` を生成 |
| `.github/workflows/update.yml` | 1日3回の自動更新 + GitHub Pagesデプロイ |

## カスタマイズポイント

- **スコア調整**: `fetch.py` の `KW` 辞書と `side_score()`
- **プロンプトの口調・禁止事項**: `generate.py` の `BASE_BRIEF`
- **ソース追加**: `feeds.py` に1行追加するだけ
