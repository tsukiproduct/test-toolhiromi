#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI SIDE LAB Editor OS — Phase 2: 編集材料の生成（テンプレートベース / トークン消費ゼロ)

raw.json → 各記事に以下を付与 → data/articles.json
  1. 記事ネタ5案（初心者 / 副業 / 比較 / 体験談 / 収益化）
  2. note設計書（想定読者・悩み・読後・構成・SEO・差別化）
  3. LLM投入用プロンプト4種（Claude / GPT / Gemini / Grok）
  4. タイトル20案
  5. SNS投稿（X / Threads / Instagram）
  6. 育成ロードマップ Lv1→Lv6

実行: python3 generate.py
"""
import json, re
from pathlib import Path

DATA = Path(__file__).parent / "data"
SRC = DATA / "raw.json"
OUT = DATA / "articles.json"
ARCHIVE = DATA / "archive.json"

CAT_LABEL = {
    "model": "AIモデル", "imggen": "画像生成", "vidgen": "動画生成",
    "tool": "AIツール", "biz": "AIビジネス", "news": "AIニュース",
}

# ────────────────────────────────────────────
# ユーティリティ
# ────────────────────────────────────────────
def topic_of(a) -> str:
    """タイトルから主題を短く抽出（先頭の【】等を除去し、句読点で区切る）"""
    t = a["title"]
    t = re.sub(r"^\s*[【\[（(][^】\]）)]*[】\]）)]\s*", "", t)   # 先頭の【解説】などを除去
    t = re.split(r"[|｜:：—\-–、。/]", t)[0].strip()             # 最初の区切りまで
    if len(t) > 24:
        t = t[:24].rstrip("のをにはがでとやも、") + "…"
    return t or a["title"][:24]

def seo_keywords(a) -> list:
    base = [CAT_LABEL[a["category"]], "AI", "副業"]
    words = re.findall(r"[A-Za-z][A-Za-z0-9\.\-]{2,}", a["title"])[:3]
    return list(dict.fromkeys(words + base))[:6]

# ────────────────────────────────────────────
# 1. 記事ネタ5案
# ────────────────────────────────────────────
def ideas(a) -> list:
    t = topic_of(a)
    return [
        {"type": "初心者向け", "angle": f"「{t}」とは？何がすごいのか3分でわかる解説",
         "reader": "AIに興味はあるが専門用語が苦手な層"},
        {"type": "副業向け",   "angle": f"{t}で作業時間を半分にする実践ワークフロー",
         "reader": "副業でAIを使い倒したい会社員・個人事業主"},
        {"type": "比較記事",   "angle": f"{t} vs 既存の定番手法、乗り換えるべきか徹底比較",
         "reader": "すでにAIツールを使っていて次を探している層"},
        {"type": "体験談",     "angle": f"{t}を実際に使ってみた正直レビュー（良い点・微妙な点）",
         "reader": "導入前にリアルな評価を知りたい層"},
        {"type": "収益化",     "angle": f"{t}で稼げる可能性をロードマップ付きで検証",
         "reader": "AI副業で月1万円の壁を超えたい層"},
    ]

# ────────────────────────────────────────────
# 2. note設計書
# ────────────────────────────────────────────
def blueprint(a) -> dict:
    t = topic_of(a)
    kw = seo_keywords(a)
    return {
        "theme": t,
        "reader": "AI初心者〜中級者。副業・情報発信に関心がある20〜40代",
        "pain": f"「{t}」が話題だが、何が変わるのか・自分に関係あるのかが分からない",
        "after": "概要を人に説明でき、今日から試す最初の一歩が明確になっている",
        "structure": ["導入（読者の疑問を代弁）", "背景（なぜ今このニュースか）",
                      "本題（何ができるようになったか）", "メリット3つ",
                      "注意点・落とし穴", "まとめ + 次のアクション"],
        "seo": kw,
        "diff": "一次情報リンク + 初心者目線の噛み砕き + 副業への具体的な応用例で差別化",
        "spec": {"length": "2,600〜3,000字", "intro": "冒頭220字以内で結論提示",
                 "headings": "6〜7個", "linebreak": "3〜4行ごとに改行", "image": "見出し直下に図解1枚推奨"},
    }

# ────────────────────────────────────────────
# 3. LLM投入用プロンプト（4種）
# ────────────────────────────────────────────
BASE_BRIEF = """テーマ: {t}
元ニュース: {title}
出典URL: {link}
要約: {summary}

