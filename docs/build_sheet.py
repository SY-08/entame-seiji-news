from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.utils import get_column_letter

FONT = "Arial"
HEAD_FILL = PatternFill("solid", fgColor="1F3A5F")
SEC_FILL = PatternFill("solid", fgColor="DCE6F1")
INPUT_FILL = PatternFill("solid", fgColor="FFF2CC")
BIG_FILLS = {
    "A": "FDE9D9", "B": "FCE4D6", "C": "E2EFDA", "D": "DDEBF7",
    "E": "EDEDED", "F": "E4DFEC", "G": "FFF2CC",
}
thin = Side(style="thin", color="BFBFBF")
BORDER = Border(left=thin, right=thin, top=thin, bottom=thin)

wb = Workbook()


def style_header(ws, row, ncol):
    for c in range(1, ncol + 1):
        cell = ws.cell(row=row, column=c)
        cell.font = Font(name=FONT, bold=True, color="FFFFFF")
        cell.fill = HEAD_FILL
        cell.alignment = Alignment(vertical="center", wrap_text=True)
        cell.border = BORDER


def write_table(ws, start_row, headers, rows, widths=None):
    for i, h in enumerate(headers, 1):
        ws.cell(row=start_row, column=i, value=h)
    style_header(ws, start_row, len(headers))
    for r, row in enumerate(rows, start_row + 1):
        for c, v in enumerate(row, 1):
            cell = ws.cell(row=r, column=c, value=v)
            cell.font = Font(name=FONT)
            cell.alignment = Alignment(vertical="top", wrap_text=True)
            cell.border = BORDER
    if widths:
        for i, w in enumerate(widths, 1):
            ws.column_dimensions[get_column_letter(i)].width = w
    return start_row + len(rows) + 1


def title(ws, text, sub=None):
    ws["A1"] = text
    ws["A1"].font = Font(name=FONT, bold=True, size=16)
    if sub:
        ws["A2"] = sub
        ws["A2"].font = Font(name=FONT, size=10, color="595959")


def section(ws, row, text, ncol):
    ws.cell(row=row, column=1, value=text)
    for c in range(1, ncol + 1):
        ws.cell(row=row, column=c).fill = SEC_FILL
    ws.cell(row=row, column=1).font = Font(name=FONT, bold=True, size=12)
    return row + 1


# ---------------- 00_使い方 ----------------
ws = wb.active
ws.title = "00_使い方"
title(ws, "マンデー国会 論点地図", "作成: 2026-11-10 ／ 第222回国会（臨時会）会期中")
rows = [
    ["01_国会の基本構造", "国会で起きることを「決める（議案）」と「ただす（質疑）」に分け、賛成・反対・修正案・対案の関係を整理", "まず最初に読む"],
    ["02_地図", "政治テーマを大項目（7）→中項目→小項目（論点）の3階層で整理。全タブの分類の元", "分類に迷ったらここ。小項目IDだけ覚えればよい"],
    ["03_今国会の議案", "第222回国会で扱われている主な議案と現在地、出典", "毎日更新"],
    ["04_記録", "毎日の出来事を1行1件で記録。小項目IDを選ぶと大・中項目が自動で入る", "黄色のセルが入力欄"],
    ["05_ストーリー構成", "論点ごとに動画のシーン割りを作る。どのシーンでどの記録（発言）を使うかを決める", "動画を作る前に書く"],
    ["06_発言カット", "ストーリーで必要になった発言を、映像のどこから切るかの一覧", "頭出し時刻・開始秒は自動化で埋める予定"],
    ["07_ズレ地図", "2つ目の整理。「誰が決めるか × どこに影響が出るか」の表で、国・都道府県・市区町村の間のズレを見る", "08で付けたタグが自動で集計される"],
    ["08_ズレ記録", "テーマごとに「決める場所」「影響が出る場所」「起点（上げる・下ろす）」をタグ付けする", "黄色のセルが入力欄。完結かズレかは自動判定"],
    ["09_地域マスタ", "47都道府県と、扱う市区町村の一覧（議会名・関わっている地方議員）", "市区町村を扱うたびに1行追加"],
    ["99_リスト", "プルダウンの選択肢", "原則さわらない"],
]
r = write_table(ws, 4, ["タブ", "役割", "使い方"], rows, [22, 70, 40])
r += 1
ws.cell(row=r, column=1, value="流れ").font = Font(name=FONT, bold=True)
ws.cell(row=r + 1, column=1, value="02_地図で論点を決める → 04_記録に毎日書く → 05_ストーリー構成でシーンを組む → 06_発言カットで映像を切る → 動画")
ws.cell(row=r + 1, column=1).font = Font(name=FONT)
ws.cell(row=r + 3, column=1, value="凡例").font = Font(name=FONT, bold=True)
ws.cell(row=r + 4, column=1, value="黄色セル").fill = INPUT_FILL
ws.cell(row=r + 4, column=2, value="人（または自動リサーチ）が入力する欄。白いセルは数式で自動表示")
for c in (1, 2):
    ws.cell(row=r + 4, column=c).font = Font(name=FONT)

# ---------------- 01_国会の基本構造 ----------------
ws = wb.create_sheet("01_国会の基本構造")
title(ws, "国会の基本構造", "国会は「決める」と「ただす」の2つをやっている。テレビで見る代表質問の多くは「ただす」側")
NC = 5
r = section(ws, 4, "① 国会でやっていることは2種類", NC)
r = write_table(ws, r, ["種類", "中身", "結果", "賛否が出るか", "例（今国会）"], [
    ["決める（議案）", "法律・予算・条約などを審議して採決する", "可決／否決／継続審議／廃案", "出る（各党が賛成・反対）", "食料品の消費税減税法案"],
    ["ただす（質疑）", "政府に質問して考えや事実を明らかにする", "答弁（約束・拒否・検討）", "出ない（採決しない）", "10/9 参院代表質問 神谷代表の質問"],
], [20, 46, 30, 26, 36])
r += 1
r = section(ws, r, "② 議案の種類", NC)
r = write_table(ws, r, ["議案", "誰が出すか", "中身", "賛否の対象", "例"], [
    ["内閣提出法律案（閣法）", "内閣（政府）", "政府が作った法律案。成立する法律の多くはこれ", "○", "食料品の消費税減税関連法案"],
    ["衆法・参法（議員立法）", "国会議員（衆議院・参議院）", "与党・野党の議員が作った法律案。野党の「対案」もここに入る", "○", "衆院議員定数削減法案、政治資金規正法改正案"],
    ["予算・補正予算", "内閣", "国の1年間のお金の使い方。補正は年度途中の追加", "○", "2026年度補正予算（6月成立）"],
    ["条約", "内閣", "外国と結ぶ約束の承認", "○", "今国会に条約承認案1本の予定"],
    ["決議案", "議員", "国会としての意思表示。内閣不信任決議案もここ", "○", "―"],
], None)
r += 1
r = section(ws, r, "③ 法案に対する各党の態度", NC)
r = write_table(ws, r, ["態度", "意味", "原案との関係", "よくある組み合わせ", "注意点"], [
    ["賛成", "原案のまま賛成", "原案に乗る", "附帯決議を付けて賛成", "―"],
    ["反対", "原案に反対", "原案を否定", "対案を出して反対", "「何に反対か」を必ず書く"],
    ["修正案を出す", "原案の一部を書き換える提案", "原案にくっつく（原案の改良）", "修正が通れば賛成、通らなければ反対", "修正案は原案より先に採決される"],
    ["対案を出す", "同じテーマで別の法案を丸ごと出す", "原案とは別の独立した議案", "原案には反対することが多い", "賛成・反対とは別の軸。対案を出しつつ原案に賛成もありうる"],
    ["附帯決議", "可決するときに委員会が付ける「運用上の注文」", "原案は変えない", "賛成とセット", "法的な拘束力はない"],
    ["棄権・退席", "採決に加わらない", "―", "党の方針と違う議員が退席することもある", "「欠席＝反対」ではない"],
], None)
r += 1
ws.cell(row=r, column=1, value="実例：皇室典範改正（2026年7月、第221回国会）").font = Font(name=FONT, bold=True)
ex = [
    "原案：政府が皇族数確保のための改正案を提出",
    "修正案：立憲民主党が修正案を提出し、認められなければ原案に反対と表明（J-CAST 2026/7/9）",
    "附帯決議：参院特別委で、安定的な皇位継承策を引き続き検討するなどとした附帯決議も採択（公明新聞 2026/7/17）",
    "結果：7月17日に成立（公明新聞 2026/7/21）",
]
for i, t in enumerate(ex, 1):
    ws.cell(row=r + i, column=1, value=t).font = Font(name=FONT)
