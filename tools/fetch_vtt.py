"""参議院の中継に付いている自動字幕（WebVTT）を、巻き戻しの最初から取り込み、時刻つきのテキストにする。

使い方: python tools/fetch_vtt.py <名前> <channel_hash> <live_hash> <出力フォルダ>
字幕は発言の位置を探すためだけに使う（動画に表示する字幕にはしない）。
"""
import re
import sys
import urllib.parse
from datetime import datetime, timedelta
from pathlib import Path

import requests

name, ch, lh, out = sys.argv[1:5]
out = Path(out)
out.mkdir(parents=True, exist_ok=True)
UA = {"User-Agent": "Mozilla/5.0", "Referer": "https://www.webtv.sangiin.go.jp/"}
base = f"https://sangiin-live.live.ipcasting.jp/live/{ch}.h/{lh}/"
info = requests.get(base + "channel-info.json", headers=UA, timeout=30).json()
start = datetime.fromisoformat(info["schedules"][0]["status"]["program_start"])
master = requests.get(base + "index.m3u8", headers=UA, timeout=30).text
m = re.search(r'TYPE=SUBTITLES[^\n]*URI="([^"]+)"', master)
sub_pl_url = urllib.parse.urljoin(base, m.group(1))
pl = requests.get(sub_pl_url, headers=UA, timeout=30).text
segs = [urllib.parse.urljoin(sub_pl_url, l) for l in pl.splitlines() if l and not l.startswith("#")]
print(name, "subtitle segments:", len(segs))
cues = []
T = re.compile(r"(\d+):(\d+):(\d+)\.(\d+)\s*-->\s*(\d+):(\d+):(\d+)\.(\d+)")
mpeg_off = None
for i, u in enumerate(segs):
    t = requests.get(u, headers=UA, timeout=30).text
    # X-TIMESTAMP-MAP=MPEGTS:..,LOCAL:.. があれば無視し、プレイリスト内の相対時刻を使う
    lines = t.splitlines()
    j = 0
    while j < len(lines):
        mm = T.search(lines[j])
        if mm:
            h, mi, s, ms = map(int, mm.groups()[:4])
            sec = h * 3600 + mi * 60 + s + ms / 1000
            txt = []
            j += 1
            while j < len(lines) and lines[j].strip():
                txt.append(re.sub(r"<[^>]+>", "", lines[j]).strip())
                j += 1
            if txt:
                cues.append((sec, " ".join(txt)))
        j += 1
# 秒は配信開始からの経過とみなす。最初の字幕の秒が大きすぎる場合（絶対時刻）は最初を0にそろえる
if cues and cues[0][0] > 86400 / 2:
    first = cues[0][0]
    cues = [(c - first, x) for c, x in cues]
seen, rows = set(), []
for sec, x in cues:
    if x in seen:
        continue
    seen.add(x)
    clock = (start + timedelta(seconds=sec)).strftime("%H:%M:%S")
    rows.append(f"[{clock}] {x}")
(out / f"{name}_subtitles.txt").write_text("\n".join(rows), encoding="utf-8")
print(name, "cues:", len(rows))