ターゲット読者: AI初心者〜中級者。副業・情報発信に関心がある20〜40代
読後のゴール: 概要を人に説明でき、今日から試す最初の一歩が明確になる
構成: 導入(結論先出し220字以内)→背景→本題→メリット3つ→注意点→まとめ+次のアクション
SEOキーワード: {kw}
文字数: 2,600〜3,000字 / 見出し6〜7個 / 3〜4行ごとに改行
口調: です・ます調。専門用語は必ず一言で補足。押し付けず、読者に寄り添う
情報の扱い（重要）:
- Web閲覧ができる場合、まず出典URLを開いて内容を確認してから書くこと
- 出典が開けない・閲覧機能がない場合は、上記の要約にある事実「だけ」を根拠にすること
- 要約にない数値・日付・料金・仕様・発言の引用を創作しない。書けない詳細は「詳細は出典を参照してください」と誘導する
- 確定情報と推測を区別し、推測は「〜と考えられます」と明示する
- 記事本文の最後に【投稿前チェック】として、出典で確認すべき事実を3点、箇条書きで出力する（これは読者向けではなく執筆者向けメモ）
禁止事項: 事実の捏造 / 誇大表現 / 出典のない数値 / 元記事の文章コピー"""

def prompts(a) -> dict:
    brief = BASE_BRIEF.format(t=topic_of(a), title=a["title"], link=a["link"],
                              summary=a["summary"] or "（元記事参照）",
                              kw="、".join(seo_keywords(a)))
    return {
        "claude": f"""あなたはnoteで人気のAI副業系編集者です。以下の設計書をもとにnote記事を書いてください。

<brief>
{brief}
</brief>

<instructions>
- まず記事全体の構成案を箇条書きで示してから本文を書く
- 導入は読者の疑問を代弁する問いかけで始める
- 各見出しの下に必ず具体例を1つ入れる
- 最後に「今日やること」を1つだけ提示して締める
</instructions>""",

        "gpt": f"""# 役割
あなたはnoteで人気のAI副業系編集者です。

# タスク
以下の設計書に従ってnote記事を執筆してください。

# 設計書
{brief}

# 出力形式
1. 記事タイトル
2. 本文（markdown見出し付き）
3. 記事末尾に「今日やること」1つ""",

        "gemini": f"""noteのAI副業系人気編集者として、次の設計書どおりに記事を1本書いてください。

{brief}

補足: 構成の順番は厳守。導入で結論を先に出し、最後は読者が今日できる行動1つで締めること。""",

        "grok": f"""あなたはnoteで人気のAI副業系編集者。堅すぎず、でも軽薄にならないトーンで。

{brief}