r += len(ex) + 2
r = section(ws, r, "④ 法案が成立するまで", NC)
r = write_table(ws, r, ["順番", "場所", "やること", "", ""], [
    [1, "提出", "内閣または議員が法案を出す", "", ""],
    [2, "付託", "議長が担当の委員会に審査を任せる", "", ""],
    [3, "委員会", "趣旨説明 → 質疑 → 討論 → 採決（修正案はここで出ることが多い）", "", ""],
    [4, "本会議", "委員会の結果を報告し、院として採決", "", ""],
    [5, "もう一方の院", "同じ流れをもう一度", "", ""],
    [6, "成立", "両院で可決されると成立。会期内に終わらないと継続審議か廃案", "", ""],
], None)
r += 1
r = section(ws, r, "⑤ 国会の種類（冒頭コールで使う）", NC)
write_table(ws, r, ["種類", "正式名", "いつ", "主な仕事", "今"], [
    ["通常国会", "常会", "毎年1月召集・150日間", "翌年度の予算と多くの法案", ""],
    ["臨時国会", "臨時会", "必要に応じて（秋が多い）", "補正予算・緊急の法案", "第222回：2026/10/5〜12/12（69日間）"],
    ["特別国会", "特別会", "衆院選の後", "首相の指名", ""],
], None)

# ---------------- 02_地図 ----------------
ws = wb.create_sheet("02_地図")
title(ws, "論点地図（大項目 → 中項目 → 小項目）", "性質：情勢対応＝その時の状況への対策（期限つきが多い）／制度改革＝ルールそのものを変える／恒常政策＝毎年続く政策")
big = {
    "A": "経済・暮らし", "B": "財政・税", "C": "社会保障・人口", "D": "外交・安全保障",
    "E": "国土・エネルギー・食料", "F": "統治・制度", "G": "社会・人権・教育",
}
mid = [
    ("A", "A1", "物価・家計支援"), ("A", "A2", "景気・成長戦略"), ("A", "A3", "雇用・賃金"), ("A", "A4", "産業・中小企業"),
    ("B", "B1", "税制"), ("B", "B2", "予算・補正予算"), ("B", "B3", "国債・財源"),
    ("C", "C1", "年金"), ("C", "C2", "医療・介護"), ("C", "C3", "子ども・子育て"), ("C", "C4", "障害福祉"), ("C", "C5", "人口戦略"),
    ("D", "D1", "外交"), ("D", "D2", "防衛"), ("D", "D3", "経済安全保障・重要土地"), ("D", "D4", "条約・通商"),
    ("E", "E1", "エネルギー"), ("E", "E2", "農業・食料"), ("E", "E3", "防災・地方"), ("E", "E4", "環境"),
    ("F", "F1", "選挙制度・議員定数"), ("F", "F2", "政治とカネ"), ("F", "F3", "皇室制度"), ("F", "F4", "憲法"), ("F", "F5", "行政改革・デジタル"),
    ("G", "G1", "外国人政策"), ("G", "G2", "家族制度・氏"), ("G", "G3", "多様性・人権"), ("G", "G4", "教育"), ("G", "G5", "治安・司法"),
]
small = {
    "A1": [("物価高対策（給付・補助）", "情勢対応", "", "物価上昇への家計支援全般"),
           ("お米券", "情勢対応", "", "参政党が代表質問で提案。総理は検討していないと答弁")],
    "A2": [("成長投資・危機管理投資", "恒常政策", "", "政府の投資方針")],
    "A3": [("最低賃金・賃上げ", "恒常政策", "", "")],
    "A4": [("中小企業・外食業への支援", "情勢対応", "食料品消費税減税法案", "減税で影響を受ける業界への支援策は未定")],
    "B1": [("食料品の消費税減税（1%・2年間）", "情勢対応", "食料品消費税減税関連法案", "2027年4月から2年間、飲食料品を8%→1%"),
           ("一律の消費税減税", "情勢対応", "", "一部野党が主張"),
           ("所得連動型の給付（就業者負担軽減支援金）", "制度改革", "食料品消費税減税関連法案", "減税とあわせて導入する給付制度。金額・対象は未定")],
    "B2": [("補正予算", "情勢対応", "", "2026年度補正予算は6月成立")],
    "B3": [("減税の財源（2年で約10兆円）", "情勢対応", "食料品消費税減税関連法案", "政府は赤字国債に頼らず確保するとしている"),
           ("公債特例法", "恒常政策", "令和8年度公債特例法案（衆法）", "")],
    "C1": [("年金制度改革", "制度改革", "", "")],
    "C2": [("医療・介護の負担", "恒常政策", "", ""), ("コロナワクチン", "恒常政策", "", "参政党が代表質問で取り上げ")],
    "C3": [("子育て支援・少子化対策", "恒常政策", "", "")],
    "C4": [("障害者と家族への支援", "制度改革", "障害者支援施策推進法案（衆法）", "国民民主党提出・継続審議")],
    "C5": [("人口戦略", "制度改革", "", "参政党が代表質問で取り上げ")],
    "D1": [("対米・対中関係", "恒常政策", "", "")],
    "D2": [("防衛費・防衛力", "恒常政策", "", "")],
    "D3": [("重要土地の取得規制（許可制）", "制度改革", "土地利用規制法改正案（閣法）", "防衛施設周辺・国境離島の土地取得を許可制に")],
    "D4": [("条約の承認", "恒常政策", "条約承認案（1本予定）", ""), ("米国産ジャガイモの輸入", "情勢対応", "", "参政党が代表質問で取り上げ")],
    "E1": [("原油調達の多角化", "情勢対応", "原油調達多角化関連法案（閣法）", "中東情勢の悪化を踏まえた対応"),
           ("再エネ賦課金・電気代", "恒常政策", "", "")],
    "E2": [("米・農業政策", "恒常政策", "", "")],
    "E3": [("防災・復興", "恒常政策", "", "")],
    "E4": [("脱炭素", "恒常政策", "", "")],
    "F1": [("衆院議員定数削減", "制度改革", "衆院議員定数削減法案（衆法）", "与党案は比例45削減。自民が比例31減案を提示、国民民主は19減を主張")],
    "F2": [("政治資金規正法改正", "制度改革", "政治資金規正法改正案（衆法）", "野党提出・継続審議")],
    "F3": [("皇族数の確保（皇室典範改正）", "制度改革", "皇室典範改正案（成立済）", "2026年7月17日成立。安定的な皇位継承は引き続き検討")],
    "F4": [("憲法改正", "制度改革", "", "")],
    "F5": [("副首都構想", "制度改革", "", "維新が推進")],
    "G1": [("外国人政策の見直し", "制度改革", "", "政府は「秩序ある共生」を掲げる")],
    "G2": [("旧姓の通称使用拡大", "制度改革", "政府法案（検討中）", ""),
           ("夫婦同氏の維持と旧姓証明", "制度改革", "参政党提出法案（参法）", "10/6に参議院に提出")],
    "G3": [("LGBT理解増進法と女性の安全", "制度改革", "", "参政党が代表質問で取り上げ")],
    "G4": [("教育無償化", "恒常政策", "", "")],
    "G5": [("治安・犯罪対策", "恒常政策", "", "")],
}
map_rows = []
for b, mid_id, mid_name in mid:
    items = small.get(mid_id, [])
    for i, (name, nature, bill, note) in enumerate(items, 1):
        sid = f"{mid_id}-{i:02d}"
        map_rows.append([b, big[b], mid_id, mid_name, sid, name, nature, bill, note])
