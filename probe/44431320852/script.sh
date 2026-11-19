python - <<'PY' > "$OUT/san2.txt"
import requests,re,html as H
UA={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/130.0 Safari/537.36","Referer":"https://www.webtv.sangiin.go.jp/webtv/index.php"}
S="https://www.webtv.sangiin.go.jp/webtv/"
s=requests.Session(); s.get(S+"index.php",headers=UA,timeout=30)
for sid in list(range(9315,9330)):
    d=s.get(S+f"detail.php?sid={sid}",headers=UA,timeout=30).text
    def g(p):
        m=re.search(p,d,flags=re.S); return H.unescape(re.sub(r"<[^>]+>"," ",m.group(1))).strip() if m else ""
    hsh=re.search(r"player\?hash=([a-z0-9]+)",d)
    print("=====",sid,g(r"開会日</dt><dd>(.*?)</dd>"),g(r"会議名</dt><dd>(.*?)</dd>"),"hash",hsh.group(1) if hsh else "")
    print("経過:",re.sub(r"\s+","",g(r"会議の経過</h3>\s*<span>(.*?)</span>")))
    print("発言者:",[(H.unescape(n),float(o)) for o,n in re.findall(r"href='#([\d.]+)' class='play2'>([^<]+)</a>",d)])
    if sid==9329 and hsh:
        p=s.get("https://public.mediasp.jp/v1/player?hash="+hsh.group(1)+"&forward_sec=10",headers=UA,timeout=30).text
        open("PLAYER","w").write(p)
        print("PLAYER", sorted(set(re.findall(r"https?://[^\"'\\\\ ]+",p)))[:30])
PY
cp PLAYER "$OUT/player_9329.js" 2>/dev/null; true
