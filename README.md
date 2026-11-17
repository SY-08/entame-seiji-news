# エンタメ政治ニュース

政治をサッカー中継のように楽しく伝えるYouTubeチャンネル「エンタメ政治ニュース（デイリー国会）」の制作用リポジトリです。

## 夕方の自動リサーチ

平日の日本時間17:07に GitHub Actions が動き、Claude がその日の国会の動きを調べて、次のファイルを作ります。20時の公開に間に合わせるための時刻です。

| ファイル | 中身 |
| --- | --- |
| `research/YYYY-MM-DD/台本.md` | デイリー版本編の台本（シーン構成・ショートの前半後半の割り振り・出典） |
| `research/YYYY-MM-DD/シート追記.csv` | スプレッドシートに入れる記録・シーン・発言カットの行 |
| `research/YYYY-MM-DD/summary.md` | 選んだ対戦カードと、確認が必要な点 |

終わると Issue が1件でき、GitHub から通知が届きます。

- 設定：`.github/workflows/daily-research.yml`
- Claude への指示：`prompts/daily-research.md`
- 手動で動かす：Actions タブ →「夕方の自動リサーチ」→「Run workflow」（日付を指定すると過去の日も作れる）

## 最初の設定（1回だけ）

1. Claude Code でこのリポジトリを開き、`/install-github-app` を実行する。Claude の GitHub アプリが入り、`CLAUDE_CODE_OAUTH_TOKEN` が登録される。
2. Actions タブで「夕方の自動リサーチ」を手動実行し、Issue が届くことを確かめる。

## その他

| 場所 | 中身 |
| --- | --- |
| `docs/国会論点地図.xlsx` | 論点地図・記録・ストーリー・発言カット・ズレ地図のスプレッドシート |
| `docs/build_sheet.py` | 上のスプレッドシートを作るスクリプト |
