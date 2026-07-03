#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""articles.json を index.html に埋め込み、単体で開けるプレビューを生成"""
import json
from pathlib import Path

root = Path(__file__).parent
html = (root / "index.html").read_text(encoding="utf-8")
data = json.loads((root / "data" / "articles.json").read_text(encoding="utf-8"))

embed = f"<script>window.EMBED = {json.dumps(data, ensure_ascii=False)};</script>\n<script>"
html = html.replace("<script>\nconst CAT", embed + "\nconst CAT", 1)

out = root / "preview.html"
out.write_text(html, encoding="utf-8")
print(f"→ {out}（ブラウザで直接開けるデモ版）")