headers = ["大ID", "大項目", "中ID", "中項目", "小ID", "小項目（論点）", "性質", "今国会の関連議案", "メモ", "記録件数"]
HR = 4
write_table(ws, HR, headers, map_rows, [6, 20, 6, 22, 9, 34, 11, 30, 44, 9])
for i in range(len(map_rows)):
    rr = HR + 1 + i
    ws.cell(row=rr, column=10, value=f"=COUNTIF('04_記録'!$H:$H,E{rr})").font = Font(name=FONT)
    ws.cell(row=rr, column=10).border = BORDER
    color = BIG_FILLS[map_rows[i][0]]
    for c in (1, 2):
        ws.cell(row=rr, column=c).fill = PatternFill("solid", fgColor=color)
    if map_rows[i][7]:
        ws.cell(row=rr, column=6).font = Font(name=FONT, bold=True)
MAP_LAST = HR + len(map_rows)
ws.freeze_panes = "A5"
ws.auto_filter.ref = f"A{HR}:J{MAP_LAST}"
ws.cell(row=MAP_LAST + 2, column=1, value="太字の小項目＝今国会に関連議案がある論点。小項目は増やしてよい（IDは中ID-連番）").font = Font(name=FONT, color="595959")

# ---------------- 03_今国会の議案 ----------------
ws = wb.create_sheet("03_今国会の議案")
title(ws, "第222回国会（臨時会）の主な議案", "会期：2026年10月5日〜12月12日（69日間）／政府提出は新規法案21本と条約承認案1本の予定（10/1時点）／状況は2026-11-10時点")
bills = [
    ["食料品の消費税減税関連法案", "閣法", "内閣", "B1-01", "参議院で審議へ（11/11審議入り予定）",
     "10/9提出 → 10/20衆院審議入り → 11/6衆院可決（自民・維新などの賛成多数）", "飲食料品を2027年4月から2年間1%に。所得連動型給付も導入",
     "https://news.web.nhk/newsweb/na/nd-20261107de71985"],
    ["衆院議員定数削減法案", "衆法", "自民・維新", "F1-01", "政党間協議中",
     "与党案は比例45削減。10/26 自民が比例31減案を提示、維新は執行部一任。国民民主は19減を主張", "",
     "https://kumanichi.com/articles/2050632"],
    ["土地利用規制法改正案（重要土地の許可制）", "閣法", "内閣", "D3-01", "提出方針（10/2時点）・要更新",
     "有識者会議の提言を踏まえ提出の方針", "防衛施設周辺・国境離島の土地取得に許可制",
     "https://kumanichi.com/articles/2042296"],
    ["原油調達多角化関連法案", "閣法", "内閣", "E1-01", "提出予定（10/1時点）・要更新",
     "", "中東情勢の悪化を踏まえた対応", "https://kumanichi.com/articles/2041683"],
    ["旧姓の通称使用拡大に関する法案", "閣法", "内閣", "G2-01", "提出を検討（10/1時点）・要更新",
     "", "", "https://kumanichi.com/articles/2041683"],
    ["夫婦同氏維持・旧姓証明書交付の法案", "参法", "参政党", "G2-02", "参議院に提出（10/6）",
     "", "", "https://ja.wikipedia.org/wiki/第222回国会"],
    ["政治資金規正法改正案", "衆法", "中道改革連合・無所属、国民民主党・無所属クラブ", "F2-01", "審議中（第221回国会から継続）",
     "", "", "https://ja.wikipedia.org/wiki/第222回国会"],
    ["令和8年度公債特例法案", "衆法", "中道改革連合・無所属、国民民主党・無所属クラブ", "B3-02", "審議中（第221回国会から継続）",
     "", "", "https://ja.wikipedia.org/wiki/第222回国会"],
    ["障害者と家族への支援施策推進法案", "衆法", "国民民主党・無所属クラブ", "C4-01", "審議中（第221回国会から継続）",
     "", "", "https://ja.wikipedia.org/wiki/第222回国会"],
]
for b in bills:
    b.insert(4, None)
headers = ["議案", "種類", "提出者・会派", "小ID", "論点（自動）", "現在の状況", "経緯", "中身", "出典"]
write_table(ws, 4, headers, bills, [34, 8, 26, 8, 28, 28, 46, 36, 40])
for i in range(len(bills)):
    rr = 5 + i
    ws.cell(row=rr, column=5, value=f"=IFERROR(INDEX('02_地図'!$F:$F,MATCH(D{rr},'02_地図'!$E:$E,0)),\"\")")
    ws.cell(row=rr, column=5).font = Font(name=FONT)
    ws.cell(row=rr, column=5).border = BORDER
    for c in (6, 7):
        ws.cell(row=rr, column=c).fill = INPUT_FILL