追加指示: ユーモアは1記事に1〜2箇所まで。事実ベースを最優先し、煽りタイトルは禁止。""",
    }

# ────────────────────────────────────────────
# 4. タイトル20案（フック型: 数字/問いかけ/逆説/損失回避/簡単系）
# ────────────────────────────────────────────
def titles(a) -> list:
    t = topic_of(a)
    c = CAT_LABEL[a["category"]]
    return [
        f"{t}とは？初心者向けに3分で解説",
        f"【最新】{t}、何が変わったのか要点だけまとめた",
        f"{t}を知らないと損する3つの理由",
        f"「{t}」って結局なに？に答える記事",
        f"{t}で作業時間が半分になった話",
        f"{t}、正直どうなの？使って分かった本音",
        f"初心者が{t}で最初にやるべきこと",
        f"{t}と定番ツール、どっちを選ぶべきか",
        f"{t}の落とし穴。始める前に知ってほしい注意点",
        f"月1万円の壁を{t}で超える方法を考えた",
        f"{t}まとめ｜今日から使える{c}の新常識",
        f"忙しい人のための{t}要点整理",
        f"{t}を副業に活かす具体的な3ステップ",
        f"なぜ今{t}が話題なのか、背景から解説",
        f"{t}、無料でどこまでできるか検証した",
        f"5分でわかる{t}。専門用語ゼロで解説",
        f"{t}が変える{c}の未来と、今やるべき準備",
        f"実は簡単だった{t}の始め方",
        f"{t}レビュー｜良かった点・微妙だった点を正直に",
        f"{t}完全ガイド【保存版】",
    ]

# ────────────────────────────────────────────
# 5. SNS投稿
# ────────────────────────────────────────────
def sns(a) -> dict:
    t = topic_of(a)
    return {
        "x": f"{t}、要点だけまとめました。\n\n・何ができる？\n・誰に関係ある？\n・今日からどう使う？\n\nnoteに詳細を書きました↓\n（記事URL）\n\n#AI #AI副業",
        "threads": f"{t}が話題ですね。\n\n「結局、自分に関係あるの？」という視点で整理してみました。\n\n結論だけ言うと、副業でAIを使っている人には確実に影響があります。詳しくはnoteで。",
        "instagram": f"📌 {t}\n\n今週のAIニュースで一番押さえておきたい話題。\n\n✅ 何が変わった？\n✅ 初心者に関係ある？\n✅ 副業にどう活きる？\n\n詳細はプロフィールのリンクから📎\n\n#AI #AI副業 #AI初心者 #生成AI",
    }

# ────────────────────────────────────────────
# 6. 育成ロードマップ Lv1→Lv6
# ────────────────────────────────────────────
def roadmap(a) -> list:
    t = topic_of(a)
    return [
        {"lv": 1, "type": "速報",       "title": f"【速報】{t}", "when": "当日", "platform": "X"},
        {"lv": 2, "type": "初心者解説", "title": f"{t}とは？3分でわかる解説", "when": "1〜2日後", "platform": "note無料"},
        {"lv": 3, "type": "比較記事",   "title": f"{t} vs 既存手法を比較", "when": "3〜4日後", "platform": "note無料"},
        {"lv": 4, "type": "体験レビュー", "title": f"{t}を1週間使った正直レビュー", "when": "1週間後", "platform": "note無料+X"},
        {"lv": 5, "type": "収益化記事", "title": f"{t}で稼ぐ具体的ワークフロー", "when": "2週間後", "platform": "note有料"},
        {"lv": 6, "type": "商品化",     "title": f"{t}活用テンプレート集", "when": "1ヶ月後", "platform": "Brain/note有料"},
    ]

# ────────────────────────────────────────────
# 7. 組み合わせ記事（コンボ）
#    収益化の高いニュース × 別カテゴリの手法系ニュースを掛け合わせ
# ────────────────────────────────────────────
COMBO_PROMPT = """あなたはnoteで人気のAI副業系編集者です。
以下の2つのニュースを掛け合わせて、1本のnote記事を書いてください。

<news_a role="事例・動機づけ">
タイトル: {ta}
要約: {sa}
出典: {la}
</news_a>

<news_b role="手法・具体的なやり方">
タイトル: {tb}
要約: {sb}
出典: {lb}
</news_b>

