cd "$OUT"
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/130.0 Safari/537.36"
R="https://www.webtv.sangiin.go.jp/"
curl -sS -A "$UA" -e "$R" "https://public.mediasp.jp/v1/player?channel_hash=cpl6oed632pig7l1fg0g&live_hash=dbtb210lufuc710sri30&dvr=true&forward_sec=10&playback_speed_steps=11" -o player.js
wc -c player.js
grep -o -E 'https?://[^"'"'"' )]*' player.js | sort -u | head -40
grep -o -E '"[a-z_]*(url|hls|m3u8|src|endpoint|api)[a-z_]*"\s*:\s*"[^"]*"' player.js | head -20
grep -o -E '[a-zA-Z0-9_./:-]*m3u8[a-zA-Z0-9_./?=&-]*' player.js | sort -u | head
for h in 9332 9333 9334; do curl -sS -A "$UA" -e "$R" -X POST "https://www.webtv.sangiin.go.jp/webtv/detail.php?sid=$h&fromtop=1" | grep -o -E 'live_hash=[a-z0-9]+|vod_hash=[a-z0-9]+|channel_hash=[a-z0-9]+|[a-z_]*hash=[a-z0-9]+' | sort -u | sed "s/^/$h /"; done
# shugiin download (10min) + transcribe
U="https://hlsvod.shugiintv.go.jp/vod/_definst_/amlst:2026/2026-1117-1210-01/playlist.m3u8"
yt-dlp -q --no-warnings --referer "https://www.shugiintv.go.jp/" --user-agent "$UA" -f best -o shu_56525.%(ext)s "$U" || ffmpeg -v warning -y -headers "Referer: https://www.shugiintv.go.jp/" -user_agent "$UA" -i "$U" -c copy shu_56525.ts
ls -la shu_56525.* 
F=$(ls shu_56525.* | head -1)
ffprobe -v error -show_entries format=duration:stream=width,height -of compact "$F"
ffmpeg -v error -y -i "$F" -c:v libx264 -preset veryfast -crf 23 -c:a aac -b:a 128k -movflags +faststart shu_56525.mp4 && rm -f shu_56525.ts
pip install -q faster-whisper
python3 - <<'PY'
from faster_whisper import WhisperModel
import json, subprocess
subprocess.run(["ffmpeg","-v","error","-y","-i","shu_56525.mp4","-ac","1","-ar","16000","a.wav"],check=True)
m=WhisperModel("small",device="cpu",compute_type="int8")
segs,_=m.transcribe("a.wav",language="ja",beam_size=5,vad_filter=True)
rows=[{"start":round(s.start,2),"end":round(s.end,2),"text":s.text.strip()} for s in segs]
json.dump(rows,open("shu_56525.json","w",encoding="utf-8"),ensure_ascii=False,indent=0)
open("shu_56525.txt","w",encoding="utf-8").write("\n".join(f"[{r['start']:7.1f}-{r['end']:7.1f}] {r['text']}" for r in rows))
PY
rm -f a.wav