ws.freeze_panes = "B5"
sr = 5 + len(bills) + 1
ws.cell(row=sr, column=1, value="出典（会期・全体）").font = Font(name=FONT, bold=True)
srcs = [
    "日本経済新聞 2026/10/4「臨時国会、消費税減税や議員定数削減めぐり激しい論戦へ」 https://www.nikkei.com/article/DGXZQOUA294ML0Z20C26A9000000/",
    "共同通信（熊本日日新聞）2026/10/1「政府、新規法案21本提出へ」 https://kumanichi.com/articles/2041683",
    "共同通信（神奈川新聞）2026/10/20「消費減税、衆院で論戦スタート」 https://www.kanaloco.jp/news/social/article-1313854.html",
    "セレクトラ 消費税減税法案の審議状況 https://selectra.jp/money/news/shohizei-genzei-seiritsu",
    "KAB 2026/10/26 国民民主党 衆院定数19減を主張 https://www.kab.co.jp/news/article/16995176",
    "Wikipedia 第222回国会（提出会派の表記を含む。一次資料で要確認） https://ja.wikipedia.org/wiki/第222回国会",
]
for i, s in enumerate(srcs, 1):
    ws.cell(row=sr + i, column=1, value=s).font = Font(name=FONT, size=9, color="595959")

# ---------------- 99_リスト ----------------
wl = wb.create_sheet("99_リスト")
lists = {
    "舞台": ["衆・本会議", "衆・予算委員会", "衆・常任委員会", "衆・特別委員会", "参・本会議", "参・予算委員会",
             "参・常任委員会", "参・特別委員会", "党首討論", "内閣・閣議", "首相・閣僚会見", "政党会見",
             "都道府県議会", "市区町村議会", "首長会見", "その他"],
    "種別": ["議案（決める）", "質疑（ただす）", "会見・発表", "その他"],
    "役割": ["質問", "答弁", "趣旨説明", "討論", "会見", "その他"],
    "態度": ["賛成", "反対", "修正案提出", "対案提出", "附帯決議", "棄権・退席", "該当なし"],
    "確度": ["一次確認済", "報道のみ", "要確認"],
    "動画で使う": ["デイリー本編", "ショート", "総集編", "すべて", "不使用"],
    "シーン種別": ["冒頭コール", "テーマ一覧", "選手紹介", "問い（質問）", "答え（答弁）", "比較図解", "用語解説", "その後どうなった", "締め"],
    "カット状態": ["未着手", "頭出し済", "切出済", "要確認", "使用不可"],
    "層": ["市区町村", "都道府県", "国"],
    "起点": ["上げる（声から）", "下ろす（決定から）"],
    "経由": ["直通", "都道府県経由", "該当なし"],
    "ショート区分": ["前半", "後半", "使わない"],
    "ズレ状況": ["未着手", "声を集めた", "質問・要望した", "回答あり", "意見書・制度に反映", "完了"],
}
for ci, (name, vals) in enumerate(lists.items(), 1):
    wl.cell(row=1, column=ci, value=name)
    for ri, v in enumerate(vals, 2):
        wl.cell(row=ri, column=ci, value=v).font = Font(name=FONT)
    wl.column_dimensions[get_column_letter(ci)].width = 18
style_header(wl, 1, len(lists))
list_ref = {}
for ci, (name, vals) in enumerate(lists.items(), 1):
    col = get_column_letter(ci)
    list_ref[name] = f"='99_リスト'!${col}$2:${col}${len(vals) + 1}"


def add_dv(ws, ref_formula, rng):
    dv = DataValidation(type="list", formula1=ref_formula, allow_blank=True)
    ws.add_data_validation(dv)
    dv.add(rng)


N = 300  # rows prepared

# ---------------- 04_記録 ----------------
ws = wb.create_sheet("04_記録", 4)
title(ws, "記録（1行1件）", "黄色＝入力。小IDを選ぶと大項目・中項目・論点が自動で入る")
headers = ["記録ID", "日付", "国会", "舞台", "会議名", "種別", "議案名", "小ID", "大項目（自動）", "中項目（自動）", "論点（自動）",
           "発言者", "所属", "役割", "態度", "事実の要旨（評価語なし）", "出典URL", "映像URL", "頭出し時刻", "確度", "動画で使う"]
write_table(ws, 4, headers, [], [16, 11, 16, 14, 18, 14, 22, 9, 16, 18, 26, 14, 12, 9, 11, 50, 30, 30, 10, 11, 10])
ex_rows = [
    ["2026-10-09-001", "2026-10-09", "第222回 臨時会", "参・本会議", "本会議（代表質問）", "質疑（ただす）", "", "B1-02", None, None, None,
     "神谷宗幣", "参政党", "質問", "該当なし", "消費税の一律減税と、その分の賃上げを求めた", "", "", "", "要確認", "デイリー本編"],
    ["2026-10-09-002", "2026-10-09", "第222回 臨時会", "参・本会議", "本会議（代表質問）", "質疑（ただす）", "", "A1-02", None, None, None,
     "神谷宗幣", "参政党", "質問", "該当なし", "お米券で家計と農家を支えることを提案した", "", "", "", "要確認", "デイリー本編"],
    ["2026-11-06-001", "2026-11-06", "第222回 臨時会", "衆・本会議", "本会議", "議案（決める）", "食料品の消費税減税関連法案", "B1-01", None, None, None,
     "", "", "", "賛成", "衆院本会議で自民・維新などの賛成多数で可決し、参院に送付", "https://news.web.nhk/newsweb/na/nd-20261107de71985", "", "", "報道のみ", "すべて"],
]

