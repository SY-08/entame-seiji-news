"""エンタメ政治ニュースの動画を、台本JSONから書き出す。

使い方: python tools/render.py <台本JSON> <出力フォルダ>

- 本編（1280x720）、ショート前半・後半（1080x1920）の3本を作る。
- 画面の部品は HTML で描いて Playwright で透過PNGにし、ffmpeg で映像・音声と重ねる。
- ナレーション音声は <台本JSONのフォルダ>/tts/<シーンID>.wav を使う。無ければ無音で長さを見積もる。
"""
import html
import json
import subprocess
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
FONT = "'Noto Sans CJK JP','Noto Sans JP',sans-serif"
ORANGE, NAVY, NAVY2, RED, BLUE, PINK, YELLOW = "#F47B20", "#0F1C36", "#16284A", "#D7263D", "#1F5BB5", "#E2477E", "#FFD24A"
FPS = 30

spec_path = Path(sys.argv[1])
OUT = Path(sys.argv[2])
WORK = OUT / "_work"
WORK.mkdir(parents=True, exist_ok=True)
spec = json.loads(spec_path.read_text(encoding="utf-8"))
meta = spec["meta"]
TTS = spec_path.parent / "tts"


import base64


def data_uri(path):
    return "data:image/png;base64," + base64.b64encode(Path(path).read_bytes()).decode()


def esc(s):
    return html.escape(str(s)).replace("\n", "<br>")


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(" ".join(map(str, cmd)))
        print(r.stderr[-2000:])
        raise SystemExit(1)
    return r.stdout


def dur(path):
    return float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)]).strip())


# ---------------------------------------------------------------- 部品（HTML）
BASE_CSS = f"""
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:{FONT};background:transparent;overflow:hidden}}
.abs{{position:absolute}}
.panel{{background:{NAVY};border:3px solid {ORANGE};border-radius:4px;color:#fff}}
.ph{{background:{ORANGE};color:#fff;font-weight:900;padding:6px 14px}}
.y{{color:{YELLOW}}}
"""


def news_label(w, h):
    y = h - 36
    return f'<div class="abs" style="left:0;top:{y}px;width:{w}px;height:36px;background:{NAVY};border-top:2px solid {ORANGE}"></div>' \
           f'<div class="abs" style="left:0;top:{y}px;width:100px;height:36px;background:{RED};color:#fff;font-weight:900;font-size:22px;line-height:36px;text-align:center">NEWS</div>'


def panel_html(p, scale=1.0):
    """補足図解の中身。p['kind'] = tree / compare / answer / note / after"""
    f = lambda px: int(px * scale)  # noqa: E731
    k = p.get("kind", "note")
    head = f'<div class="ph" style="font-size:{f(22)}px">{esc(p.get("title", ""))}</div>'
    body = ""
    if k == "tree":
        rows = ""
        n = len(p["items"])
        for i, it in enumerate(p["items"]):
            mark = "└" if i == n - 1 else "├"
            cur = i == p.get("current", -1)
            st = f"background:{YELLOW};color:{NAVY};" if cur else ""
            tail = "　←今回" if cur else ""
            rows += f'<div style="{st}padding:2px 8px;font-size:{f(20)}px;font-weight:700">{mark} {esc(it)}{tail}</div>'
        body = f'<div style="padding:8px 10px"><div style="color:#9fb3d9;font-size:{f(17)}px;margin-bottom:4px">{esc(p.get("sub",""))}</div>{rows}</div>'
    elif k == "compare":
        rows = ""
        for r in p["rows"]:
            c = r.get("color", "#fff")
            rows += f'<div style="color:{c};font-size:{f(17)}px;font-weight:900;margin-top:6px">{esc(r["label"])}</div>' \
                    f'<div style="font-size:{f(22)}px;font-weight:700;padding-left:8px">{esc(r["text"])}</div>'
        body = f'<div style="padding:6px 14px 12px">{rows}</div>'
    elif k == "answer":
        rs = "".join(f'<div style="font-size:{f(18)}px;padding-left:10px">{esc(x)}</div>' for x in p.get("reasons", []))
        body = f'<div style="padding:8px 14px 12px"><div class="y" style="font-size:{f(28)}px;font-weight:900">{esc(p.get("big",""))}</div>' \
               f'<div style="font-size:{f(20)}px;font-weight:700;margin:4px 0">{esc(p.get("quote",""))}</div>' \
               f'<div style="color:#9fb3d9;font-size:{f(16)}px">{esc(p.get("reason_label","ポイント"))}</div>{rs}</div>'
    else:  # note / after
        ls = "".join(f'<div style="font-size:{f(21)}px;font-weight:700;margin-top:4px">{esc(x)}</div>' for x in p.get("lines", []))
        body = f'<div style="padding:8px 14px 12px">{ls}</div>'
    return head + body


