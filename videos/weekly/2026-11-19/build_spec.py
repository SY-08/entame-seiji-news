"""党首回（2026-11-19 公開分）の spec.json・tts.json・台本.md・speakers.json を作り、クリップに話者を付ける。

カード：自民党 高市早苗 総理 × 参政党 神谷宗幣 代表（2026年10月19日 参議院 予算委員会）
お手本は 11/17 回のテンポ：議員の発言は短く、話し手が変わるたびに横塚（実況）かナビ（合いの手・用語）。
"""
import json
from pathlib import Path

D = Path(__file__).parent
CIT = "引用：参議院インターネット審議中継（2026年10月19日 予算委員会）"
JIMIN = {"party": "自民党", "label": "高市早苗 総理", "mark": "自", "color": "#C8102E"}
SANSEI = {"party": "参政党", "label": "神谷宗幣 代表", "mark": "参", "color": "#E8730C"}
BGM_J, BGM_S, BGM_END = "ラリーガ", "マンフト", "ビューティフルゴール"

CLIPS = {
    "x01": ("有村治子", "自由民主党", "予算委員長", 18706.0),
    "k01": ("神谷宗幣", "参政党", "参政党代表", 18786.5),
    "k02": ("神谷宗幣", "参政党", "参政党代表", 18811.0),
    "t01": ("高市早苗", "自由民主党", "内閣総理大臣", 18842.0),
    "t02": ("高市早苗", "自由民主党", "内閣総理大臣", 18890.5),
    "k03": ("神谷宗幣", "参政党", "参政党代表", 18913.0),
    "k04": ("神谷宗幣", "参政党", "参政党代表", 18950.0),
    "k05": ("神谷宗幣", "参政党", "参政党代表", 19349.0),
    "t03": ("高市早苗", "自由民主党", "内閣総理大臣", 19372.0),
    "t04": ("高市早苗", "自由民主党", "内閣総理大臣", 19416.5),
    "k06": ("神谷宗幣", "参政党", "参政党代表", 20946.5),
    "t05": ("高市早苗", "自由民主党", "内閣総理大臣", 20970.0),
}
S, tts = [], []


def studio(i, spk, text, bgm=BGM_S):
    S.append({"id": i, "type": "studio", "speaker": spk, "text": text, "bgm": bgm})
    tts.append({"id": i, "speaker": spk, "text": text})


def clip(i, src, a, b, caption, panel, side, short="", **kw):
    name, party, role, _ = CLIPS[src]
    sc = {"id": i, "type": "clip", "src": f"clips/{src}.mp4", "start": a, "end": b, "short": short,
          "caption": caption, "panel": panel, "side": side, "who": f"{name}（{role}）",
          "bgm": BGM_J if party == "自由民主党" else BGM_S}
    sc.update(kw)
    S.append(sc)
    if kw.get("explain"):
        tts.append({"id": i, "speaker": kw.get("speaker", "横塚"), "text": kw["explain"]})


meta = {
    "file_prefix": "エンタメ政治ニュース_党首回_20261119_自民党高市総理vs参政党神谷代表",
    "format": "党首回（週1）：本編＋ショート1本。ショートは short='前半' の行だけをつなぐ",
    "date_label": "10/19 参議院 予算委員会",
    "card_line1": "自民党 高市早苗 総理",
    "card_line2": "× 参政党 神谷宗幣 代表",
    "theme1": "「経世済民」の筋道はどっち？",
    "theme2": "税・教育・外交の3本勝負",
    "league": "参議院リーグ　予算委員会",
    "left": JIMIN, "right": SANSEI,
    "citation": CIT,
    "card_short": "自民党・高市総理 × 参政党・神谷代表",
    "theme_short": "配る政府？ 手取りを増やす？",
    "house": "参議院", "session": "臨時国会",
    "ticker": "エンタメ政治ニュース ▶ 党首回　｜　自民党 高市早苗 総理 × 参政党 神谷宗幣 代表（10/19 参議院 予算委員会）　｜　テーマ：税の筋道・学校制度・ロシアとの外交　｜　チャンネル登録・グッドボタンよろしくお願いします　｜　ご意見はコメント欄へ　｜　",
    "bgm_rule": "自民＝ラリーガ／参政＝マンフト／総括＝ビューティフルゴール（各シーンの bgm）",
    "thumbnail": {"rule": "タイトルとサムネに「自民党」「高市」と相手の党名・党首名。顔は審議中継からの静止画",
                  "left_face": "thumbs/takaichi_2.jpg（候補 takaichi_1〜3）", "right_face": "thumbs/kamiya_1.jpg（候補 kamiya_1〜3）",
                  "text_big": "自民党 高市総理 vs 参政党 神谷代表", "text_small": "配る政府？ 手取りを増やす？"},
}