SRC_CDP = "https://cdp-japan.jp/news/20261116_0759"
WEBTV = "https://www.webtv.sangiin.go.jp/webtv/index.php"
K = "消費税・支援金特別委員会"
B = "食料品の消費税減税関連法案"
real_rows = [
    ["2026-11-16-001", "2026-11-16", "第222回 臨時会", "参・特別委員会", K, "議案（決める）", B, "B1-01", None, None, None,
     "勝部賢志", "立憲民主", "質問", "該当なし", "家計負担の軽減額が小さいと指摘し、対象を絞った給付や社会保障を優先すべきと主張した（立憲民主党の発表による）", SRC_CDP, WEBTV, "14:15", "要確認", "デイリー本編"],
    ["2026-11-16-002", "2026-11-16", "第222回 臨時会", "参・特別委員会", K, "議案（決める）", B, "G4-01", None, None, None,
     "勝部賢志", "立憲民主", "質問", "該当なし", "減税を理由に学校給食費の支援額を引き下げないよう求めた。関文科相は予算編成の中で検討すると答えた（立憲民主党の発表による）", SRC_CDP, WEBTV, "14:15", "要確認", "総集編"],
    ["2026-11-16-003", "2026-11-16", "第222回 臨時会", "参・特別委員会", K, "議案（決める）", B, "B3-01", None, None, None,
     "柴愼一", "立憲民主", "質問", "該当なし", "法案は財源を「特例公債に頼らず確保する」としているが、具体的な財源と判断基準が示されていないと指摘した（立憲民主党の発表による）", SRC_CDP, WEBTV, "14:55", "要確認", "すべて"],
    ["2026-11-16-004", "2026-11-16", "第222回 臨時会", "参・特別委員会", K, "議案（決める）", B, "B1-03", None, None, None,
     "柴愼一", "立憲民主", "質問", "該当なし", "2029年度からの支援金は対象・水準・財源が不明確で白紙委任になるとして、本格導入部分を法案から切り離すよう求めた（立憲民主党の発表による）", SRC_CDP, WEBTV, "14:55", "要確認", "すべて"],
    ["2026-11-16-005", "2026-11-16", "第222回 臨時会", "参・特別委員会", K, "議案（決める）", B, "B1-01", None, None, None,
     "", "", "その他", "該当なし", "質疑者8人：本田顕子・小林孝一郎（自民）、徳永エリ・勝部賢志・柴愼一（立憲）、原田秀一・かごしま彰宏（国民）、上田勇（公明）。国民・公明の協力が焦点（NHK）", "https://news.web.nhk/newsweb/na/nd-20261116de76325", WEBTV, "13:00", "報道のみ", "すべて"],
]
ex_rows = ex_rows + real_rows
for i in range(N):
    rr = 5 + i
    vals = ex_rows[i] if i < len(ex_rows) else [None] * len(headers)
    for c in range(1, len(headers) + 1):
        cell = ws.cell(row=rr, column=c, value=vals[c - 1])
        cell.font = Font(name=FONT, color="7F7F7F" if i < 3 else "000000")
        cell.border = BORDER
        cell.alignment = Alignment(vertical="top", wrap_text=(c == 16))
        if c not in (9, 10, 11):
            cell.fill = INPUT_FILL
    ws.cell(row=rr, column=9, value=f"=IFERROR(INDEX('02_地図'!$B:$B,MATCH(H{rr},'02_地図'!$E:$E,0)),\"\")")
    ws.cell(row=rr, column=10, value=f"=IFERROR(INDEX('02_地図'!$D:$D,MATCH(H{rr},'02_地図'!$E:$E,0)),\"\")")
    ws.cell(row=rr, column=11, value=f"=IFERROR(INDEX('02_地図'!$F:$F,MATCH(H{rr},'02_地図'!$E:$E,0)),\"\")")
last = 4 + N
add_dv(ws, list_ref["舞台"], f"D5:D{last}")
add_dv(ws, list_ref["種別"], f"F5:F{last}")
add_dv(ws, f"='02_地図'!$E$5:$E${MAP_LAST}", f"H5:H{last}")
add_dv(ws, list_ref["役割"], f"N5:N{last}")
add_dv(ws, list_ref["態度"], f"O5:O{last}")
add_dv(ws, list_ref["確度"], f"T5:T{last}")
add_dv(ws, list_ref["動画で使う"], f"U5:U{last}")
ws.freeze_panes = "B5"
ws.cell(row=3, column=1, value="灰色の3行は記入例（神谷代表の質問は前回動画の内容から。会議録で要確認）。上書きして使ってよい").font = Font(name=FONT, size=9, color="595959")

# ---------------- 05_ストーリー構成 ----------------
ws = wb.create_sheet("05_ストーリー構成", 5)
title(ws, "ストーリー構成（論点 → シーン → 使う発言）", "1動画＝1論点が基本。シーンごとに「何を伝えるか」と「どの記録を使うか」を決めてから映像を切る")
headers = ["動画ID", "対象論点（小ID）", "論点（自動）", "シーン番号", "シーン種別", "このシーンで伝えること", "ナレーション案", "使う記録ID", "発言者（自動）", "映像が必要か", "補足図解テンプレ", "ショート区分"]
write_table(ws, 4, headers, [], [14, 10, 26, 8, 14, 34, 44, 16, 12, 10, 18, 10])
story_ex = [
    ["D-20261009-1", "B1-02", None, 1, "冒頭コール", "どの国会の話か", "参議院、臨時国会！", "", None, "不要", "冒頭コール"],
    ["D-20261009-1", "B1-02", None, 2, "テーマ一覧", "質問テーマは7つ、今回はその1つ目", "この日、神谷代表がぶつけたテーマは全部で7つ。今回はその1つ目です", "", None, "不要", "ツリー"],
    ["D-20261009-1", "B1-02", None, 3, "問い（質問）", "参政党は一律減税と賃上げを求めた", "", "2026-10-09-001", None, "必要", "比較"],
    ["D-20261009-1", "B1-02", None, 4, "答え（答弁）", "総理の答え", "", "", None, "必要", "答弁○✕"],
    ["D-20261009-1", "B1-02", None, 5, "その後どうなった", "政府案は11/6に衆院通過、参院へ", "", "2026-11-06-001", None, "不要", "その後"],
]
for row in story_ex:
    row.append("")
M = "D-20261116-1"
story_ex += [
    [M, "B3-01", None, 1, "冒頭コール", "どの国会の、どの場面か", "参議院、臨時国会！", "", None, "不要", "冒頭コール", "前半"],
    [M, "B3-01", None, 2, "テーマ一覧", "11/16 消費税特別委の質疑者8人。今回は立憲・柴議員の財源の質問", "この日の消費税特別委員会、質問に立ったのは8人。今回はその中から、減税の財源をめぐる攻防です！", "2026-11-16-005", None, "不要", "ツリー", "前半"],
    [M, "B3-01", None, 3, "選手紹介", "立憲民主 柴愼一 × 片山財務大臣", "", "2026-11-16-003", None, "必要", "選手紹介", "前半"],
    [M, "B3-01", None, 4, "問い（質問）", "「特例公債に頼らず確保」と書いてあるのに、財源の中身と判断基準が見えない", "", "2026-11-16-003", None, "必要", "比較", "前半"],
    [M, "B3-01", None, 5, "答え（答弁）", "片山財務相の答え（映像・会議録で確認してから書く）", "", "", None, "必要", "答弁○✕", "前半"],
    [M, "B1-03", None, 6, "問い（質問）", "2029年度からの支援金は白紙委任。法案から切り離すべき", "", "2026-11-16-004", None, "必要", "比較", "後半"],
    [M, "B1-03", None, 7, "答え（答弁）", "政府の答え（映像・会議録で確認してから書く）", "", "", None, "必要", "答弁○✕", "後半"],
    [M, "B1-01", None, 8, "用語解説", "減税は2027年4月から2年間、財源は2年で約10兆円、中身は年末の予算編成で決める", "", "", None, "不要", "用語解説", "後半"],
    [M, "B1-01", None, 9, "その後どうなった", "参院は与党が少数。国民民主・公明の協力が焦点", "", "2026-11-16-005", None, "不要", "その後", "後半"],
    [M, "B1-01", None, 10, "締め", "チャンネル登録・コメントのお願い", "", "", None, "不要", "締め", "使わない"],
]
for i in range(N):
    rr = 5 + i
    vals = story_ex[i] if i < len(story_ex) else [None] * len(headers)
    for c in range(1, len(headers) + 1):
        cell = ws.cell(row=rr, column=c, value=vals[c - 1])
        cell.font = Font(name=FONT, color="7F7F7F" if i < 5 else "000000")
        cell.border = BORDER
        cell.alignment = Alignment(vertical="top", wrap_text=(c in (6, 7)))
        if c not in (3, 9):
            cell.fill = INPUT_FILL
    ws.cell(row=rr, column=3, value=f"=IFERROR(INDEX('02_地図'!$F:$F,MATCH(B{rr},'02_地図'!$E:$E,0)),\"\")")
    ws.cell(row=rr, column=9, value=f"=IFERROR(INDEX('04_記録'!$L:$L,MATCH(H{rr},'04_記録'!$A:$A,0))&\"\",\"\")")