def mini_char(left, top, size):
    face = data_uri(ASSETS / "yoko_face.png")
    return f'<div class="abs" style="left:{left}px;top:{top}px;width:{size}px;height:{size}px;border-radius:50%;overflow:hidden;border:4px solid {ORANGE};background:#fff"><img src="{face}" style="width:100%;height:100%;object-fit:cover"></div>'


def logo(left, top, s=1.0):
    return f'<div class="abs" style="left:{left}px;top:{top}px;background:#fff;border-radius:6px;padding:{int(4*s)}px {int(10*s)}px;line-height:1.05;box-shadow:0 2px 6px rgba(0,0,0,.4)">' \
           f'<div style="color:{ORANGE};font-weight:900;font-size:{int(26*s)}px">エンタメ</div><div style="color:{NAVY};font-weight:900;font-size:{int(20*s)}px">政治ニュース</div></div>'


def main_studio(scene):
    studio = data_uri(ASSETS / "studio.png")
    spk = scene.get("speaker", "横塚")
    col = BLUE if spk == "横塚" else PINK
    th = meta
    return f"""
<div class="abs" style="left:0;top:0;width:1280px;height:720px;background:{NAVY}"></div>
<div class="abs" style="left:0;top:0;width:1280px;height:64px;background:{ORANGE}"></div>
<div class="abs" style="left:32px;top:6px;color:#fff;font-weight:900;font-size:36px">エンタメ政治ニュース</div>
<div class="abs" style="left:420px;top:12px;width:250px;height:40px;background:{NAVY};color:{YELLOW};font-weight:900;font-size:26px;text-align:center;line-height:40px">{esc(scene.get('badge','本日のニュース'))}</div>
<img class="abs" src="{studio}" style="left:20px;top:80px;width:840px;height:472px;border:3px solid #fff">
<div class="abs" style="left:878px;top:78px;width:384px;height:474px;background:{NAVY2}">
  <div class="ph" style="font-size:24px;text-align:center">本日のテーマ</div>
  <div style="color:#c9d6f2;font-size:19px;font-weight:700;text-align:center;margin:8px 0">{esc(th['date_label'])}</div>
  <div style="margin:0 12px;background:#1d3462;padding:4px 0 8px"><span class="ph" style="font-size:15px;padding:2px 10px">対戦</span>
     <div style="color:#fff;font-weight:900;font-size:24px;text-align:center;margin-top:4px">{esc(th['card_line1'])}</div>
     <div class="y" style="font-weight:900;font-size:24px;text-align:center">{esc(th['card_line2'])}</div></div>
  <div style="margin:10px 12px 0;background:#1d3462;padding:4px 0 8px"><span class="ph" style="font-size:15px;padding:2px 10px">テーマ</span>
     <div style="color:#fff;font-weight:900;font-size:23px;text-align:center;margin-top:4px">{esc(th['theme1'])}</div>
     <div class="y" style="font-weight:900;font-size:22px;text-align:center">{esc(th.get('theme2',''))}</div></div>
  <div style="margin:10px 12px 0;background:#1d3462;padding:4px 0 10px"><span class="ph" style="font-size:15px;padding:2px 10px">コーナー</span>
     <div class="y" style="font-weight:900;font-size:40px;text-align:center">デイリー国会</div></div>
</div>
<div class="abs" style="left:18px;top:570px;width:1244px;height:110px;background:#fff;border-radius:2px"></div>
<div class="abs" style="left:18px;top:570px;width:120px;height:110px;background:{col};color:#fff;font-weight:900;font-size:30px;line-height:110px;text-align:center">{esc(spk)}</div>
<div class="abs" style="left:160px;top:570px;width:1090px;height:110px;display:flex;align-items:center;color:{NAVY};font-weight:900;font-size:{30 if len(scene['text'])<=30 else 26}px;line-height:1.35">{esc(scene['text'])}</div>
{news_label(1280, 720)}
"""


