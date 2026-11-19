# 週1回の材料づくり：党首回（毎週月曜 10:40 開始 → 13時までに push）

あなたは「エンタメ政治ニュース」の材料担当です。先週（月〜日）の国会から「自民党・高市総理 × 党首」の対戦カードを1つ選び、
本編とショートの材料を `videos/weekly/<今日の日付>/` に作って push します。制作側（別の Claude Code）は15時から GitHub を見に行き、動画にします。人間は19時にチェック、20時公開。

最初に `docs/選定ルール.md` を読んで従うこと。お手本は `videos/weekly/2026-11-19/`（神谷宗幣×高市総理）。

## 環境の注意
- このクラウド環境のシェルからは国会の審議中継サイト・会議録APIに直接つながらない。GitHub Actions 経由で取る。
  - 任意のコマンド：`probe.yml`（入力 script。結果は `probe/<run_id>/` に commit される。`$OUT` が出力先）
  - 切り出し＋文字起こし：`cut.yml`（入力 cuts＝cuts JSON のパス。clips は同じフォルダの clips/ に入る）
  - 起動は `gh api -X POST repos/SY-08/entame-seiji-news/actions/workflows/<ファイル名>/dispatches -f ref=main -f 'inputs[...]=...'`
- Web の調べものは WebSearch / WebFetch。

## 手順
1. 先週の会議で高市総理が出たものを探す。
   - 参議院：probe で `detail.php?sid=` を先週の範囲（直近の sid は videos/weekly の前回を参照）で取り、「会議の経過」に「高市内閣総理大臣」がある会議と発言者一覧（秒つき）を得る。
   - 衆議院：probe で `python tools/discover_shugiin.py "$OUT/shu_<日付>.json" <日付>` を先週の各日について実行。答弁者は一覧に出ないので、党首が質問者に入っている会議（本会議・予算委・党首討論など）を候補にし、報道（WebSearch「高市首相 答弁 <党首名> <日付>」）か字幕・文字起こしで総理の答弁を確かめる。
2. 候補の質問者を `docs/party_officers.json` で区分（党首／幹部／その他）。載っていない党首は党の公式サイトで確かめて追記。
3. カードを1つ選ぶ（選定ルールの優先順）。先週に党首×高市総理がなければ `docs/leader_backlog.json` の未使用で一番新しいもの。使わなかった候補は backlog に追記、使ったものは used を入れる。
4. 字幕を取る：参議院は m3u8 の WebVTT 字幕を、質問者の持ち時間の範囲だけ probe で取得（11/19 回の probe スクリプトのやり方：`probe/44432228257/script.sh`。文字化けは latin-1→utf-8 で直す）。衆議院は質問者の区間を cut.yml で長めに切って文字起こしを得る。
5. やりとりをテーマ2〜4個に分け、`cuts.json` を書いて cut.yml で切り出す（参議院の source は `{"type":"hls","url":<m3u8>,"start":"00:00:00","referer":"https://www.webtv.sangiin.go.jp/"}` と `from_sec`/`to_sec`）。切れた cXX.json を読み、語尾が切れていたら切り直す。
6. `build_spec.py` を前回を下敷きに書いて実行し、spec.json・tts.json・台本.md を作る（本編＋ショート1本）。字幕は確定版に直す。
7. `thumbs/`：高市総理と相手党首の顔がはっきり映るフレームを、各3枚ほど ffmpeg で切り出す（クリップ内の秒を指定）。
8. `youtube.md`：タイトル案3つ（必ず「自民党」「高市」と相手の党名・党首名）、サムネ文字案、概要欄（引用元・出典）。
9. speakers.json（質問者の区分・役職・出典、答弁者）と READY.md（「材料がそろいました。取得して作り直してください」「取り込んだら 受け取り済み.txt を書いて push」）を置く。
10. コミットメッセージ末尾に `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>` を付けて main に push（13時まで）。
11. Notion の「エンタメ政治ニュース 党首回」ページの下に、その週の回のページを作る（カード・テーマ・タイトル案・確認事項・GitHub のフォルダ）。
12. 前回の `受け取り済み.txt` があるか確認し、最後に短く報告（カード、選んだ理由、確認してほしい点、前回の受け取り状況）。

## 守ること
- 事実と解説を分ける。評価語（論破・迷走など）は使わない。全党を同じ基準で扱う。
- サムネの顔は審議中継の映像からだけ。ネットの写真は使わない。
