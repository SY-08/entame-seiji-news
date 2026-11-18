"""切り出し指示（cuts.json）に従って、国会映像から発言部分を切り出し、文字起こしも付ける。

使い方: python tools/cut.py <cuts.json> <出力フォルダ> [録画フォルダ]
cuts.json:
{"sources": {"houmu": {"type": "files", "dir": "rec_houmu", "start": "09:30:01"},
             "naikaku": {"type": "dvr", "ch": "...", "lh": "..."}},
 "cuts": [{"id": "c01", "src": "houmu", "from": "10:12:30", "to": "10:13:20"}]}
- files: 10分ごとの録画ファイル（seg_000.ts...）から切る。start は seg_000 の開始時刻。
- dvr: 参議院の巻き戻し配信から直接切る（会議終了後2時間まで）。
"""
import json
import re
import subprocess
import sys
import urllib.parse
from datetime import datetime
from pathlib import Path

import numpy as np
import requests

spec = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
out = Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/130.0 Safari/537.36"
REF = "https://www.webtv.sangiin.go.jp/"


def sec(clock):
    h, m, s = map(int, clock.split(":"))
    return h * 3600 + m * 60 + s


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-1500:])
    return r


def cut_files(src, c, dst):
    st = sec(src["start"])
    a, b = sec(c["from"]) - st, sec(c["to"]) - st
    d = Path(src["dir"])
    first, last = int(a // 600), int(b // 600)
    files = [d / f"seg_{i:03d}.ts" for i in range(first, last + 1) if (d / f"seg_{i:03d}.ts").exists()]
    lst = dst.with_suffix(".txt")
    lst.write_text("".join(f"file '{f.resolve()}'\n" for f in files))
    off = a - first * 600
    return ["-f", "concat", "-safe", "0", "-i", str(lst), "-ss", f"{off:.2f}", "-t", f"{b - a:.2f}"]


def cut_dvr(src, c, dst):
    base = f"https://sangiin-live.live.ipcasting.jp/live/{src['ch']}.h/{src['lh']}/"
    info = requests.get(base + "channel-info.json", headers={"User-Agent": UA, "Referer": REF}, timeout=30).json()
    start = datetime.fromisoformat(info["schedules"][0]["status"]["program_start"])
    master = requests.get(base + "index.m3u8", headers={"User-Agent": UA, "Referer": REF}, timeout=30).text
    variants = re.findall(r"RESOLUTION=(\d+)x(\d+)[^\n]*\n([^\n]+)", master)
    best = max(variants, key=lambda v: int(v[0]))[2]
    vurl = urllib.parse.urljoin(base, best)
    pl = requests.get(vurl, headers={"User-Agent": UA, "Referer": REF}, timeout=30).text
    durs = [float(x) for x in re.findall(r"#EXTINF:([\d.]+)", pl)]
    segdur = sum(durs) / len(durs)
    a = sec(c["from"]) - (start.hour * 3600 + start.minute * 60 + start.second)
    b = sec(c["to"]) - (start.hour * 3600 + start.minute * 60 + start.second)
    idx = max(0, int(a // segdur) - 1)
    off = a - idx * segdur
    return ["-user_agent", UA, "-headers", f"Referer: {REF}", "-live_start_index", str(idx), "-i", vurl,
            "-ss", f"{off:.2f}", "-t", f"{b - a:.2f}"]


def cut_hls(src, c, dst):
    """衆議院のビデオライブラリなど、会議のはじめから始まる録画（m3u8）から切る。start は録画の開始時刻"""
    if "from_sec" in c:  # discover_shugiin.py の offset（録画の先頭からの秒）で指定
        a, b = float(c["from_sec"]), float(c["to_sec"])
    else:
        a, b = sec(c["from"]) - sec(src["start"]), sec(c["to"]) - sec(src["start"])
    return ["-user_agent", UA, "-headers", "Referer: https://www.shugiintv.go.jp/", "-ss", f"{a:.2f}", "-i", src["url"], "-t", f"{b - a:.2f}"]


model = None
for c in spec["cuts"]:
    src = spec["sources"][c["src"]]
    dst = out / f"{c['id']}.mp4"
    inp = {"files": cut_files, "dvr": cut_dvr, "hls": cut_hls}[src["type"]](src, c, dst)
    r = run(["ffmpeg", "-v", "error", "-y", *inp, "-vf", "scale=1280:720:flags=lanczos,setsar=1", "-r", "30",
             "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-c:a", "aac", "-ar", "48000", "-ac", "2",
             "-movflags", "+faststart", str(dst)])
    if r.returncode != 0 or not dst.exists():
        print("FAILED", c["id"])
        continue
    # 文字起こし（字幕づくり用）
    if model is None:
        from faster_whisper import WhisperModel
        model = WhisperModel("small", device="cpu", compute_type="int8")
    pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", str(dst), "-f", "f32le", "-ac", "1", "-ar", "16000", "-"],
                         capture_output=True, check=True).stdout
    segs, _ = model.transcribe(np.frombuffer(pcm, dtype=np.float32), language="ja", beam_size=5, vad_filter=True)
    rows = [{"start": round(g.start, 2), "end": round(g.end, 2), "text": g.text.strip()} for g in segs]
    (out / f"{c['id']}.json").write_text(json.dumps(rows, ensure_ascii=False, indent=0), encoding="utf-8")
    print("ok", c["id"], len(rows))
