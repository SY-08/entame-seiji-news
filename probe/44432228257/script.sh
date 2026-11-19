python - <<'PY'
import requests,re,os,urllib.parse,concurrent.futures as cf
UA={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/130.0 Safari/537.36","Referer":"https://www.webtv.sangiin.go.jp/"}
jobs={"kamiya_1019":("https://sangiin-vod.live.ipcasting.jp/live/dirty/9/2f394551f6a3e68ec7b9ee8ccc764938/index_161315518726326.m3u8",18700,21020),
      "koike_1113":("https://sangiin-vod.live.ipcasting.jp/live/dirty/5/1a48b8df11dd8b3ad2cb6846d283162c/index_161509875423186.m3u8",9685,10600)}
for name,(m3,a,b) in jobs.items():
    master=requests.get(m3,headers=UA,timeout=30).text
    sub=re.search(r'URI="([^"]+webvtt[^"]*)"',master).group(1)
    surl=urllib.parse.urljoin(m3,sub)
    pl=requests.get(surl,headers=UA,timeout=30).text
    t=0.0; segs=[]
    lines=pl.splitlines()
    for i,l in enumerate(lines):
        if l.startswith("#EXTINF:"):
            dur=float(l[8:].split(",")[0]); u=lines[i+1]
            if t+dur>=a and t<=b: segs.append((t,urllib.parse.urljoin(surl,u)))
            t+=dur
    def f(x): 
        st,u=x
        try: return st,requests.get(u,headers=UA,timeout=30).text
        except Exception as e: return st,""
    with cf.ThreadPoolExecutor(8) as ex: res=list(ex.map(f,segs))
    out=[]
    for st,txt in res:
        for m in re.finditer(r"(\d+:\d+:\d+\.\d+|\d+:\d+\.\d+) --> \S+[^\n]*\n(.+?)(?:\n\n|\Z)",txt,flags=re.S):
            out.append(f"{st:.1f}\t{m.group(1)}\t"+m.group(2).replace("\n"," "))
    open(os.environ["OUT"]+f"/{name}.tsv","w").write("\n".join(out))
    print(name,len(segs),"segs",len(out),"cues", "playlist total",t)
    if res: open(os.environ["OUT"]+f"/{name}_sample.vtt","w").write(res[len(res)//2][1][:1500])
PY
