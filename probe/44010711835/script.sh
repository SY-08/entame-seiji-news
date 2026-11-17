cd "$OUT"
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/130.0 Safari/537.36"
J=cj.txt
echo "== shugiin m3u8"
for u in http://hlsvod.shugiintv.go.jp/vod/_definst_/amlst:2026/2026-1117-1210-01/playlist.m3u8 https://hlsvod.shugiintv.go.jp/vod/_definst_/amlst:2026/2026-1117-1210-01/playlist.m3u8; do
  curl -sS -L -A "$UA" -e "https://www.shugiintv.go.jp/" -o m.txt -w "%{http_code} %{content_type}\n" "$u"; head -c 400 m.txt; echo
done
S=https://www.webtv.sangiin.go.jp/webtv
curl -sS -c $J -b $J -A "$UA" "$S/index.php" -o /dev/null
for sid in 9332 9333 9334; do
  curl -sS -c $J -b $J -A "$UA" -e "$S/index.php" -X POST "$S/detail.php?sid=$sid&fromtop=1" -o san_$sid.html
  echo "== sid $sid $(wc -c < san_$sid.html)"
  grep -o -E 'https?:[^"'"'"' ]*\.m3u8[^"'"'"' ]*' san_$sid.html | sort -u
  python3 - san_$sid.html <<'PY'
import re,html,sys
t=open(sys.argv[1],encoding="utf-8",errors="ignore").read()
t=re.sub(r'<script.*?</script>|<style.*?</style>',' ',t,flags=re.S)
s=re.sub(r'<[^>]+>',' ',t); s=re.sub(r'\s+',' ',html.unescape(s))
print(s[:2500])
PY
done
