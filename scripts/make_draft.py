"""API の無い（または審査が要る）SNS の「下書き」を作る。投稿は人が手で行う。

  python3 scripts/make_draft.py note "朝10分の家計簿"
  python3 scripts/make_draft.py tiktok "朝10分の家計簿"

templates/<種類>.md を写して drafts/<日付>-<種類>-<題>.md を作るだけ（ネットには出ない）。
中身はエージェントが playbooks/ の手順で書き、持ち主が確かめてアプリから投稿します。
"""

import os as _ng_os, sys as _ng_sys  # N-Hack 専用の門（下の3行を消すとこのキットは動きません）
_ng_sys.path.insert(0, _ng_os.path.dirname(_ng_os.path.abspath(__file__)))
import nhack_gate as _nhack_gate  # noqa: E402,F401

import argparse
import re
import sys
import time

from _common import ROOT

p = argparse.ArgumentParser()
p.add_argument("kind", choices=["tiktok"])
p.add_argument("title")
a = p.parse_args()
src = ROOT / "templates" / f"{a.kind}.md"
slug = re.sub(r"[\\/:*?\"<>|\s]+", "-", a.title)[:30]
dst = ROOT / "drafts" / f"{time.strftime('%Y-%m-%d')}-{a.kind}-{slug}.md"
if dst.exists():
    sys.exit(f"もうあります: {dst.relative_to(ROOT)}")
dst.parent.mkdir(exist_ok=True)
dst.write_text(src.read_text(encoding="utf-8").replace("（題）", a.title), encoding="utf-8")
print(f"作りました: {dst.relative_to(ROOT)}")