def main_call(scene):
    return f"""
<div class="abs" style="left:0;top:0;width:1280px;height:720px;background:radial-gradient(circle at 50% 45%,#22407a,{NAVY} 70%)"></div>
<div class="abs" style="left:0;top:210px;width:1280px;text-align:center;color:#fff;font-weight:900;font-size:120px;letter-spacing:12px;text-shadow:0 6px 0 {RED}">{esc(scene['text1'])}</div>
<div class="abs" style="left:0;top:380px;width:1280px;text-align:center;color:{YELLOW};font-weight:900;font-size:110px;letter-spacing:8px;text-shadow:0 6px 0 {ORANGE}">{esc(scene['text2'])}</div>
"""


def main_matchup(scene):
    L, R = meta["left"], meta["right"]
    return f"""
<div class="abs" style="left:0;top:14px;width:1280px;text-align:center;color:#fff;font-weight:900;font-size:30px;text-shadow:0 2px 6px #000">{esc(meta['league'])}</div>
<div class="abs" style="left:40px;top:62px;width:520px;height:96px;background:rgba(10,18,36,.85);border-radius:48px"></div>
<div class="abs" style="left:34px;top:54px;width:112px;height:112px;border-radius:50%;background:#fff;display:flex;align-items:center;justify-content:center"><div style="width:92px;height:92px;border-radius:50%;background:{L['color']};color:#fff;font-weight:900;font-size:54px;text-align:center;line-height:92px">{esc(L['mark'])}</div></div>
<div class="abs" style="left:170px;top:88px;color:{L['color']};font-weight:900;font-size:28px">{esc(L['label'])}</div>
<div class="abs" style="left:250px;top:66px;width:300px;text-align:center;color:#fff;font-weight:900;font-size:60px">{esc(L['party'])}</div>
<div class="abs" style="left:590px;top:40px;color:#fff;font-weight:300;font-size:130px;line-height:130px">×</div>
<div class="abs" style="left:720px;top:62px;width:520px;height:96px;background:rgba(10,18,36,.85);border-radius:48px"></div>
<div class="abs" style="left:1134px;top:54px;width:112px;height:112px;border-radius:50%;background:#fff;display:flex;align-items:center;justify-content:center"><div style="width:92px;height:92px;border-radius:50%;background:{R['color']};color:#fff;font-weight:900;font-size:54px;text-align:center;line-height:92px">{esc(R['mark'])}</div></div>
<div class="abs" style="left:760px;top:88px;color:{R['color']};font-weight:900;font-size:28px">{esc(R['label'])}</div>
<div class="abs" style="left:830px;top:66px;width:300px;text-align:center;color:#fff;font-weight:900;font-size:60px">{esc(R['party'])}</div>
"""


def main_profile(scene):
    p = scene["profile"]
    return f"""
<div class="abs" style="left:640px;top:0;width:640px;height:684px;background:linear-gradient(90deg,rgba(255,255,255,0),rgba(255,255,255,.93) 22%)"></div>
<div class="abs" style="left:760px;top:170px;width:120px;height:44px;background:{p.get('color',ORANGE)};color:#fff;font-weight:900;font-size:26px;text-align:center;line-height:44px">{esc(p['party'])}</div>
<div class="abs" style="left:760px;top:226px;color:{NAVY};font-weight:900;font-size:120px;line-height:1.1;-webkit-text-stroke:2px {NAVY}">{esc(p['name'])}</div>
<div class="abs" style="left:760px;top:396px;width:440px;border-top:3px solid {NAVY};padding-top:12px;color:{NAVY};font-weight:700;font-size:26px">{esc(p['role'])}</div>
{news_label(1280, 720)}
"""


