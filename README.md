# agaru-up-camera

Raspberry Pi上で動作するカメラ記録・動画取得APIシステムです。

## 📋 概要

このプロジェクトは、Raspberry Piのカメラを使用して動画を継続的に記録し、FastAPI経由で取得できるシステムです。指定した秒数分の動画を自動的に結合して提供します。

## 📁 ファイル構成

```
agaru-up-camera/
├── main.py                  # FastAPI アプリケーション（動画取得API）
├── rec.sh                   # カメラ記録スクリプト
├── combine_segments.sh      # 動画結合スクリプト
├── pyproject.toml           # プロジェクト設定
├── .env.sample              # 環境変数テンプレート
├── LICENSE                  # ライセンス
├── README.md                # このファイル
├── recordings/              # 記録された動画ファイルの保存先
└── .venv/                   # Python仮想環境
```

## 🚀 セットアップ

### 必要条件

- Raspberry Pi
- Python 3.14以上
- uv（パッケージ管理）
- FFmpeg（動画結合用）

### インストール手順

1. リポジトリをクローンします：
```bash
git clone https://github.com/ohs25-2-misoten/agaru-up-camera.git
cd agaru-up-camera
```

2. `.env` ファイルを設定します：
```bash
cp .env.sample .env
# .envファイルを適切に編集してください
```

3. 依存パッケージをインストールします：
```bash
uv sync
```

## 🔧 主な機能

### 動画記録 (`rec.sh`)

Raspberry Piのカメラから継続的に動画を記録します。
```bash
./rec.sh
```

### 動画取得API (`main.py`)

FastAPIサーバーとして起動し、指定した秒数分の動画を取得できます。

```bash
uvicorn main:app --reload
```

**エンドポイント:**
- `GET /`: ヘルスチェック
- `GET /videos?time=<seconds>`: 指定秒数（1～120秒）分の動画をMP4形式で返す

### 動画結合 (`combine_segments.sh`)

複数の動画セグメントを1つのMP4ファイルに結合します。

## 📝 環境変数

`.env` ファイルで以下の環境変数を設定できます：
- `OUTPUT_DIR`: 出力動画ファイルの保存先ディレクトリ
- `feat/*`: 新機能開発用ブランチ
- `fix/*`: バグ修正用ブランチ
- `hotfix/*`: 緊急修正用ブランチ

### 開発フロー

1. mainブランチから短命ブランチを作成：
```bash
git checkout main
git pull origin main
git checkout -b feat/your-feature-name
```

2. 開発・コミット：
```bash
git add .
git commit -m "feat: 新機能の説明"
```

3. プルリクエストを作成してmainにマージ
4. マージ後、短命ブランチを削除

## 📝 コーディング規約

### コミットメッセージ

Conventional Commits形式を採用：

```
<type>(<scope>): <subject>

<body>

<footer>
```

**タイプ**:
- `feat`: 新機能
- `fix`: バグ修正
- `docs`: ドキュメント
- `style`: スタイル変更
- `refactor`: リファクタリング
- `test`: テスト
- `chore`: その他

## 🚢 リリース

### バージョニング

Semantic Versioning (SemVer) を採用：
- `MAJOR.MINOR.PATCH` (例: 1.0.0)

### リリースプロセス

1. mainブランチから最新の変更を取得：
```bash
git checkout main
git pull origin main
```

2. バージョンを更新（例：1.0.0 → 1.1.0）

3. 変更をコミット：
```bash
git commit -m "chore: リリース v1.1.0"
```

4. タグを作成してプッシュ：
```bash
git tag -a v1.1.0 -m "Release v1.1.0"
git push origin main --tags
```

5. GitHubの Releases ページでリリースノートを作成

## 🤝 コントリビューション

1. このリポジトリをフォーク
2. 機能ブランチを作成 (`git checkout -b feat/amazing-feature`)
3. 変更をコミット (`git commit -m 'feat: 素晴らしい機能を追加'`)
4. ブランチにプッシュ (`git push origin feat/amazing-feature`)
5. プルリクエストを作成

### プルリクエストガイドライン

- [ ] 適切なブランチから作成
- [ ] テストの追加・更新
- [ ] コードレビューの実施
- [ ] コンフリクトの解決
- [ ] ドキュメントの更新（必要な場合）

## 📄 ライセンス

GNU Affero General Public License v3.0 (AGPL-3.0) ライセンスの下で提供されています。詳細は [LICENSE](./LICENSE) ファイルを参照してください。

## 👥 メンテナー

- [tomo3101](mailto:tacstomo.sub@gmail.com)

## 📞 サポート

質問や問題がある場合は、以下の方法でお問い合わせください：

- [Issues](../../issues) - バグ報告や機能要望
- [Discussions](../../discussions) - 質問や議論

## 📚 追加リソース

- [Cloudflare Tunnel Documentation](https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/)
- [uv - Python package installer](https://docs.astral.sh/uv/)

---

**最終更新**: 2026年1月8日