<brief>
記事の狙い: news_aで「稼げる・変化が起きている」という動機を作り、news_bで「では具体的にどうやるか」を示す構成
ターゲット読者: AI副業に関心がある初心者〜中級者
構成: 導入(2つのニュースの接点を一言で)→news_aの紹介(何が起きたか)→news_bの紹介(どう使うか)→2つを組み合わせた実践ステップ3つ→注意点→まとめ+今日やること1つ
文字数: 2,600〜3,000字 / 見出し6〜7個 / 3〜4行ごとに改行
口調: です・ます調。専門用語は一言で補足
情報の扱い（重要）:
- Web閲覧ができる場合、2つの出典URLを両方開いて確認してから書くこと
- 開けない場合は、上記の各要約にある事実「だけ」を根拠にし、要約にない数値・仕様を創作しない
- 記事本文の最後に【投稿前チェック】として、各出典で確認すべき事実を計3点、箇条書きで出力する（執筆者向けメモ）
禁止事項: 事実の捏造 / 誇大表現 / 出典のない数値 / 2つのニュースの因果関係の捏造(「関連する動き」として紹介し、無理につなげない)
</brief>"""

def combo_prompt(a, b) -> str:
    return COMBO_PROMPT.format(
        ta=a["title"], sa=a.get("summary_ja") or a["summary"] or "（出典参照）", la=a["link"],
        tb=b["title"], sb=b.get("summary_ja") or b["summary"] or "（出典参照）", lb=b["link"])

def combo_titles(a, b) -> list:
    x, y = topic_of(a), topic_of(b)
    return [
        f"{x}の今、{y}で稼ぐ準備を始める",
        f"{x}×{y}｜この組み合わせが副業の最短ルート",
        f"{x}が示す変化と、{y}という具体策",
        f"ニュース2本で理解する、いまAI副業で起きていること",
        f"{y}の使いどき。{x}が追い風になる理由",
    ]

def build_combos(articles) -> list:
    if len(articles) < 2:
        return []
    by_money = sorted(articles, key=lambda a: a["score"]["monetize"], reverse=True)
    combos, used = [], set()
    for money in by_money:
        if len(combos) >= 3:
            break
        if money["id"] in used:
            continue
        # 相方: 別カテゴリで、手法系(tool/model/imggen/vidgen)かつnote適性が高いもの
        partners = [p for p in articles
                    if p["id"] != money["id"] and p["id"] not in used
                    and p["category"] != money["category"]
                    and p["category"] in ("tool", "model", "imggen", "vidgen")]
        if not partners:
            partners = [p for p in articles if p["id"] != money["id"] and p["id"] not in used]
        if not partners:
            continue
        partner = max(partners, key=lambda p: p["score"]["note"])
        used.update({money["id"], partner["id"]})
        combos.append({
            "id": f"cb_{money['id']}_{partner['id']}",
            "theme": f"{topic_of(money)} × {topic_of(partner)}",
            "a_id": money["id"], "b_id": partner["id"],
            "a_title": money["title"], "b_title": partner["title"],
            "why": f"「{topic_of(money)}」で読者の関心と動機を作り、「{topic_of(partner)}」で具体的な手を渡す構成が組めます。事例×手法は単体記事より深く、有料化にも向きます。",
            "prompt": combo_prompt(money, partner),
            "titles": combo_titles(money, partner),
        })
    return combos

# ────────────────────────────────────────────

def merge_archive(current_articles) -> list:
    merged = {}
    if ARCHIVE.exists():
        try:
            old = json.loads(ARCHIVE.read_text(encoding="utf-8")).get("articles", [])
        except Exception:
            old = []
        for a in old:
            if a.get("id"):
                merged[a["id"]] = a
    for a in current_articles:
        if a.get("id"):
            merged[a["id"]] = a
    return sorted(
        merged.values(),
        key=lambda a: a.get("published") or "",
        reverse=True,
    )[:1000]

def main():
    src = json.loads(SRC.read_text(encoding="utf-8"))
    for a in src["articles"]:
        a["ideas"] = ideas(a)
        a["blueprint"] = blueprint(a)
        a["prompts"] = prompts(a)
        a["titles"] = titles(a)
        a["sns"] = sns(a)
        a["roadmap"] = roadmap(a)
    src["combos"] = build_combos(src["articles"])
    archive_articles = merge_archive(src["articles"])
    archive = dict(src)
    archive["articles"] = archive_articles
    archive["count"] = len(archive_articles)
    archive["combos"] = build_combos(archive_articles[:60])
    OUT.write_text(json.dumps(src, ensure_ascii=False, indent=1), encoding="utf-8")
    ARCHIVE.write_text(json.dumps(archive, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"→ {OUT} に編集材料を付与しました（記事{src['count']}件 / 組み合わせ{len(src['combos'])}案 / アーカイブ{len(archive_articles)}件）")

if __name__ == "__main__":
    main()