def main_overlay(scene):
    """国会映像の上に重ねる部品（映像は透明部分から見える）"""
    parts = [news_label(1280, 720)]
    if scene.get("matchup"):
        parts.append(main_matchup(scene))
    if scene.get("panel"):
        top = 180 if scene.get("matchup") else 30
        parts.append(f'<div class="abs panel" style="left:30px;top:{top}px;width:380px">{panel_html(scene["panel"])}</div>')
    parts.append(logo(8, 470, 1.0))
    parts.append(mini_char(150, 520, 140))
    if scene.get("caption"):
        cap = scene["caption"]
        parts.append(f'<div class="abs" style="left:430px;top:574px;width:820px;min-height:60px;background:rgba(0,0,0,.72);color:#fff;font-weight:700;font-size:26px;padding:10px 18px;border-radius:4px;line-height:1.4">{esc(cap)}</div>')
    if scene.get("explain"):
        parts.append(f'<div class="abs" style="left:430px;top:540px;width:820px;background:#fff;border-left:10px solid {BLUE};color:{NAVY};font-weight:900;font-size:28px;padding:12px 18px;line-height:1.4"><div style="color:{BLUE};font-size:18px">横塚の解説</div>{esc(scene["explain"])}</div>')
    parts.append(f'<div class="abs" style="right:14px;top:652px;color:#fff;font-size:15px;text-shadow:0 1px 3px #000">{esc(meta["citation"])}</div>')
    return "".join(parts)


def main_end(scene):
    s = dict(scene)
    s.setdefault("speaker", "ナビ")
    base = main_studio(s)
    # 右パネルを「お知らせ」に差し替え
    cta = f"""
<div class="abs" style="left:878px;top:78px;width:384px;height:474px;background:{NAVY2}">
 <div class="ph" style="font-size:24px;text-align:center;background:{RED}">INFORMATION ｜ お知らせ</div>
 <div style="margin:22px 26px 0;height:64px;background:#555;color:#fff;font-weight:900;font-size:26px;text-align:center;line-height:64px">✓ 登録済み 🔔</div>
 <div style="margin:16px 26px 0;height:64px;background:{BLUE};color:#fff;font-weight:900;font-size:26px;text-align:center;line-height:64px">グッドボタン</div>
 <div style="margin:16px 26px 0;height:64px;background:#2e9e4f;color:#fff;font-weight:900;font-size:26px;text-align:center;line-height:64px">コメントでご意見を</div>
 <div class="y" style="margin-top:34px;text-align:center;font-weight:900;font-size:40px">また次回！</div>
</div>"""
    return base + cta


