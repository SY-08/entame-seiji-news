cd "$OUT"
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/130.0 Safari/537.36"
J=cj.txt
B="https://www.shugiintv.go.jp/jp/index.php"
curl -sS -c $J -b $J -A "$UA" "$B?ex=VL" -o /dev/null
curl -sS -c $J -b $J -A "$UA" -e "$B?ex=VL" "$B?ex=VL&deli_id=56525&media_type=" -o vod.html; wc -c vod.html
iconv -f EUC-JP -t UTF-8 vod.html > vod_utf8.html 2>/dev/null || cp vod.html vod_utf8.html
grep -o -E 'https?://[^"'"'"' ]*\.m3u8[^"'"'"' ]*|vtag_src[^>]*' vod_utf8.html | sort -u
python3 - <<'PY'
import re,html
t=open("vod_utf8.html",encoding="utf-8",errors="ignore").read()
s=re.sub(r'\s+',' ',html.unescape(re.sub(r'<script.*?</script>',' ',t,flags=re.S)))
s=re.sub(r'<[^>]+>',' ',s); s=re.sub(r'\s+',' ',s)
i=s.find("政治改革"); print(s[max(0,i-300):i+1500])
PY
URL=$(grep -o -E 'https?://[^"'"'"' ]*\.m3u8[^"'"'"' ]*' vod_utf8.html | grep -v _roomid_ | head -1)
echo "URL=$URL"
[ -z "$URL" ] && exit 0
ffmpeg -v warning -y -user_agent "$UA" -i "$URL" -c copy full.ts
ffprobe -v error -show_entries format=duration:stream=width,height,codec_name -of compact full.ts
ffmpeg -v error -y -i full.ts -vf "scale=1280:720" -c:v libx264 -preset veryfast -crf 27 -c:a aac -b:a 128k -movflags +faststart vod_56525.mp4
ls -la vod_56525.mp4
rm -f full.ts
pip install -q faster-whisper
python3 - <<'PY'
from faster_whisper import WhisperModel
import json, subprocess
subprocess.run(["ffmpeg","-v","error","-y","-i","vod_56525.mp4","-ac","1","-ar","16000","a.wav"],check=True)
m=WhisperModel("small",device="cpu",compute_type="int8")
segs,_=m.transcribe("a.wav",language="ja",beam_size=5,vad_filter=True)
rows=[{"start":round(s.start,2),"end":round(s.end,2),"text":s.text.strip()} for s in segs]
json.dump(rows,open("transcript_56525.json","w",encoding="utf-8"),ensure_ascii=False,indent=0)
open("transcript_56525.txt","w",encoding="utf-8").write("\n".join(f"[{r['start']:7.1f}-{r['end']:7.1f}] {r['text']}" for r in rows))
print(len(rows))
PY
rm -f a.wav
