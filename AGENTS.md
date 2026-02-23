# AGENTS.md — プロジェクトルール

## 概要

Jekyll 製の静的サイト（[butsugiri.github.io](https://butsugiri.github.io)）。
Docker コンテナ内で開発・ビルドを行う。ホスト環境に Ruby を直接インストールしない。

## ディレクトリ構成

```
.
├── Dockerfile            # コンテナイメージ定義
├── docker-compose.yml    # サービス定義
└── my-blog/              # Jekyll サイト本体（コンテナ内では /code にマウント）
    ├── Gemfile
    ├── Gemfile.lock
    ├── _config.yml
    ├── _bibliography/
    ├── _layouts/
    ├── _includes/
    ├── assets/
    └── repository/       # 論文 PDF 等
```

## Docker 構成

- ベースイメージ: `ruby:4.0.1-bookworm`（`linux/amd64` で固定）
- `./my-blog` が `/code` としてマウントされる
- Dockerfile では `Gemfile` と `Gemfile.lock` の両方をコピーしてから `bundle install` する

```dockerfile
FROM ruby:4.0.1-bookworm

WORKDIR /code
COPY my-blog/Gemfile .
COPY my-blog/Gemfile.lock .
RUN bundle install
```

## 主要コマンド

### 開発サーバーの起動

```bash
docker-compose up
```

ブラウザで http://localhost:4000 にアクセスする。

### ビルド確認

```bash
docker-compose run --rm service_jekyll bundle exec jekyll build
```

### gem の更新

```bash
# 1. コンテナ内で bundle update（Gemfile.lock がホスト側に反映される）
docker-compose run --rm service_jekyll bundle update

# 2. イメージを再ビルド（Gemfile.lock の変更をイメージに反映する）
docker-compose build

# 3. ビルド確認
docker-compose run --rm service_jekyll bundle exec jekyll build
```

### Ruby バージョンの更新

`Dockerfile` の `FROM` 行を変更し、上記の gem 更新手順を実施する。
Ruby バージョンが変わると `google-protobuf` 等のプラットフォーム固有 gem のロックが変わるため、
イメージ再ビルド前に必ず `bundle update` を実行し直すこと。

## 注意事項

- `Gemfile.lock` は常に **コンテナ内**（`docker-compose run --rm service_jekyll bundle update`）で更新する。ホスト（macOS）上の Ruby で更新すると Linux 環境と不整合になる。
- `Gemfile.lock` を更新したら必ずイメージを `docker-compose build` で再ビルドする。
- `google-protobuf` など一部の gem はプラットフォーム固有のバイナリ版とネイティルコンパイル版がある。Ruby バージョンを変更した際は `bundle update` を再実行して lock ファイルのプラットフォーム情報を更新すること。