# ---- ショート（1080x1920）
def short_overlay(scene, half):
    p = []
    p.append(f'<div class="abs" style="left:0;top:0;width:1080px;height:240px;background:{NAVY}"></div>')
    p.append(f'<div class="abs" style="left:0;top:848px;width:1080px;height:1072px;background:{NAVY}"></div>')
    p.append(f'<div class="abs" style="left:0;top:0;width:1080px;height:70px;background:{ORANGE};color:#fff;font-weight:900;font-size:34px;text-align:center;line-height:70px">エンタメ政治ニュース ｜ デイリー国会</div>')
    p.append(f'<div class="abs" style="left:30px;top:90px;width:1020px;height:70px;background:{RED};color:#fff;font-weight:900;font-size:40px;text-align:center;line-height:70px">{esc(meta["card_short"])}</div>')
    p.append(f'<div class="abs" style="left:30px;top:172px;width:150px;height:52px;background:{ORANGE};color:#fff;font-weight:900;font-size:30px;text-align:center;line-height:52px">{esc(half)}戦</div>')
    p.append(f'<div class="abs" style="left:200px;top:172px;width:850px;color:{YELLOW};font-weight:900;font-size:34px;line-height:52px">{esc(meta["theme_short"])}</div>')
    # 映像枠（240〜848）は透明
    if scene.get("caption"):
        p.append(f'<div class="abs" style="left:30px;top:880px;width:1020px;background:#000;color:#fff;font-weight:700;font-size:40px;padding:16px 24px;border-radius:6px;text-align:center;line-height:1.45">{esc(scene["caption"])}</div>')
    if scene.get("panel"):
        p.append(f'<div class="abs panel" style="left:30px;top:{1060 if scene.get("caption") else 900}px;width:720px">{panel_html(scene["panel"], 1.6)}</div>')
    if scene.get("explain"):
        p.append(f'<div class="abs" style="left:30px;top:900px;width:1020px;background:#fff;border-left:14px solid {BLUE};color:{NAVY};font-weight:900;font-size:44px;padding:20px 26px;line-height:1.45"><div style="color:{BLUE};font-size:28px">横塚の解説</div>{esc(scene["explain"])}</div>')
    p.append(logo(790, 1420, 1.5))
    p.append(mini_char(800, 1530, 230))
    p.append(f'<div class="abs" style="left:0;top:1868px;width:1080px;height:52px;background:{NAVY};border-top:3px solid {ORANGE}"></div><div class="abs" style="left:0;top:1868px;width:150px;height:52px;background:{RED};color:#fff;font-weight:900;font-size:30px;line-height:52px;text-align:center">NEWS</div>')
    p.append(f'<div class="abs" style="right:16px;top:812px;color:#fff;font-size:20px;text-shadow:0 1px 3px #000">{esc(meta["citation"])}</div>')
    return "".join(p)


def short_title():
    return f"""
<div class="abs" style="left:0;top:0;width:1080px;height:1920px;background:{NAVY}"></div>
<div class="abs" style="left:0;top:640px;width:1080px;text-align:center;color:#fff;font-weight:900;font-size:52px">エンタメ政治ニュース</div>
<div class="abs" style="left:0;top:720px;width:1080px;text-align:center;color:{ORANGE};font-weight:900;font-size:130px">デイリー国会</div>
<div class="abs" style="left:0;top:930px;width:1080px;height:90px;background:{RED};color:#fff;font-weight:900;font-size:46px;text-align:center;line-height:90px">{esc(meta['house'])} {esc(meta['session'])}リーグ</div>
"""


def short_end():
    studio = data_uri(ASSETS / "studio.png")
    return f"""
<div class="abs" style="left:0;top:0;width:1080px;height:1920px;background:{NAVY}"></div>
<div class="abs" style="left:0;top:0;width:1080px;height:300px;background:#fff"></div>
<div class="abs" style="left:0;top:40px;width:1080px;text-align:center;color:{ORANGE};font-weight:900;font-size:110px;line-height:1">エンタメ</div>
<div class="abs" style="left:0;top:160px;width:1080px;text-align:center;color:{NAVY};font-weight:900;font-size:96px;line-height:1">政治ニュース</div>
<img class="abs" src="{studio}" style="left:30px;top:340px;width:1020px;height:573px;border:4px solid #fff">
<div class="abs" style="left:30px;top:960px;width:1020px;height:150px;background:#fff;display:flex;align-items:center"><div style="width:150px;height:150px;background:{BLUE};color:#fff;font-weight:900;font-size:40px;line-height:150px;text-align:center">横塚</div><div style="padding:0 24px;color:{NAVY};font-weight:900;font-size:40px">この続きは、本編で詳しく解説しています！</div></div>
<div class="abs" style="left:60px;top:1180px;width:960px;height:220px;background:{RED};border-radius:10px;color:#fff;text-align:center"><div style="font-weight:900;font-size:80px;margin-top:22px">続きは 本編で！</div><div style="font-weight:700;font-size:40px;color:{YELLOW}">▼ 概要欄の本編をご覧ください ▼</div></div>
"""