# ===== オープニング
S.append({"id": "o01", "type": "call", "text1": "党首回", "text2": "キックオフ！", "bgm": None})
tts.append({"id": "o01", "speaker": "コール", "text": "党首回、キックオフ！"})
studio("o02", "横塚", "エンタメ政治ニュース、党首回！今週のカードは、自民党・高市早苗総理と、参政党・神谷宗幣代表です！")
CARD = {"kind": "tree", "title": "10/19 参議院 予算委員会", "sub": "今週の対戦カード",
        "items": ["自民党 高市早苗 総理", "× 参政党 神谷宗幣 代表", "① 税：配る？ 手取り？", "② 教育：学校制度を見直す？", "③ 外交：ロシアとも対話？"]}
clip("o03", "x01", 1.8, 9.0, "", CARD, "card", explain="舞台は10月19日の参議院予算委員会。テーマは税、教育、外交の3本です！", main_only=True)
studio("o04", "ナビ", "少し前の試合ですが、党首どうしの直接対決。じっくり見ていきましょう。")

# ===== 第1テーマ：税（経世済民の筋道）
studio("a00", "横塚", "第1テーマは税。ボールを持ったのは神谷代表！")
S.append({"id": "a0p", "type": "profile", "src": "clips/k01.mp4", "start": 0.0, "end": 3.0, "bgm": BGM_S,
          "profile": {"party": "参政党", "name": "神谷宗幣", "role": "参政党 代表　参議院議員", "color": SANSEI["color"]}})
P1 = {"kind": "compare", "title": "神谷代表の問い", "rows": [{"label": "集めて配る政府", "text": "税を多く集め、給付で配る"}, {"label": "手取りを増やす政府", "text": "税・保険料を下げて手取りを増やす"}]}
clip("a01", "k01", 0.0, 21.4, "参政党は、税や社会保険料そのものを下げて、国民が使えるお金を増やしたい。政府からの給付がないと生活できない社会は、あまりよくないと考えている", P1, "q")
clip("s01", "k01", 12.6, 21.4, "政府からの給付がないと生活できない社会は、あまりよくないと考えている", P1, "q", short="前半", main=False, theme_short="配る政府？ 手取りを増やす？")
studio("a02", "ナビ", "「経世済民」は、高市総理が所信表明で使った言葉。世の中を治めて、民を救う、という意味です。")
clip("a03", "k02", 2.9, 29.2, "多く集めて配った方がよいのか、なるべく集める税金を少なくして、働いた分の手取りが増える形にした方がいいのか。総理の考える筋道はどちらに重きがあるのか", P1, "q")
studio("a04", "横塚", "さあ、高市総理が答弁席へ！")
S.append({"id": "a0q", "type": "profile", "src": "clips/t01.mp4", "start": 3.0, "end": 6.0, "bgm": BGM_J,
          "profile": {"party": "自民党", "name": "高市早苗", "role": "内閣総理大臣　自民党総裁", "color": JIMIN["color"]}})
PA = {"kind": "answer", "title": "高市総理の答え", "big": "集めすぎず、集めなさすぎず", "quote": "",
      "reason_label": "考え方", "reasons": ["責任ある積極財政で成長", "税収は自然に増える好循環へ", "中・低所得の手取りは増やす"]}
clip("a05", "t01", 2.4, 17.1, "経世済民という言葉を用いたのは、経済の力で国民の暮らしを守り、希望ある未来を切り開くという意味", PA, "a")
clip("a06", "t02", 0.9, 25.6, "税を集めすぎることも、集めなさすぎることもなく、財政の持続可能性も前提に、強い経済と公正な分配をともに実現する。新しい経済財政運営を始めていく", PA, "a",
     note="語尾「始めていくということです」の直後で切る。その後に委員長の呼名「神谷宗幣さん」が入るので25.6秒を超えない")
