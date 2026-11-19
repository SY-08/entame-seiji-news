python - <<'PY'
import datetime as dt,subprocess
d=dt.date(2026,10,19)
while d<=dt.date(2026,11,7):
    if d.weekday()<5: subprocess.run(["python","tools/discover_shugiin.py",f"{__import__('os').environ['OUT']}/shu_{d}.json",str(d)],capture_output=True)
    d+=dt.timedelta(days=1)
PY
python - <<'PY' > "$OUT/san3.txt"
import requests,re,html as H
UA={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/130.0 Safari/537.36","Referer":"https://www.webtv.sangiin.go.jp/webtv/index.php"}
S="https://www.webtv.sangiin.go.jp/webtv/"
s=requests.Session(); s.get(S+"index.php",headers=UA,timeout=30)
for sid in range(9255,9300):
    d=s.get(S+f"detail.php?sid={sid}",headers=UA,timeout=30).text
    def g(p):
        m=re.search(p,d,flags=re.S); return H.unescape(re.sub(r"<[^>]+>"," ",m.group(1))).strip() if m else ""
    ke=re.sub(r"\s+","",g(r"会議の経過</h3>\s*<span>(.*?)</span>"))
    sp=[H.unescape(n) for o,n in re.findall(r"href='#([\d.]+)' class='play2'>([^<]+)</a>",d)]
    print(sid,g(r"開会日</dt><dd>(.*?)</dd>"),g(r"会議名</dt><dd>(.*?)</dd>"),"総理" if ("内閣総理大臣" in ke or any("内閣総理大臣" in x for x in sp)) else "",sp if ("内閣総理大臣" in ke or any("内閣総理大臣" in x for x in sp)) else "")
PY