# ---------------------------------------------------------------- 画像化
def shoot(page, inner, w, h, name):
    page.set_viewport_size({"width": w, "height": h})
    page.set_content(f"<html><head><style>{BASE_CSS}</style></head><body style='width:{w}px;height:{h}px'>{inner}</body></html>")
    page.wait_for_timeout(80)
    path = WORK / f"{name}.png"
    page.screenshot(path=str(path), omit_background=True)
    return path


def tts_for(scene, fallback_text):
    wav = TTS / f"{scene['id']}.wav"
    if wav.exists():
        return wav, dur(wav)
    est = max(1.6, len(fallback_text) * 0.14 + 0.5)
    return None, est


def seg_still(png, d, wav, w, h, name):
    out = WORK / f"{name}.mp4"
    cmd = ["ffmpeg", "-v", "error", "-y", "-loop", "1", "-framerate", str(FPS), "-t", f"{d:.3f}", "-i", str(png)]
    if wav:
        cmd += ["-i", str(wav), "-filter_complex", f"[1:a]apad,atrim=0:{d:.3f},aresample=48000[a]", "-map", "0:v", "-map", "[a]"]
    else:
        cmd += ["-f", "lavfi", "-t", f"{d:.3f}", "-i", "anullsrc=r=48000:cl=stereo", "-map", "0:v", "-map", "1:a"]
    cmd += ["-vf", f"scale={w}:{h},format=yuv420p", "-r", str(FPS), "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
            "-c:a", "aac", "-ar", "48000", "-ac", "2", "-shortest", str(out)]
    run(cmd)
    return out


def seg_clip(scene, overlay, w, h, name, vbox):
    """vbox: (x, y, vw, vh) 映像を置く位置。overlay は上に重ねる透過PNG。"""
    src = spec_path.parent / scene["src"]
    s, e = scene["start"], scene["end"]
    d = e - s
    x, y, vw, vh = vbox
    out = WORK / f"{name}.mp4"
    wav = None
    if scene.get("explain"):
        wav, d2 = tts_for(scene, scene["explain"])
        d = max(d2 + 0.4, 1.5) if scene.get("fit_to_voice", True) else d
    fc = f"color=c={NAVY}:s={w}x{h}:r={FPS}[bg];[0:v]scale={vw}:{vh}:force_original_aspect_ratio=increase,crop={vw}:{vh},setsar=1[v];" \
         f"[bg][v]overlay={x}:{y}:shortest=1[b];[b][1:v]overlay=0:0,format=yuv420p[vo]"
    cmd = ["ffmpeg", "-v", "error", "-y", "-ss", f"{s:.3f}", "-t", f"{d:.3f}", "-i", str(src), "-loop", "1", "-i", str(overlay)]
    if wav:
        cmd += ["-i", str(wav)]
        fc += f";[0:a]volume=0.15,aresample=48000[bgm];[2:a]aresample=48000,apad[vo_a];[bgm][vo_a]amix=inputs=2:duration=first:normalize=0[a]"
    else:
        fc += ";[0:a]aresample=48000,volume=1.0[a]"
    cmd += ["-filter_complex", fc, "-map", "[vo]", "-map", "[a]", "-t", f"{d:.3f}", "-r", str(FPS), "-c:v", "libx264", "-preset", "veryfast",
            "-crf", "20", "-c:a", "aac", "-ar", "48000", "-ac", "2", str(out)]
    run(cmd)
    return out


def concat(parts, out):
    lst = WORK / (out.stem + "_list.txt")
    lst.write_text("".join(f"file '{p.resolve()}'\n" for p in parts), encoding="utf-8")
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
         "-c:a", "aac", "-ar", "48000", "-ac", "2", "-movflags", "+faststart", str(out)])
    return out