clip("s02", "t02", 0.9, 22.4, "税を集めすぎることも、集めなさすぎることもなく…強い経済と公正な分配をともに実現する", PA, "a", short="前半", main=False, theme_short="配る政府？ 手取りを増やす？")
studio("a07", "横塚", "どちらか一方ではなく、真ん中にボールを置いた答弁！神谷代表の反応は？")
clip("a08", "k03", 6.4, 18.9, "少し聞いたのと違う角度からの回答だったように思います。どちらにバランスを、という回答だったかと思います", {"kind": "note", "title": "神谷代表の受け止め", "lines": ["聞いたのと違う角度の回答", "「どちらに」より「バランス」"]}, "q")
clip("s03", "k03", 6.4, 11.0, "少し聞いたのと違う角度からの回答だったように思います", None, "q", short="前半", main=False, theme_short="配る政府？ 手取りを増やす？")
P1c = {"kind": "note", "title": "国民負担率（税＋社会保険料）", "lines": ["神谷代表：いま45％ぐらい", "→ 3分の1ぐらいまで下げるべき"]}
clip("a09", "k03", 18.9, 29.0, "国民負担率はいま45%ぐらい。まだ高いので、3分の1ぐらいまで下げていくべきではないか", P1c, "q")
studio("a10", "ナビ", "国民負担率は、所得のうち税金と社会保険料に回る割合のことです。")

# ===== 第2テーマ：教育
studio("b00", "横塚", "第2テーマは教育。神谷代表、ここが一番の得意ゾーン！")
clip("b01", "k04", 0.0, 13.2, "経世済民のために重要なのは、経済政策以上に教育ではないか。参政党は、国の最重要政策は教育だと結党以来訴えてきた", {"kind": "note", "title": "参政党の主張", "lines": ["一番大事なのは教育", "（結党以来の最重要政策）"]}, "q")
studio("b02", "ナビ", "神谷代表は、10歳までは体と心づくり、中学から専門コースも、という案を紹介していました。")
P2 = {"kind": "note", "title": "神谷代表の問い", "lines": ["将来の産業から逆算して", "小・中学校まで含めて", "学校制度を見直すべき？"]}
clip("b03", "k05", 0.0, 23.0, "将来の産業構造から逆算して、小学校・中学校まで含めて学校制度そのもののあり方を再検討する必要があるという意見に、賛成していただけるか", P2, "q")
studio("b04", "横塚", "賛成か、反対か。総理の答えは！")
P2a = {"kind": "answer", "title": "高市総理の答え", "big": "人材育成は重要", "quote": "",
       "reason_label": "取り組み", "reasons": ["高校・高専・大学と産業界で人材育成", "探究的な学び", "ものづくり・科学技術への関心"]}
clip("b05", "t03", 0.1, 9.7, "国力の基盤となるのは人材力。産業構造の転換に応じた人材育成は重要だと思っております", P2a, "a")
clip("b06", "t04", 0.0, 14.4, "グローバル人材やDX・AXなどの人材育成の強化、探究的な学びの充実、ものづくりや科学技術に関心を持つ環境の整備にも取り組んでまいります", P2a, "a")
studio("b07", "ナビ", "学校制度そのものを変えるかどうかには、賛成とも反対とも言っていませんね。")
studio("b08", "横塚", "賛否のジャッジは持ち越し。神谷代表は「次の機会に教育を質問したい」と予告しました！")

# ===== 第3テーマ：外交
studio("c00", "横塚", "試合は終盤。第3テーマは外交、ロシアとの付き合い方！")
P3 = {"kind": "note", "title": "神谷代表の問い", "lines": ["日本の周りにはロシア・中国・北朝鮮", "欧州と同じ立場だけでなく", "ロシアや中国とも対話を"]}
clip("c01", "k06", 0.9, 24.9, "欧州各国と同じ立場をとるだけでなく、ロシアや中国ともしっかり対話をして、地域の安定を目指していく外交が必要ではないか。総理の考えをお聞かせください", P3, "q")
studio("c02", "ナビ", "ここで質問時間がいっぱいに。委員長が「最後に答弁を」と促します。")
P3a = {"kind": "answer", "title": "高市総理の答え", "big": "国際社会と連携", "quote": "",
       "reason_label": "方針", "reasons": ["日本の国益を踏まえる", "ウクライナ支援を続ける", "対ロ制裁にも取り組む"]}
clip("c03", "t05", 0.5, 16.9, "あくまでも日本の国益を踏まえつつ、国際社会とも緊密に連携して、ウクライナ支援及び対ロ制裁に取り組みます", P3a, "a")
studio("c04", "横塚", "ロスタイムの一言は、これまでの路線を続けるという答え。ここでタイムアップ！")

