"""今日の参議院の会議（審議中継）を探し、収録に使う channel_hash / live_hash の一覧を出す。

使い方: python tools/discover.py <出力JSON>
出力: {"date": "...", "sangiin": [{"sid": "9332", "name": "内閣委員会", "time": "10:00", "key": "s9332:ch:lh"}], "channels": ["s9332:ch:lh", ...]}
"""
import json
import re
import sys
from datetime import datetime, timedelta, timezone

import requests

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/130.0 Safari/537.36",
      "Referer": "https://www.webtv.sangiin.go.jp/webtv/index.php"}
S = "https://www.webtv.sangiin.go.jp/webtv/"
ses = requests.Session()
ses.get(S + "index.php", headers=UA, timeout=30)
html = ses.post(S + "result_selecter.php", headers=UA, timeout=30).text
rows = []
for sid in sorted(set(re.findall(r"detail\.php\?sid=(\d+)", html))):
    d = ses.post(S + f"detail.php?sid={sid}&fromtop=1", headers=UA, timeout=30).text
    ch = re.search(r"channel_hash=([a-z0-9]+)", d)
    lh = re.search(r"live_hash=([a-z0-9]+)", d)
    name = re.search(r"会議名\s*</[^>]+>\s*<[^>]+>\s*([^<]+)", d)
    text = re.sub(r"<[^>]+>", " ", d)
    nm = re.search(r"会議名\s+(\S+)", text)
    tm = re.search(r"公報掲載時刻\s+(\d{1,2}:\d{2})", text)
    if ch and lh:
        rows.append({"sid": sid, "name": nm.group(1) if nm else "", "time": tm.group(1) if tm else "",
                     "key": f"s{sid}:{ch.group(1)}:{lh.group(1)}"})
out = {"date": datetime.now(timezone(timedelta(hours=9))).strftime("%Y-%m-%d"), "sangiin": rows,
       "channels": [r["key"] for r in rows]}
open(sys.argv[1], "w", encoding="utf-8").write(json.dumps(out, ensure_ascii=False, indent=1))
print(json.dumps(out, ensure_ascii=False, indent=1))
