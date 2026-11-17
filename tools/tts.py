"""VOICEVOX でナレーションの音声を作る。

使い方: python tools/tts.py <依頼JSON> <出力フォルダ>
依頼JSON: [{"id": "s02", "speaker": "横塚", "text": "..."}, ...]
声の割り当て（VOICEVOX のスタイルID）：横塚＝玄野武宏 ノーマル(11)、ナビ＝春日部つむぎ ノーマル(8)
"""
import json
import sys
import time
from pathlib import Path

import requests

VOICE = {"横塚": 11, "ナビ": 8, "コール": 13}
API = "http://127.0.0.1:50021"

for _ in range(60):
    try:
        requests.get(f"{API}/version", timeout=3)
        break
    except Exception:  # noqa: BLE001
        time.sleep(3)

req = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
out = Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)
for item in req:
    sid = VOICE.get(item["speaker"], 11)
    q = requests.post(f"{API}/audio_query", params={"text": item["text"], "speaker": sid}, timeout=60).json()
    q["speedScale"] = item.get("speed", 1.15)
    q["outputSamplingRate"] = 48000
    w = requests.post(f"{API}/synthesis", params={"speaker": sid}, json=q, timeout=120)
    (out / f"{item['id']}.wav").write_bytes(w.content)
    print("ok", item["id"])
