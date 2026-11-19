python - <<'PY' > "$OUT/pm.txt"
import requests,time,collections
H={"User-Agent":"Mozilla/5.0"}
A="https://kokkai.ndl.go.jp/api/"
mt=[];start=1
while True:
    r=requests.get(A+"meeting_list",params={"speaker":"高市早苗","from":"2026-10-01","until":"2026-11-19","maximumRecords":100,"startRecord":start,"recordPacking":"json"},headers=H,timeout=60).json()
    mt+=r.get("meetingRecord",[]); n=r.get("nextRecordPosition")
    if not n: break
    start=n; time.sleep(1)
for m in mt:
    r=requests.get(A+"speech",params={"issueID":m["issueID"],"maximumRecords":100,"recordPacking":"json"},headers=H,timeout=60).json()
    sp=[]; 
    for s in r.get("speechRecord",[]):
        k=(s["speaker"],s.get("speakerGroup") or s.get("speakerPosition") or "")
        if k not in sp: sp.append(k)
    print("==",m["date"],m["nameOfHouse"],m["nameOfMeeting"],m["issue"])
    print("  ",[f"{a}({b})" for a,b in sp])
    time.sleep(1)
PY