# ===== 総括
SUM = {"kind": "note", "title": "その後どうなった？", "lines": ["税 → 食料品の消費税を2年間下げる法案が審議中", "教育 → 学校制度を変えるかは答えず", "外交 → ウクライナ支援・対ロ制裁を継続"]}
clip("z01", "t01", 17.1, 30.0, "", SUM, "summary", bgm=BGM_END, main_only=True, speaker="横塚",
     explain="振り返りです。税は、どちらか一方ではなくバランスという答え。食料品の消費税を2年間下げる法案は、いま参議院で審議中です。教育は、学校制度を変えるかどうかの答えはなし。外交は、これまでの路線を続けるという答えでした。")
studio("z02", "ナビ", "配る政府か、手取りを増やす政府か。あなたはどっち派ですか？コメントで教えてください！", bgm=BGM_END)
studio("z03", "横塚", "来週も党首どうしの対決を追いかけます！", bgm=BGM_END)
S.append({"id": "z04", "type": "end", "speaker": "横塚", "text": "チャンネル登録とグッドボタン、よろしくお願いします！", "bgm": BGM_END})
tts.append({"id": "z04", "speaker": "横塚", "text": "チャンネル登録とグッドボタン、よろしくお願いします！"})

# ===== ショートのナレーション（short='前半' の前後に入れる）
SHORT_LINES = [
    ("sh1", "横塚", "自民党・高市総理に、参政党・神谷代表が直撃！"),
    ("sh2", "ナビ", "集めて配る政府か、手取りを増やす政府か。総理の答えは？"),
    ("sh3", "横塚", "続きは本編で！概要欄からどうぞ！"),
]
for i, spk, text in SHORT_LINES:
    S.append({"id": i, "type": "studio", "speaker": spk, "text": text, "short": "前半", "main": False, "bgm": BGM_S})
    tts.append({"id": i, "speaker": spk, "text": text})
meta["short_order"] = ["sh1", "s01", "sh2", "s02", "s03", "sh3"]

(D / "spec.json").write_text(json.dumps({"meta": meta, "scenes": S}, ensure_ascii=False, indent=1), encoding="utf-8")
(D / "tts.json").write_text(json.dumps(tts, ensure_ascii=False, indent=1), encoding="utf-8")

# ===== speakers.json
speakers = {
    "episode": "党首回 2026-11-19 公開分",
    "meeting": {"house": "参議院", "name": "予算委員会", "date": "2026-10-19", "sid": 9267,
                "video": "https://sangiin-vod.live.ipcasting.jp/live/dirty/9/2f394551f6a3e68ec7b9ee8ccc764938/index_161315518726326.m3u8",
                "citation": CIT, "chair": "有村治子（予算委員長）"},
    "why": "先週（11/9〜11/13）は党首×高市総理の場面なし（総理出席は11/13 参・消費税特委のみ、質問者に党首なし）。在庫の未使用分で一番新しい党首×高市総理を採用。",
    "questioner": {"name": "神谷宗幣", "kana": "かみや そうへい", "party": "参政党", "category": "党首", "post": "参政党 代表",
                   "category_source": "docs/party_officers.json（参政党 代表：https://kumanichi.com/articles/2038699）",
                   "time_offset": [18708.1, 20998.2], "vod_clock_note": "offset は録画の先頭からの秒"},
    "answerers": [{"name": "高市早苗", "post": "内閣総理大臣（自民党総裁）", "category": "総理", "party": "自由民主党"},
                  {"name": "山下貴司", "post": "法務大臣", "category": "大臣", "note": "万博関係者の難民申請（本編では不使用）"},
                  {"name": "上野賢一郎", "post": "厚生労働大臣", "category": "大臣", "note": "エボラ対策（不使用）"},
                  {"name": "茂木敏充", "post": "外務大臣", "category": "大臣", "note": "花博・ロシア（不使用）"},
                  {"name": "小野田紀美", "post": "経済安全保障担当大臣", "category": "大臣", "note": "外国人受け入れ（不使用）"}],
    "themes": [{"no": 1, "theme": "税：集めて配る政府か、手取りを増やす政府か（経世済民の筋道）", "clips": ["k01", "k02", "t01", "t02", "k03"]},
               {"no": 2, "theme": "教育：学校制度そのものを見直すべきか", "clips": ["k04", "k05", "t03", "t04"]},
               {"no": 3, "theme": "外交：ロシア・中国とも対話する外交を", "clips": ["k06", "t05"]}],
    "unused_in_meeting": ["花博・万博関係者の難民申請（山下法務大臣）", "エボラ出血熱の水際対策（上野厚労大臣）", "外国人労働者の受け入れ枠（山下・小野田大臣）", "ウクライナ支援額（外務省）"],
}
(D / "speakers.json").write_text(json.dumps(speakers, ensure_ascii=False, indent=1), encoding="utf-8")

