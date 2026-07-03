#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI SIDE LAB Editor OS — Phase 1.5: Cloudflare Workers AIによる強化（任意・無料枠）

英語ニュースに日本語要約＋AI副業視点の一言を付与する。
Workerのデプロイは不要。REST APIを直接呼ぶ。

必要な環境変数（GitHub Secretsに登録）:
  CF_ACCOUNT_ID  … CloudflareのアカウントID
  CF_API_TOKEN   … Workers AI 権限付きAPIトークン

未設定なら何もせず正常終了する（Editor OSはAIなしでも完全動作する設計）。
実行: python3 enrich.py
"""
import json, os, re, sys
from pathlib import Path

import requests

DATA = Path(__file__).parent / "data" / "raw.json"
MODEL = "@cf/meta/llama-3.3-70b-instruct-fp8-fast"   # まうBotで日本語品質を確認済み
MAX_CALLS = 20        # 無料枠(1日10,000ニューロン)を考慮した上限
TIMEOUT = 40

ACC = os.environ.get("CF_ACCOUNT_ID", "").strip()
TOK = os.environ.get("CF_API_TOKEN", "").strip()

PROMPT = """次の英語AIニュースを処理してください。
タイトル: {title}
概要: {summary}

以下のJSONだけを返してください。前置き・コードブロック記号は禁止。
{{"summary_ja":"日本語要約(100字以内、です・ます調)","tip":"AI副業に活かす視点の一言(40字以内)"}}"""

def call_ai(title: str, summary: str) -> dict | None:
    url = f"https://api.cloudflare.com/client/v4/accounts/{ACC}/ai/run/{MODEL}"
    try:
        r = requests.post(url,
            headers={"Authorization": f"Bearer {TOK}"},
            json={"messages": [{"role": "user", "content": PROMPT.format(title=title, summary=summary or "(no summary)")}],
                  "max_tokens": 220, "temperature": 0.3},
            timeout=TIMEOUT)
        r.raise_for_status()
        text = (r.json().get("result") or {}).get("response", "")
        m = re.search(r"\{.*\}", text, re.S)
        if not m:
            return None
        obj = json.loads(m.group())
        s, t = str(obj.get("summary_ja", "")).strip(), str(obj.get("tip", "")).strip()
        if not s:
            return None
        return {"summary_ja": s[:140], "tip": t[:60]}
    except Exception as ex:
        print(f"  [skip] {ex}")
        return None

def main():
    if not (ACC and TOK):
        print("CF_ACCOUNT_ID / CF_API_TOKEN 未設定 → AI強化をスキップ（テンプレートのみで続行）")
        return
    if not DATA.exists():
        print("raw.json がありません。先に fetch.py を実行してください")
        sys.exit(1)

    src = json.loads(DATA.read_text(encoding="utf-8"))
    done = 0
    for a in src["articles"]:
        if done >= MAX_CALLS:
            break
        if a.get("lang") != "en" or a.get("summary_ja"):
            continue
        res = call_ai(a["title"], a.get("summary", ""))
        if res:
            a["summary_ja"] = res["summary_ja"]
            if res["tip"]:
                a["tip"] = res["tip"]
            done += 1
            print(f"  [ai] {a['title'][:40]}…")

    DATA.write_text(json.dumps(src, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"→ Workers AIで {done} 件を日本語化しました")

if __name__ == "__main__":
    main()
