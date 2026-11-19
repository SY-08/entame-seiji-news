python - <<'PY' > "$OUT/s9267.json"
import requests,re,html as H,json
UA={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/130.0 Safari/537.36","Referer":"https://www.webtv.sangiin.go.jp/webtv/index.php"}
S="https://www.webtv.sangiin.go.jp/webtv/"
s=requests.Session(); s.get(S+"index.php",headers=UA,timeout=30)
out={}
for sid in (9267,9329):
    d=s.get(S+f"detail.php?sid={sid}",headers=UA,timeout=30).text
    hsh=re.search(r"player\?hash=([a-z0-9]+)",d).group(1)
    p=s.get("https://public.mediasp.jp/v1/player?hash="+hsh+"&forward_sec=10",headers=UA,timeout=30).text
    m3=re.findall(r"https?://[^\"'\\\\ ]+\.m3u8",p)
    ke=re.search(r"会議の経過</h3>\s*<span>(.*?)</span>",d,flags=re.S)
    out[sid]={"hash":hsh,"m3u8":m3,"keika":re.sub(r"\s+","",H.unescape(re.sub(r"<[^>]+>","",ke.group(1)))) if ke else "",
              "speakers":[[H.unescape(n),float(o)] for o,n in re.findall(r"href='#([\d.]+)' class='play2'>([^<]+)</a>",d)]}
    if m3:
        master=s.get(m3[0],headers=UA,timeout=30).text
        out[sid]["master"]=master[:800]
print(json.dumps(out,ensure_ascii=False,indent=1))
PY