def add_ticker(src, out, w, h, bar_h, label_w, text, skip_ranges):
    """NEWS の横を流れるテロップを全体にかける（冒頭コールなどは除く）"""
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page()
        fs = int(bar_h * 0.62)
        strip = shoot(pg, f'<div style="white-space:nowrap;color:#fff;font-weight:700;font-size:{fs}px;line-height:{bar_h}px;padding-left:40px">{esc(text)}</div>',
                      len(text) * fs + 200, bar_h, out.stem + "_ticker")
        b.close()
    sw = int(run(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", "stream=width", "-of", "csv=p=0", str(strip)]).strip())
    en = "*".join(f"not(between(t,{a:.2f},{b:.2f}))" for a, b in skip_ranges) or "1"
    speed = 110 if w == 1280 else 140
    # テロップを流したあと、NEWS ラベルの部分を元の映像で上書きしてラベルの下に潜らせる
    fc = (f"[0:v]split[a][b];[1:v]format=rgba[t];[a][t]overlay=x='{label_w}+{w}-mod(t*{speed},{sw}+{w})':y={h - bar_h + 2}:enable='{en}'[m];"
          f"[b]crop={label_w}:{bar_h}:0:{h - bar_h}[lab];[m][lab]overlay=0:{h - bar_h}[o]")
    run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-loop", "1", "-i", str(strip), "-filter_complex", fc, "-map", "[o]", "-map", "0:a",
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-c:a", "copy", "-shortest", "-movflags", "+faststart", str(out)])


# ---------------------------------------------------------------- 組み立て
def build():
    main_parts, short_parts = [], {"前半": [], "後半": []}
    skip_main, t_main = [], 0.0
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page()
        sh_title = shoot(pg, short_title(), 1080, 1920, "short_title")
        sh_end = shoot(pg, short_end(), 1080, 1920, "short_end")
        for sc in spec["scenes"]:
            sid, typ = sc["id"], sc["type"]
            halves = [h for h in ("前半", "後半") if h in sc.get("short", "")]
            if typ == "call":
                png = shoot(pg, main_call(sc), 1280, 720, sid)
                wav, d = tts_for(sc, sc["text1"] + sc["text2"])
                d = max(d + 0.3, 1.8)
                seg = seg_still(png, d, wav, 1280, 720, sid)
                skip_main.append((t_main, t_main + d))
            elif typ in ("studio", "end"):
                html_ = main_end(sc) if typ == "end" else main_studio(sc)
                png = shoot(pg, html_, 1280, 720, sid)
                wav, d = tts_for(sc, sc["text"])
                d += 0.35
                seg = seg_still(png, d, wav, 1280, 720, sid)
            elif typ == "profile":
                ov = shoot(pg, main_profile(sc), 1280, 720, sid)
                seg = seg_clip(sc, ov, 1280, 720, sid, (0, 0, 1280, 720))
            else:  # clip
                ov = shoot(pg, main_overlay(sc), 1280, 720, sid)
                seg = seg_clip(sc, ov, 1280, 720, sid, (0, 0, 1280, 720))
            main_parts.append(seg)
            t_main += dur(seg)
            for h in halves:
                if typ == "clip" or typ == "profile":
                    ov = shoot(pg, short_overlay(sc, h), 1080, 1920, f"{sid}_s{h}")
                    short_parts[h].append(seg_clip(sc, ov, 1080, 1920, f"{sid}_s{h}", (0, 240, 1080, 608)))
        b.close()
    OUT.mkdir(parents=True, exist_ok=True)
    raw = concat(main_parts, WORK / "main_raw.mp4")
    main_out = OUT / f"{meta['file_prefix']}_デイリー版本編.mp4"
    add_ticker(raw, main_out, 1280, 720, 36, 100, meta["ticker"], skip_main)
    results = [main_out]
    for h in ("前半", "後半"):
        if not short_parts[h]:
            continue
        t = seg_still(sh_title, 1.5, None, 1080, 1920, f"short_title_{h}")
        e = seg_still(sh_end, 3.0, None, 1080, 1920, f"short_end_{h}")
        raw = concat([t] + short_parts[h] + [e], WORK / f"short_{h}_raw.mp4")
        o = OUT / f"{meta['file_prefix']}_ショート{h}.mp4"
        add_ticker(raw, o, 1080, 1920, 52, 150, meta["ticker"], [(0, 1.5)])
        results.append(o)
    for r in results:
        print(r, f"{dur(r):.1f}s")


build()
