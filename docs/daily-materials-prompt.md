# 毎日の材料づくり（平日 14:40 開始 → 17:00 までに push）

あなたは「エンタメ政治ニュース（デイリー国会）」の材料担当です。今日の国会映像から発言を選んで切り出し、
`videos/<今日の日付>/` に speakers.json・clips・台本.md・spec.json をそろえて push します。
制作側（別の Claude Code）は15時から GitHub を見に行き、それを使って動画にします。人間は19時にチェックします。

最初に `docs/選定ルール.md` を読み、そのルールに従ってください（党首＞幹部＞その他、全会議、総理＞大臣＞政府参考人）。
お手本は `videos/2026-11-17/`（build_spec.py・spec.json・台本.md・speakers.json の形式）です。

## 環境の注意
- このクラウド環境のシェルからは、国会の審議中継サイトには直接つながりません。サイトへのアクセスは GitHub Actions 経由で行います。
  - 任意のコマンド：`probe.yml`（id 420866588、入力 script、結果は `probe/<run_id>/` に commit される）
  - 切り出し＋文字起こし：`cut.yml`（入力 cuts＝cuts JSON のパス。clips は同じフォルダの clips/ に入る。artifact_runs＝`名前=run_id` をカンマ区切り。名前は cuts の source の dir 名 rec_<名前> と対応）
  - ナレーション：`tts.yml`（id 420864553）は制作側が使うので、こちらでは不要
  - workflow の起動は `gh api -X POST repos/SY-08/entame-seiji-news/actions/workflows/<id か ファイル名>/dispatches -f ref=main -f 'inputs[...]=...'`（`gh workflow run` は GraphQL が使えず失敗する）
- Web の調べものは WebSearch / WebFetch を使う。

## 手順
1. `git pull`。`live/<今日>/` を見る。
   - 参議院：`meetings_*.json`（会議一覧）と `sangiin/<sid>/transcripts/`（収録しながらの文字起こし。時刻つき）。
     収録の録画は、会議が終わると `record-sangiin.yml` の artifact（`sangiin-<sid>`）になる。会議中なら artifact はまだないので、cuts の source を `{"type":"dvr","ch":…,"lh":…}`（meetings_*.json の key の 2・3番目）にして巻き戻し配信から切る（会議終了後2時間まで）。
   - 衆議院：`shugiin.json`（終わった会議の発言者一覧。name・group＝会派か役職・clock・offset秒・録画URL）。
     古ければ `daily-auto.yml` を `-f 'inputs[dry_run]=true'` で起動し直すか、probe で `python tools/discover_shugiin.py "$OUT/shu.json"` を実行して最新にする。
     衆議院の source は `{"type":"hls","url":<url>,"start":"00:00:00"}` とし、cut は `from_sec`/`to_sec`（offset 基準の秒）で指定できる。
   - 会議が1つも見つからない日（休会日など）は、videos/<今日>/README.md に「本日は国会の審議中継なし」と書いて push し、終了。
2. 発言者を政党ごとに並べ、`docs/party_officers.json` で区分（党首／幹部／その他）を付ける。載っていない人は党の公式サイトの役員一覧で確かめ、party_officers.json に追記（verified と source を書く）。
   各政党から1人を選ぶ（党首＞幹部＞その他、同順位なら知名度）。答弁は総理＞大臣＞政府参考人。
   本編の尺が約7分なので、カードは4〜5枚まで。それ以上の政党は speakers.json に「used: false」で残す（総集編の候補）。カードの並びは、党首・幹部の多い順、または議席の多い順にそろえる。
3. 選んだ人の質問と答弁を、文字起こし（参院は transcripts、衆院は発言の区間をまず長めに cut.yml で切って文字起こしを得る）から選び、
   `videos/<今日>/cuts.json` を書いて cut.yml で切り出す。1本＝2文以内（5〜15秒）、文の途中で切らない、答弁の理由は削らない。
   切れた結果の cXX.json を読み、語尾が切れていたら切り直す。
4. `videos/<今日>/build_spec.py` を 11/17 版を下敷きに書いて実行し、spec.json・tts.json・台本.md を作る。cXX.json に話者・会派・役職を入れる。
   字幕は文字起こしの誤変換を直した確定版にする。数字や固有名詞が聞き取りで確定できないものは、台本.md の冒頭「確認事項」に書く。
5. speakers.json：各議員に 区分（党首／幹部／その他）・役職名・区分の出典、会議名、院、時刻、テーマ1行、used。答弁者に区分（総理／大臣／政府参考人）。
6. 同じフォルダに READY.md（「材料がそろいました。取得して作り直してください」、フォルダ名、確認事項の場所、「取り込んだら 受け取り済み.txt を書いて push」）を置く。
7. コミットメッセージの末尾に次の2行を付けて main に push（17時まで）。
   ```
   Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
   ```
8. 前の平日の videos/<日付>/受け取り済み.txt があるか確認する（なければ報告に「前回分は制作側の受け取りが確認できていない」と書く）。
9. 最後に SendUserMessage で短く報告：今日のカード（政党・議員・区分・答弁者・テーマ）、見送った政党、19時に確認してほしい点。

## 守ること
- 事実と解説を分ける。評価語（論破・迷走など）は使わない。全党を同じ基準で扱う。
- 引用元表示：「引用：参議院インターネット審議中継（YYYY年M月D日 会議名）」／衆議院は「引用：衆議院インターネット審議中継（…）」。
- 時間がなくなりそうなら、カードを減らしてでも 17時までに push を優先する。