last = 4 + N
add_dv(ws, f"='02_地図'!$E$5:$E${MAP_LAST}", f"B5:B{last}")
add_dv(ws, list_ref["シーン種別"], f"E5:E{last}")
add_dv(ws, list_ref["ショート区分"], f"L5:L{last}")
ws.freeze_panes = "B5"

# ---------------- 06_発言カット ----------------
ws = wb.create_sheet("06_発言カット", 6)
title(ws, "発言カット（映像のどこを切るか）", "05で「映像が必要」としたシーンの発言を並べる。頭出し時刻〜終了秒は自動化で埋める予定（当面は手入力）")
headers = ["カットID", "動画ID", "シーン番号", "記録ID", "発言者（自動）", "日付（自動）", "使う発言の文言（会議録どおり）", "映像URL", "頭出し時刻", "開始（秒）", "終了（秒）", "長さ（秒）", "照合一致度", "状態"]
write_table(ws, 4, headers, [], [10, 14, 8, 16, 12, 11, 50, 30, 10, 9, 9, 9, 10, 10])
cut_ex = [["C-0001", "D-20261009-1", 3, "2026-10-09-001", None, None, "（会議録が出たら文言を貼る）", "", "", "", "", None, "", "未着手"],
          ["C-0002", "D-20261116-1", 4, "2026-11-16-003", None, None, "（財源の質問。会議録または文字起こしで確定）", WEBTV, "14:55", "", "", None, "", "未着手"],
          ["C-0003", "D-20261116-1", 5, "", None, None, "（片山財務相の答弁）", WEBTV, "14:55", "", "", None, "", "未着手"],
          ["C-0004", "D-20261116-1", 6, "2026-11-16-004", None, None, "（支援金の切り離しを求める質問）", WEBTV, "14:55", "", "", None, "", "未着手"],
          ["C-0005", "D-20261116-1", 7, "", None, None, "（政府の答弁）", WEBTV, "14:55", "", "", None, "", "未着手"]]
for i in range(N):
    rr = 5 + i
    vals = cut_ex[i] if i < len(cut_ex) else [None] * len(headers)
    for c in range(1, len(headers) + 1):
        cell = ws.cell(row=rr, column=c, value=vals[c - 1])
        cell.font = Font(name=FONT, color="7F7F7F" if i < 1 else "000000")
        cell.border = BORDER
        cell.alignment = Alignment(vertical="top", wrap_text=(c == 7))
        if c not in (5, 6, 12):
            cell.fill = INPUT_FILL
    ws.cell(row=rr, column=5, value=f"=IFERROR(INDEX('04_記録'!$L:$L,MATCH(D{rr},'04_記録'!$A:$A,0))&\"\",\"\")")
    ws.cell(row=rr, column=6, value=f"=IFERROR(INDEX('04_記録'!$B:$B,MATCH(D{rr},'04_記録'!$A:$A,0))&\"\",\"\")")
    ws.cell(row=rr, column=12, value=f"=IF(AND(ISNUMBER(J{rr}),ISNUMBER(K{rr})),K{rr}-J{rr},\"\")")
last = 4 + N
add_dv(ws, list_ref["カット状態"], f"N5:N{last}")
ws.freeze_panes = "B5"

LV = '{"市区町村","都道府県","国"}'

# ---- 09_地域マスタ ----
wm = wb.create_sheet("09_地域マスタ")
title(wm, "地域マスタ", "都道府県は47固定。市区町村は扱うたびに右の表へ追加（プルダウンに反映される）")
PREFS = ["北海道","青森県","岩手県","宮城県","秋田県","山形県","福島県","茨城県","栃木県","群馬県","埼玉県","千葉県","東京都","神奈川県",
         "新潟県","富山県","石川県","福井県","山梨県","長野県","岐阜県","静岡県","愛知県","三重県","滋賀県","京都府","大阪府","兵庫県",
         "奈良県","和歌山県","鳥取県","島根県","岡山県","広島県","山口県","徳島県","香川県","愛媛県","高知県","福岡県","佐賀県","長崎県",
         "熊本県","大分県","宮崎県","鹿児島県","沖縄県"]
write_table(wm, 4, ["都道府県名"], [[x] for x in PREFS], [12])
CITY_N = 200
write_table(wm, 4, [], [], None)
for i, h in enumerate(["市区町村名", "都道府県名", "議会名", "関わっている地方議員", "メモ"]):
    wm.cell(row=4, column=3 + i, value=h)
for c in range(3, 8):
    cl = wm.cell(row=4, column=c)
    cl.font = Font(name=FONT, bold=True, color="FFFFFF"); cl.fill = HEAD_FILL; cl.border = BORDER
cities = [["町田市", "東京都", "町田市議会", "矢口まゆ（町田市議）", "対談：2026/10/6、11/10"]]
for i in range(CITY_N):
    rr = 5 + i
    for j in range(5):
        v = cities[i][j] if i < len(cities) else None
        cl = wm.cell(row=rr, column=3 + j, value=v)
        cl.font = Font(name=FONT); cl.border = BORDER; cl.fill = INPUT_FILL
for col, w in zip("CDEFG", [14, 12, 16, 24, 30]):
    wm.column_dimensions[col].width = w
add_dv(wm, "='09_地域マスタ'!$A$5:$A$51", f"D5:D{4 + CITY_N}")
PREF_REF = "='09_地域マスタ'!$A$5:$A$51"
CITY_REF = f"='09_地域マスタ'!$C$5:$C${4 + CITY_N}"


def judge(dec, eff):
    return (f'=IF(OR({dec}="",{eff}=""),"",IF(MATCH({dec},{LV},0)=MATCH({eff},{LV},0),"完結",'
            f'IF(MATCH({dec},{LV},0)>MATCH({eff},{LV},0),"ズレ","要確認")))')


