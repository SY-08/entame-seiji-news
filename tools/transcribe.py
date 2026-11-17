"""収録した区切りファイル（10分ごと）を順に文字起こしする。

使い方: python tools/transcribe.py <録画フォルダ> <文字起こしの出力フォルダ>
ファイル名 seg_HHMMSS.ts の HHMMSS を開始時刻（日本時間）として、発言ごとの時刻を付ける。
まだ書き込み中の最新ファイルは飛ばす。すでに文字起こし済みのものも飛ばす。
"""
import json
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

from faster_whisper import WhisperModel

rec = Path(sys.argv[1])
out = Path(sys.argv[2])
final = len(sys.argv) > 3 and sys.argv[3] == "final"
out.mkdir(parents=True, exist_ok=True)

segs = sorted(rec.glob("seg_*.ts"))
if not final:
    segs = segs[:-1]  # 最新は書き込み中
todo = [s for s in segs if not (out / (s.stem + ".json")).exists() and s.stat().st_size > 100_000]
if not todo:
    print("nothing to do")
    sys.exit(0)

model = WhisperModel("small", device="cpu", compute_type="int8", cpu_threads=3)
for s in todo:
    wav = s.with_suffix(".wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(s), "-ac", "1", "-ar", "16000", str(wav)], check=True)
    import os
    num = s.stem[4:]
    if len(num) == 3 and os.environ.get("START_CLOCK"):
        h0, m0, s0 = map(int, os.environ["START_CLOCK"].split(":"))
        base = datetime(2000, 1, 1, h0, m0, s0) + timedelta(seconds=600 * int(num))
    else:
        base = datetime(2000, 1, 1, int(num[0:2]), int(num[2:4]), int(num[4:6]))
    import numpy as np
    pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", str(wav), "-f", "f32le", "-ac", "1", "-ar", "16000", "-"], capture_output=True, check=True).stdout
    audio = np.frombuffer(pcm, dtype=np.float32)
    segments, _ = model.transcribe(audio, language="ja", beam_size=1, vad_filter=True)
    rows = []
    for g in segments:
        t0 = base + timedelta(seconds=g.start)
        rows.append({"file": s.name, "start": round(g.start, 2), "end": round(g.end, 2),
                     "clock": t0.strftime("%H:%M:%S"), "text": g.text.strip()})
    (out / (s.stem + ".json")).write_text(json.dumps(rows, ensure_ascii=False, indent=0), encoding="utf-8")
    (out / (s.stem + ".txt")).write_text("\n".join(f"[{r['clock']}] {r['text']}" for r in rows), encoding="utf-8")
    wav.unlink()
    print("done", s.name, len(rows))
