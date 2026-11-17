cd "$OUT"
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/130.0 Safari/537.36"
curl -sS -A "$UA" https://www.shugiintv.go.jp/js/js_video.js -o shu_js_video.js
curl -sS -A "$UA" "https://www.shugiintv.go.jp/jp/index.php?ex=VL" --data "s_Year=2026&s_Month=11&s_Day=17&e_Year=2026&e_Month=11&e_Day=17&c_day=on&r_condition=0&s_kaigi=&h_page=1" -o shu_vl_search.html
grep -o 'deli_id=[0-9]*[^"]*' shu_vl_search.html | sort -u | head -20
curl -sS -A "$UA" https://www.webtv.sangiin.go.jp/webtv/index.php -o san_index.html
grep -o 'src="[^"]*\.js[^"]*"' san_index.html
for j in $(grep -o 'src="[^"]*\.js[^"]*"' san_index.html | sed 's/src="//;s/"//' | grep -v jquery | head -8); do u=$(python3 -c "import urllib.parse,sys;print(urllib.parse.urljoin('https://www.webtv.sangiin.go.jp/webtv/index.php',sys.argv[1]))" "$j"); f=san_$(basename "${j%%\?*}"); curl -sS -A "$UA" "$u" -o "$f"; echo "== $u"; grep -o -E '[a-zA-Z0-9_./-]+\.(php|json)[^"'"'"' ]*' "$f" | sort -u | head -20; done