# ===== クリップに話者を付ける
for cid, (name, party, role, off) in CLIPS.items():
    p = D / "clips" / f"{cid}.json"
    if not p.exists():
        continue
    d = json.loads(p.read_text(encoding="utf-8"))
    rows = d["rows"] if isinstance(d, dict) else d
    p.write_text(json.dumps({"id": cid, "speaker": name, "party": party, "role": role, "vod_offset": off, "source": CIT,
                             "transcript_note": "faster-whisper(small)の自動文字起こし。確定字幕は spec.json の caption。参院の字幕全文は subs/kamiya_1019.txt",
                             "rows": rows}, ensure_ascii=False, indent=1), encoding="utf-8")

# ===== 台本.md
L = ["# 党首回 台本（2026-11-19 公開分）", "",
     "- カード：**自民党 高市早苗 総理 × 参政党 神谷宗幣 代表**（2026年10月19日 参議院 予算委員会）",
     "- 先週（11/9〜11/13）は党首×高市総理の場面がなかったため、在庫の中で一番新しい党首戦を使用",
     f"- {CIT}（全編の画面に常時表示）",
     "- BGM：" + meta["bgm_rule"],
     "- サムネ：左 高市総理 `thumbs/takaichi_2.jpg`、右 神谷代表 `thumbs/kamiya_1.jpg`（候補は各3枚）。文字「自民党 高市総理 vs 参政党 神谷代表」",
     "- タイトル案・概要欄：`youtube.md`", "",
     "## 確認事項", "",
     "- 「国民負担率は45%ぐらい」は神谷代表の発言どおり（「ぐらいですかね」と言っている）。数字の出典は示していない。",
     "- 総括の「食料品の消費税を2年間下げる法案は参議院で審議中」は11/19時点。公開日に状況が変わっていたら直す。",
     "- t02 は終わり際に委員長の呼名が入るので、25.6秒より後ろを使わない。",
     "- 映像は10/19（1か月前）。冒頭で「少し前の試合」と伝えている。", "", "## 本編", ""]
for s in S:
    if s.get("short") or s.get("main") is False:
        continue
    t = s["type"]
    bgm = f"　〔BGM: {s['bgm']}〕" if s.get("bgm") else ""
    if t == "call":
        L.append(f"**{s['id']}** コール「{s['text1']}、{s['text2']}」")
    elif t in ("studio", "end"):
        L.append(f"**{s['id']}** {s['speaker']}「{s['text']}」{bgm}")
    elif t == "profile":
        L.append(f"**{s['id']}** 選手紹介：{s['profile']['name']}（{s['profile']['role']}）{bgm}")
    else:
        line = f"**{s['id']}** 🎥 `{s['src'].split('/')[-1]}` {s['start']}〜{s['end']}秒　{s.get('who', '')}"
        if s.get("caption"):
            line += f"\n　字幕「{s['caption']}」"
        if s.get("explain"):
            line += f"\n　{s.get('speaker', '横塚')}（映像の上で）「{s['explain']}」"
        p = s.get("panel")
        if p:
            if p["kind"] in ("note", "tree"):
                body = " / ".join(p.get("lines", p.get("items", [])))
            elif p["kind"] == "compare":
                body = " / ".join(f"{r['label']}→{r['text']}" for r in p["rows"])
            else:
                body = f"{p['big']}｜" + " / ".join(p["reasons"])
            line += f"\n　図解［{p['title']}］{body}"
        L.append(line + bgm)
    L.append("")
L += ["## ショート（1本・58秒以内）", ""]
tot = 0
by = {s["id"]: s for s in S}
for i in meta["short_order"]:
    s = by[i]
    if s["type"] == "studio":
        L.append(f"- {s['speaker']}「{s['text']}」")
    else:
        dur = s["end"] - s["start"]
        tot += dur
        L.append(f"- 🎥 `{s['src'].split('/')[-1]}` {s['start']}〜{s['end']}秒（{dur:.1f}秒）「{s['caption']}」")
L += [f"- 映像の合計 {tot:.1f}秒＋ナレーション3つ（約12秒）", ""]
(D / "台本.md").write_text("\n".join(L), encoding="utf-8")

clipsec = sum(s["end"] - s["start"] for s in S if s["type"] in ("clip", "profile") and s.get("main", True) and not s.get("short"))
print(len(S), "scenes", f"clip {clipsec:.0f}s voice≈{sum(len(t['text']) for t in tts if not t['id'].startswith('sh'))/7:.0f}s short clips {tot:.1f}s")
