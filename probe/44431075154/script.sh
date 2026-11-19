for d in 2026-11-09 2026-11-10 2026-11-11 2026-11-12 2026-11-13 2026-11-14; do python tools/discover_shugiin.py "$OUT/shu_$d.json" $d > /dev/null 2>&1; done
python - <<'PY' > "$OUT/san.txt"
import requests,re,html as H
UA={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/130.0 Safari/537.36","Referer":"https://www.webtv.sangiin.go.jp/webtv/index.php"}
S="https://www.webtv.sangiin.go.jp/webtv/"
s=requests.Session(); s.get(S+"index.php",headers=UA,timeout=30)
for sid in range(9290,9336):
    try: d=s.get(S+f"detail.php?sid={sid}",headers=UA,timeout=30).text
    except Exception as e: print(sid,"ERR",e); continue
    if sid==9310: open("SAMPLE","w").write(d)
    t=H.unescape(re.sub(r"\s+"," ",re.sub(r"<[^>]+>"," ",re.sub(r"<script.*?</script>"," ",d,flags=re.S))))
    m=re.search(r"開会日\s*(\S+)",t); n=re.search(r"会議名\s*(\S+)",t)
    media=sorted(set(re.findall(r"https?://[^\"' ]+\.(?:m3u8|mp4)",d)))[:2]
    sp=re.findall(r"(\S+)（([^）]{1,25})）\s*\d{1,2}時\d{1,2}分",t)[:40]
    print(sid, m.group(1) if m else "", n.group(1) if n else "", media, sp)
PY
cp SAMPLE "$OUT/san_sample.html" 2>/dev/null
