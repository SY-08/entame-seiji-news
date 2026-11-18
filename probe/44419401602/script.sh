python - <<'PY' > "$OUT/leaders.txt"
import requests, time, collections
names = ["玉木雄一郎","水岡俊一","田村智子","藤田文武","神谷宗幣","山本太郎","斉藤鉄夫","野田佳彦","百田尚樹","福島みずほ","安野貴博","吉村洋文","西田昌司","竹谷とし子","櫛渕万里","大石あきこ","泉健太"]
for n in names:
    rows=[]; start=1
    while True:
        r=requests.get("https://kokkai.ndl.go.jp/api/speech",params={"speaker":n,"from":"2025-10-01","until":"2026-11-19","maximumRecords":100,"startRecord":start,"recordPacking":"json"},timeout=60,headers={"User-Agent":"Mozilla/5.0"}); print(n,r.status_code,r.text[:200]) if r.status_code!=200 or not r.text.startswith("{") else None; r=r.json() if r.text.startswith("{") else {}
        for s in r.get("speechRecord",[]): rows.append((s["date"],s["nameOfHouse"],s["nameOfMeeting"]))
        nxt=r.get("nextRecordPosition")
        if not nxt: break
        start=nxt; time.sleep(1)
    days=sorted(set((d,h,m) for d,h,m in rows))
    byday=sorted(set(d for d,_,_ in days))
    print(f"## {n}  発言 {len(rows)}件 / {len(byday)}日")
    for d,h,m in days: print("  ",d,h,m)
    time.sleep(1)
PY
