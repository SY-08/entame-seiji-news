cd "$OUT"
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/130.0 Safari/537.36"
J=cj.txt
curl -sS -c $J -b $J -A "$UA" "https://www.shugiintv.go.jp/jp/index.php?ex=VL" -o shu_vl_get.html; wc -c shu_vl_get.html
curl -sS -c $J -b $J -A "$UA" -e "https://www.shugiintv.go.jp/jp/index.php?ex=VL" "https://www.shugiintv.go.jp/jp/index.php?ex=VL" \
  --data-urlencode "c_day=true" --data "s_Year=2026&s_Month=11&s_Day=17&e_Year=2026&e_Month=11&e_Day=17&c_kaigi=&s_kaigi=&c_anken=&t_anken=&c_hatsugen=&t_hatsugen=&r_condition=0&h_page=1&submit3=" -o shu_vl_post.html; wc -c shu_vl_post.html
grep -o 'deli_id=[0-9]*' shu_vl_get.html shu_vl_post.html | sort -u | head
grep -o 'ex=VL[^"]*' shu_vl_get.html | sort -u | head -20
# sangiin
S=https://www.webtv.sangiin.go.jp/webtv
curl -sS -c $J -b $J -A "$UA" "$S/index.php" -o /dev/null
curl -sS -c $J -b $J -A "$UA" -e "$S/index.php" -X POST "$S/result_selecter.php" -o san_result.html; wc -c san_result.html
curl -sS -c $J -b $J -A "$UA" -e "$S/index.php" "$S/kaigi_list.php" -o san_kaigi.html; wc -c san_kaigi.html
curl -sS -c $J -b $J -A "$UA" -e "$S/index.php" "$S/news.php" -o san_news.html; wc -c san_news.html
grep -o "showDetail('[^']*')\|detail.php?[^\"' ]*\|sid=[0-9]*" san_result.html san_news.html | sort -u | head -30
for f in san_result.html san_news.html; do python3 - "$f" <<'PY'
import re,sys,html
t=open(sys.argv[1],encoding='utf-8',errors='ignore').read()
t=re.sub(r'<[^>]+>',' ',t); t=html.unescape(t); t=re.sub(r'\s+',' ',t)
print(sys.argv[1], t[:1500])
PY
done
