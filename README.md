# butsugiri.github.io

Shun Kiyono のプロフィール・論文一覧を公開する Jekyll サイトです。
公開 URL: https://butsugiri.github.io

## 開発

Docker を起動してから、リポジトリのルートで実行します。
ホストに Ruby をインストールする必要はありません。

```sh
docker compose build
docker compose up
```

http://localhost:4000 を開きます。LiveReload はポート 35729 を使います。
設定ファイルを変更した場合はサーバーを再起動してください。

## ビルド確認

```sh
docker compose run --rm -e JEKYLL_ENV=production service_jekyll bundle exec jekyll build --trace
python3 scripts/check_site.py
```

生成物は `my-blog/_site/` に出力され、Git の管理対象には含めません。
CI でもすべてのブランチ向けの PR と main への push 時に Docker ビルドと生成 HTML を検証します。
HTML 検査は要旨本文・メタ情報・ローカル資料・ページ内リンクを確認します（Python 3 標準ライブラリのみ）。
main では検証成功後に既存の方式で gh-pages ブランチへ公開します。
GitHub Pages の公開元は gh-pages ブランチのルートを使用します。

## 更新するファイル

- `my-blog/index.md`: 経歴・学歴・活動
- `my-blog/_bibliography/*.bib`: 論文情報
- `my-blog/repository/`: 論文・スライド・ポスター PDF
- `my-blog/_data/menu.yml`: ページ内ナビゲーション
- `my-blog/_config.yml`: 公開 URL・著者・SEO・テーマ設定

論文の `url` は末尾が `.pdf` の場合に「PDF」、それ以外は「Paper」と表示します。
`slide`・`poster`・`spotlight` は別リンクとして表示します。
ローカルの資料には `/repository/ファイル名.pdf` を指定します。
要旨は `abstract` に設定すると開閉できます。

## gem・Ruby の更新

`Gemfile.lock` は必ず Linux コンテナ内で更新します。

```sh
docker compose run --rm service_jekyll bundle update
docker compose build
docker compose run --rm -e JEKYLL_ENV=production service_jekyll bundle exec jekyll build --trace
```

Ruby を更新する際は Dockerfile と CI の `ruby_ver` を合わせ、同じ更新手順を実行します。
詳しいルールは [AGENTS.md](AGENTS.md) を参照してください。

## 旧サイト

`obsolete/` は以前の Python 製サイトの保存用です。現在のビルド・公開には使用しません。
旧資料は履歴保持のため残し、現在の論文一覧で参照する PDF は `my-blog/repository/` にも保存します。
Docker のビルドコンテキストには Gemfile とロックファイルだけを含めます。
