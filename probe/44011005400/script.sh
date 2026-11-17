cd "$OUT"
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/130.0 Safari/537.36"
R="https://www.webtv.sangiin.go.jp/"
for pair in "naikaku cpl6oed632pig7l1fg0g dbtb210lufuc710sri30" "houmu cpl6ndumbb93lo02j6gg dbtb1u0lufuc710sri2g" "keisan cpl6m9d632pu6i7ccg70 dbtb1tjl80ds71s5u9f0"; do
  set -- $pair
  curl -sS -A "$UA" -e "$R" "https://sangiin-live.live.ipcasting.jp/live/$2.h/$3/channel-info.json" -o ci_$1.json
  echo "== $1"; cat ci_$1.json; echo
  M=$(python3 -c "import json,sys,re;t=open('ci_$1.json').read();m=re.findall(r'https?://[^\"]+\.m3u8[^\"]*',t);print(m[0] if m else '')")
  echo "M=$M"
  [ -n "$M" ] && curl -sS -A "$UA" -e "$R" "$M" | head -12
done
U="https://hlsvod.shugiintv.go.jp/vod/_definst_/amlst:2026/2026-1117-1210-01/playlist.m3u8"
ffmpeg -v warning -y -headers "Referer: https://www.shugiintv.go.jp/" -user_agent "$UA" -i "$U" -c copy shu_56525.ts
ls -la shu_56525.ts
ffprobe -v error -show_entries format=duration:stream=width,height -of compact shu_56525.ts
