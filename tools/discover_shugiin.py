"""今日（または指定日）の衆議院ビデオライブラリの会議を探し、発言者一覧と録画URLを出す。

使い方: python tools/discover_shugiin.py <出力JSON> [YYYY-MM-DD]
衆議院は会議が終わって十数分後にビデオライブラリに載る（会議中のものは載らない）。
出力: {"date":..., "meetings":[{"deli_id","name","url","speakers":[{"name","group","clock","minutes","offset"}]}]}
- group は会派名または役職（例: 自由民主党・無所属の会 / 内閣総理大臣 / 政府参考人）
- offset は録画の先頭からの秒数（cut.py の from_sec / to_sec にそのまま使える）
"""
import html
import json
import re
import sys
from datetime import datetime, timedelta, timezone

import requests

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/130.0 Safari/537.36"
B = "https://www.shugiintv.go.jp/jp/index.php"
day = sys.argv[2] if len(sys.argv) > 2 else datetime.now(timezone(timedelta(hours=9))).strftime("%Y-%m-%d")
y, m, d = (int(x) for x in day.split("-"))
s = requests.Session()
s.headers.update({"User-Agent": UA, "Referer": B + "?ex=VL"})
s.get(B + "?ex=VL", timeout=30)


def get(url, data=None):
    r = s.post(url, data=data, timeout=60) if data else s.get(url, timeout=60)
    return r.content.decode("euc-jp", "ignore")


ids, page = [], 1
while True:
    t = get(B + "?ex=VL", {"c_day": "true", "s_Year": y, "s_Month": m, "s_Day": d, "e_Year": y, "e_Month": m, "e_Day": d,
                           "c_kaigi": "", "s_kaigi": "", "c_anken": "", "t_anken": "", "c_hatsugen": "", "t_hatsugen": "",
                           "r_condition": 0, "h_page": page, "submit3": ""})
    new = [i for i in dict.fromkeys(re.findall(r"deli_id=(\d+)", t)) if i not in ids]
    if not new:
        break
    ids += new
    page += 1
    if page > 5:
        break

out = []
for i in ids:
    t = get(f"{B}?ex=VL&deli_id={i}&media_type=")
    url = re.search(r'vtag_src_base_vod" value="([^"]+\.m3u8)"', t)
    name = re.search(r"会議名\s*[：:]\s*([^<\(（]+)", re.sub(r"<[^>]+>", " ", t))
    sp = []
    for off, who, rest in re.findall(r"deli_id=\d+&time=([\d.]+)\" class=\"play_vod\">([^<]+)</a></TD>(.*?)</TR>", t, flags=re.S | re.I):
        cells = [re.sub(r"\s+", "", html.unescape(re.sub(r"<[^>]+>", "", c))) for c in re.findall(r"<TD[^>]*>(.*?)</TD>", rest, flags=re.S | re.I)]
        mm = re.match(r"(.+?)\((.+)\)$", who.strip())
        sp.append({"name": mm.group(1) if mm else who.strip(), "group": mm.group(2) if mm else "",
                   "clock": cells[0].replace("時", ":").replace("分", "") if cells else "",
                   "minutes": cells[1].replace("分", "") if len(cells) > 1 else "", "offset": float(off)})
    out.append({"deli_id": i, "name": name.group(1).strip() if name else "",
                "url": url.group(1).replace("http://", "https://") if url else "", "speakers": sp})

res = {"date": day, "house": "衆議院", "meetings": out}
open(sys.argv[1], "w", encoding="utf-8").write(json.dumps(res, ensure_ascii=False, indent=1))
print(json.dumps(res, ensure_ascii=False, indent=1)[:4000])
