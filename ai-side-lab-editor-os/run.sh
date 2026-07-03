#!/bin/bash
# AI SIDE LAB Editor OS — ローカル一発起動
set -e
pip install feedparser -q 2>/dev/null || pip install feedparser --break-system-packages -q
python3 fetch.py || true
COUNT=$(python3 -c "import json;print(json.load(open('data/raw.json'))['count'])" 2>/dev/null || echo 0)
if [ "$COUNT" = "0" ]; then
  echo "⚠ RSS取得0件 → デモデータに切り替えます"
  python3 seed_demo.py
fi
python3 generate.py
python3 build_demo.py
echo ""
echo "✅ 完了。preview.html をブラウザで開くか、以下でローカルサーバー起動:"
echo "   python3 -m http.server 8000  →  http://localhost:8000"
