D=live/$(date +%F)/sangiin/subtitles
python3 tools/fetch_vtt.py houmu cpl6ndumbb93lo02j6gg dbtb1u0lufuc710sri2g $D
python3 tools/fetch_vtt.py naikaku cpl6oed632pig7l1fg0g dbtb210lufuc710sri30 $D
python3 tools/fetch_vtt.py keisan cpl6m9d632pu6i7ccg70 dbtb1tjl80ds71s5u9f0 $D
cp -r live "$OUT/"