# ---- 04_記録 にズレのタグ列を追加 ----
ws = wb["04_記録"]
extra = ["決める場所", "影響が出る場所", "ズレ判定（自動）", "都道府県名", "市区町村名"]
for i, h in enumerate(extra):
    c = 22 + i
    ws.cell(row=4, column=c, value=h)
    ws.column_dimensions[get_column_letter(c)].width = 13
style_header(ws, 4, 26)
ex_tags = [("国", "国"), ("国", "国"), ("国", "市区町村")] + [("国", "国")] * 5
for i in range(N):
    rr = 5 + i
    for j, c in enumerate((22, 23)):
        v = ex_tags[i][j] if i < len(ex_tags) else None
        cell = ws.cell(row=rr, column=c, value=v)
        cell.fill = INPUT_FILL
        cell.border = BORDER
        cell.font = Font(name=FONT, color="7F7F7F" if i < len(ex_tags) else "000000")
    cell = ws.cell(row=rr, column=24, value=judge(f"V{rr}", f"W{rr}"))
    cell.border = BORDER
    cell.font = Font(name=FONT)
add_dv(ws, list_ref["層"], f"V5:W{4 + N}")
for i in range(N):
    for c in (25, 26):
        cl = ws.cell(row=5 + i, column=c)
        cl.fill = INPUT_FILL; cl.border = BORDER; cl.font = Font(name=FONT)
add_dv(ws, PREF_REF, f"Y5:Y{4 + N}")
add_dv(ws, CITY_REF, f"Z5:Z{4 + N}")

# ---- 08_ズレ記録 ----
ws = wb.create_sheet("08_ズレ記録", 7)
title(ws, "ズレ記録（テーマごとのタグ付け）",
      "決める場所＝それを変える決定権がどこにあるか／影響が出る場所＝暮らしの中でどこで感じるか。同じなら完結、違えばズレ（つなぐ人が必要）")
headers = ["ID", "テーマ", "都道府県名", "市区町村名", "決める場所", "影響が出る場所", "判定（自動）", "マス（自動）", "起点", "経由",
           "国の論点ID", "論点（自動）", "中身・生活者の声", "届け先・質問先", "状況", "関連する記録ID", "出典"]
write_table(ws, 4, headers, [], [8, 30, 10, 11, 11, 12, 10, 18, 16, 12, 9, 22, 46, 34, 14, 14, 30])
U, D, Dn = "上げる（声から）", "下ろす（決定から）", "該当なし"
gap = [
    ["学校プール開放の見直し", "町田市", "市区町村", "市区町村", U, Dn, "", "9月議会の対談で話題", "町田市議会・市役所"],
    ["公園の遊具の安全", "町田市", "市区町村", "市区町村", U, Dn, "", "", "町田市役所"],
    ["道路・公園の困りごとのLINE通報", "町田市", "市区町村", "市区町村", U, Dn, "", "", "町田市役所"],
    ["近所の交差点に信号機がほしい", "町田市", "都道府県", "市区町村", U, "直通", "", "市役所に言いがちだが、決めるのは都の警察（公安委員会）", "警察署・都議会議員"],
    ["水道料金（多摩地域）", "町田市", "都道府県", "市区町村", D, "直通", "", "町田の水道は都が運営。料金を決めるのは都", "都議会・都の水道局"],
    ["たばこのルール（屋内＝都の条例、路上＝市のルール）", "町田市", "都道府県", "市区町村", D, "直通", "", "決める場所が分かれていて、住民から違いが見えない", "町田市議会・都議会"],
    ["都立高校", "東京都", "都道府県", "都道府県", D, Dn, "", "", "都議会・都の教育委員会"],
    ["南町田のバス減便", "町田市", "国", "市区町村", U, "直通", "", "根っこは運転手不足と働き方の規制。路線バスの許認可は国", "国会議員・市議会の意見書"],
    ["部活動の地域移行", "町田市", "国", "市区町村", D, "都道府県経由", "", "国は方針、指導者・場所・費用の受け皿は市", "町田市議会・市の教育委員会"],
    ["食料品の消費税減税で市の収入が減る", "町田市", "国", "市区町村", D, "都道府県経由", "B1-01", "地方消費税は都道府県に入り、半分が市町村へ", "町田市議会（2027年度予算）"],
    ["物価高対策の交付金の使い道", "町田市", "国", "市区町村", D, "直通", "A1-01", "国が枠とお金、使い道は自治体が選ぶ", "町田市議会・市役所"],
    ["自転車の交通違反に反則金（青切符）", "東京都", "国", "都道府県", D, "直通", "", "ルールは国、取り締まりの運用は都の警察", "都議会・警視庁"],
    ["病院・病床の計画", "東京都", "国", "都道府県", D, "直通", "", "国の方針に沿って都が医療計画をつくる", "都議会・都庁"],
    ["消費税減税による地方の減収の穴埋め", "東京都", "国", "都道府県", U, "直通", "B3-01", "知事会などが代わりの財源を国に要望", "知事会・国会議員",
     "https://kumanichi.com/articles/2021838"],
    ["東京の税収を地方に回す仕組み", "東京都", "国", "都道府県", U, "直通", "", "都は見直しを国に要望。立場で見え方が逆になる", "都知事の提案要求・国会議員"],
    ["年金", "―", "国", "国", D, Dn, "C1-01", "国が決めて国（日本年金機構）が実行", "国会"],
    ["外交・防衛", "―", "国", "国", D, Dn, "D1-01", "", "国会"],
]
for i in range(N):
    rr = 5 + i
    g = gap[i] if i < len(gap) else None
    vals = [None] * len(headers)
    if g:
        vals[0] = f"Z-{i + 1:03d}"
        area = {"町田市": ("東京都", "町田市"), "東京都": ("東京都", ""), "―": ("", "")}[g[1]]
        vals[1] = g[0]
        vals[2], vals[3] = area
        vals[4], vals[5], vals[8], vals[9], vals[10], vals[12], vals[13] = g[2], g[3], g[4], g[5], g[6], g[7], g[8]
        vals[14] = "未着手"
        vals[16] = g[9] if len(g) > 9 else ""
    for c in range(1, len(headers) + 1):
        cell = ws.cell(row=rr, column=c, value=vals[c - 1])
        cell.font = Font(name=FONT)
        cell.border = BORDER
        cell.alignment = Alignment(vertical="top", wrap_text=(c in (2, 13, 14)))
        if c not in (7, 8, 12):
            cell.fill = INPUT_FILL
    ws.cell(row=rr, column=7, value=judge(f"E{rr}", f"F{rr}"))
    ws.cell(row=rr, column=8, value=f'=IF(G{rr}="","",IF(G{rr}="完結",E{rr}&"で完結",E{rr}&"→"&F{rr}))')
    ws.cell(row=rr, column=12, value=f"=IFERROR(INDEX('02_地図'!$F:$F,MATCH(K{rr},'02_地図'!$E:$E,0)),\"\")")
