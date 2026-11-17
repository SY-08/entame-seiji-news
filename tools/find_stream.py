"""衆参インターネット審議中継のページをたどり、ライブ（または録画）のHLS(m3u8)のURLを探す。

使い方: python tools/find_stream.py <院: shugiin|sangiin> <出力フォルダ> [会議名の一部]
見つかったURLを <出力フォルダ>/stream_url.txt に書く。たどったページとリンクも保存する（調査用）。
"""
import json
import re
import subprocess
import sys
import urllib.parse
from pathlib import Path

import requests

house = sys.argv[1]
out = Path(sys.argv[2])
keyword = sys.argv[3] if len(sys.argv) > 3 else ""
(out / "pages").mkdir(parents=True, exist_ok=True)

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36",
      "Accept-Language": "ja,en;q=0.8"}
if house == "shugiin":
    starts = ["https://www.shugiintv.go.jp/jp/index.php?ex=TD", "https://www.shugiintv.go.jp/jp/"]
    host = "shugiintv.go.jp"
else:
    starts = ["https://www.webtv.sangiin.go.jp/webtv/index.php"]
    host = "sangiin.go.jp"

M3U8 = re.compile(r"""(https?:)?(\\?/\\?/)[^"'\s<>]+?\.m3u8[^"'\s<>]*""")
HREF = re.compile(r"""(?:href|src)\s*=\s*["']([^"']+)["']""", re.I)

seen, queue, found, log = set(), list(starts), [], []
n = 0
while queue and n < 40:
    url = queue.pop(0)
    if url in seen:
        continue
    seen.add(url)
    n += 1
    try:
        r = requests.get(url, headers=UA, timeout=30)
        text = r.text
        log.append(f"{r.status_code} {len(text)} {url}")
    except Exception as e:  # noqa: BLE001
        log.append(f"ERR {e} {url}")
        continue
    (out / "pages" / f"{n:02d}.html").write_text(f"<!-- {url} -->\n" + text, encoding="utf-8")
    for m in M3U8.finditer(text):
        u = m.group(0).replace("\\/", "/")
        if u.startswith("//"):
            u = "https:" + u
        found.append({"page": url, "m3u8": u, "keyword_hit": keyword in text})
    for h in HREF.findall(text):
        full = urllib.parse.urljoin(url, h)
        if host not in full or full in seen:
            continue
        low = full.lower()
        if any(k in low for k in ("deli_id", "ex=vl", "ex=td", "ex=lv", "live", "detail.php", "sid=", "player")):
            queue.append(full)

(out / "links.txt").write_text("\n".join(log), encoding="utf-8")
(out / "found.json").write_text(json.dumps(found, ensure_ascii=False, indent=1), encoding="utf-8")
print("\n".join(log))
print(json.dumps(found, ensure_ascii=False, indent=1))

# yt-dlp の汎用抽出も試す
if not found:
    for url in list(seen)[:15]:
        try:
            p = subprocess.run(["yt-dlp", "-g", "--no-warnings", url], capture_output=True, text=True, timeout=60)
            for line in p.stdout.splitlines():
                if line.startswith("http"):
                    found.append({"page": url, "m3u8": line, "keyword_hit": False, "via": "yt-dlp"})
        except Exception:  # noqa: BLE001
            pass

best = None
for f in found:
    if keyword and f.get("keyword_hit"):
        best = f
        break
if not best and found:
    best = found[0]
if best:
    (out / "stream_url.txt").write_text(best["m3u8"], encoding="utf-8")
    print("STREAM", best["m3u8"])
else:
    print("STREAM NOT FOUND")
    sys.exit(1)