last = 4 + N
add_dv(ws, PREF_REF, f"C5:C{last}")
add_dv(ws, CITY_REF, f"D5:D{last}")
add_dv(ws, list_ref["層"], f"E5:F{last}")
add_dv(ws, list_ref["起点"], f"I5:I{last}")
add_dv(ws, list_ref["経由"], f"J5:J{last}")
add_dv(ws, f"='02_地図'!$E$5:$E${MAP_LAST}", f"K5:K{last}")
add_dv(ws, list_ref["ズレ状況"], f"O5:O{last}")
ws.freeze_panes = "C5"
ws.auto_filter.ref = f"A4:Q{last}"

# ---- 07_ズレ地図 ----
ws = wb.create_sheet("07_ズレ地図", 7)
title(ws, "ズレ地図：誰が決めるか × どこに影響が出るか",
      "同じなら【完結】、違えば【ズレ】＝つなぐ人が必要。数字は08_ズレ記録と04_記録のタグから自動集計（↑上げる・↓下ろす）")
Z = "'08_ズレ記録'"
R4 = "'04_記録'"
layers = ["市区町村", "都道府県", "国"]
label = {"市区町村": "市区町村（町田市）", "都道府県": "都道府県（東京都）", "国": "国"}
ws.cell(row=4, column=1, value="決める ＼ 影響が出る")
for j, e in enumerate(layers):
    ws.cell(row=4, column=2 + j, value=label[e])
style_header(ws, 4, 4)
examples = {
    ("市区町村", "市区町村"): "例：学校プール開放、公園の遊具",
    ("都道府県", "市区町村"): "例：↑信号機 ↓水道料金 ↓たばこ",
    ("都道府県", "都道府県"): "例：都立高校",
    ("国", "市区町村"): "例：↑バス減便 ↓部活動の地域移行 ↓減税で市の収入減",
    ("国", "都道府県"): "例：↓青切符 ↓病床の計画 ↑減税の穴埋め",
    ("国", "国"): "例：年金、外交・防衛",
}
GAP_FILL = PatternFill("solid", fgColor="FCE4D6")
OK_FILL = PatternFill("solid", fgColor="E2EFDA")
NA_FILL = PatternFill("solid", fgColor="F2F2F2")
for i, d in enumerate(layers):
    rr = 5 + i
    h = ws.cell(row=rr, column=1, value=label[d])
    h.font = Font(name=FONT, bold=True, color="FFFFFF")
    h.fill = HEAD_FILL
    h.alignment = Alignment(vertical="center", wrap_text=True)
    h.border = BORDER
    for j, e in enumerate(layers):
        c = 2 + j
        cell = ws.cell(row=rr, column=c)
        cell.border = BORDER
        cell.alignment = Alignment(vertical="top", wrap_text=True)
        cell.font = Font(name=FONT)
        if layers.index(d) < layers.index(e):
            cell.value = "―（起きない）"
            cell.fill = NA_FILL
            continue
        kind = "完結" if d == e else "ズレ"
        L = 4 + N
        flt = f'*(($G$4="")+({Z}!$C$5:$C${L}=$G$4)>0)*(($G$5="")+({Z}!$D$5:$D${L}=$G$5)>0)'
        flt4 = f'*(($G$4="")+({R4}!$Y$5:$Y${L}=$G$4)>0)*(($G$5="")+({R4}!$Z$5:$Z${L}=$G$5)>0)'
        base = f'({Z}!$E$5:$E${L}="{d}")*({Z}!$F$5:$F${L}="{e}")'
        tot = f'SUMPRODUCT({base}{flt})'
        up = f'SUMPRODUCT({base}*({Z}!$I$5:$I${L}="上げる（声から）"){flt})'
        dn = f'SUMPRODUCT({base}*({Z}!$I$5:$I${L}="下ろす（決定から）"){flt})'
        rec = f'SUMPRODUCT(({R4}!$V$5:$V${L}="{d}")*({R4}!$W$5:$W${L}="{e}"){flt4})'
        cell.value = (f'="【{kind}】"&CHAR(10)&"テーマ "&{tot}'
                      f'&"件（↑"&{up}&" ↓"&{dn}&"）"&CHAR(10)&"国会・議会の記録 "&{rec}&"件"'
                      f'&CHAR(10)&"{examples[(d, e)]}"')
        cell.fill = OK_FILL if kind == "完結" else GAP_FILL
    ws.row_dimensions[rr].height = 92
for rr_, lab in ((4, "都道府県で絞る"), (5, "市区町村で絞る")):
    ws.cell(row=rr_, column=6, value=lab).font = Font(name=FONT, bold=True)
    cc = ws.cell(row=rr_, column=7)
    cc.fill = INPUT_FILL
    cc.border = BORDER
ws.cell(row=6, column=6, value="空欄＝すべて").font = Font(name=FONT, size=9, color="595959")
add_dv(ws, PREF_REF, "G4")
add_dv(ws, CITY_REF, "G5")
ws.column_dimensions["F"].width = 16
ws.column_dimensions["G"].width = 14
ws.column_dimensions["A"].width = 22
for col in "BCD":
    ws.column_dimensions[col].width = 38
r = 9
r = section(ws, r, "読み方", 4)
notes = [
    ["【完結】", "決める場所と影響が出る場所が同じ。そこの議会・役所に言えば話が完結する"],
    ["【ズレ】", "決める場所と影響が出る場所が違う。つなぐ人がいないと声が止まる＝この活動の担当範囲"],
    ["↑ 上げる", "生活者の困りごとから始まる。「その困りごと、誰に言えば変わる？」"],
    ["↓ 下ろす", "国や都の決定から始まる。「決まったことが、町田でどうなる？」"],
    ["―（起きない）", "決める場所は影響が出る場所と同じか上にしかないため、使わない"],
]
r = write_table(ws, r, ["印", "意味"], notes, None)
r += 1
r = section(ws, r, "ズレを埋めるルート", 4)
write_table(ws, r, ["つなぐ場所", "上げるルート", "下ろすときに聞く相手", ""], [
    ["市区町村 ↔ 都道府県", "都議会議員、市議会の意見書、都への要望", "市議会・市役所「都の決定は町田でどうなる？」", ""],
    ["市区町村 ↔ 国", "国会議員、市議会の意見書（直接または都経由）", "市議会・市役所「国の決定は町田でどうなる？」", ""],
    ["都道府県 ↔ 国", "知事の提案要求、知事会、都議会の意見書", "都議会・都庁「国の決定は都でどうなる？」", ""],
], None)
ws.column_dimensions["A"].width = 22

for s in wb.worksheets:
    s.sheet_view.showGridLines = s.title not in ("00_使い方", "01_国会の基本構造")

wb.move_sheet("09_地域マスタ", offset=-1)
wb.save("国会論点地図.xlsx")
print("saved", MAP_LAST)
