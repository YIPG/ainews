# AI Newsletter Japan

日本語版AIニュースレター翻訳アーカイブシステム - AI技術ニュースレターの内容を自動的に日本語に翻訳してGitHub Actionsにアーカイブし、Discordに通知します。

## 概要

このプロジェクトは、指定されたRSSフィードから最新のAIニュースレターを取得し、Azure OpenAI GPT-4oを使用して日本語に翻訳し、GitHub Actionsアーティファクトとして保存する自動化パイプラインです。翻訳完了時にはDiscordに要約付きで通知されます。

## 機能

- 🔄 RSS フィードからの自動取得と重複チェック
- 🌐 Azure OpenAI GPT-4oによる高品質な日本語翻訳
- ✅ 翻訳品質の自動チェック（スコア0.95以上）
- 📦 GitHub Actionsアーティファクトへの自動保存（30日間保持）
- 💬 Discord Webhookによる翻訳完了通知（要約付き）
- 🕐 平日15:00 UTC（太平洋時間8:00）に自動実行
- 🔔 SlackおよびDiscordへのエラー通知（オプション）

## セットアップ

### 前提条件

- Python 3.8以上
- Azure OpenAIアカウントとGPT-4oデプロイメント
- GitHubアカウント（GitHub Actions用）
- Discord Webhook URL（オプション、通知用）

### 1. リポジトリのクローン

```bash
git clone https://github.com/yourusername/ainews.git
cd ainews
```

### 2. 仮想環境のセットアップ

```bash
make venv
```

### 3. 環境変数の設定

ローカルテスト用に以下の環境変数を設定してください：

```bash
export FEED_URL="your-rss-feed-url"
export AOAI_ENDPOINT="https://your-resource.openai.azure.com/"
export AOAI_KEY="your-azure-openai-key"
export AOAI_DEPLOYMENT="your-gpt4o-deployment-name"
export DISCORD_WEBHOOK="your-discord-webhook-url"  # オプション
export SLACK_WEBHOOK="your-slack-webhook-url"      # オプション
```

### 4. GitHub Secretsの設定

GitHub リポジトリの Settings → Secrets and variables → Actions で以下のシークレットを追加：

- `FEED_URL` - RSS フィードURL
- `AOAI_ENDPOINT` - Azure OpenAIエンドポイント
- `AOAI_KEY` - Azure OpenAI APIキー
- `AOAI_DEPLOYMENT` - GPT-4oデプロイメント名
- `DISCORD_WEBHOOK` - Discord Webhook URL（オプション）
- `SLACK_WEBHOOK` - Slack Webhook URL（オプション）

### 5. GitHub Pagesの有効化

1. Settings → Pages
2. Source: Deploy from a branch
3. Branch: main / folder: /public
4. Save

### 6. 自動実行の設定

GitHub Actionsは平日15:00 UTC（太平洋時間8:00）に自動的に実行されます。手動実行も可能です。

## 使用方法

### ローカルテスト（公開せずに実行）

```bash
make test-run
```

生成された`email.html`ファイルで結果を確認できます。

このコマンドは、最新のフィードを取得して翻訳しますが、公開はしません。翻訳結果は `YYYY-MM-DD_translated.md` として保存されます。

### 手動でGitHub Actionsを実行

1. Actions タブを開く
2. "AI Newsletter Pipeline" ワークフローを選択
3. "Run workflow" をクリック

## プロジェクト構成

```
ainews/
├── scripts/              # パイプラインスクリプト
│   ├── fetch.py         # RSSフィード取得
│   ├── convert.py       # HTML→Markdown変換
│   ├── translate.py     # 日本語翻訳
│   └── summarize.py     # Discord用要約生成
├── prompts/             # プロンプト
│   └── translator.txt   # 翻訳プロンプト
├── public/              # 静的サイト
│   └── index.html       # ランディングページ
├── .github/
│   └── workflows/
│       └── pipeline.yml # GitHub Actions設定
├── pyproject.toml       # Pythonプロジェクト設定
├── Makefile            # 開発コマンド
├── latest.txt          # 処理済みGUID追跡
├── PRD.md              # プロダクト要求定義書
├── CLAUDE.md           # Claude Code用ガイド
└── README.md           # このファイル
```

## トラブルシューティング

### 翻訳品質エラー

品質スコアが0.95未満の場合、翻訳は失敗します。以下を確認してください：
- Azure OpenAIのクォータ制限
- GPT-4デプロイメントの設定
- プロンプトファイルの内容

### RSS フィードエラー

- `latest.txt`ファイルを削除して重複チェックをリセット
- フィードURLが正しいか確認

### Discord通知エラー

- Webhook URLの有効性を確認
- Discordサーバーの権限設定を確認

## 翻訳アーカイブの取得

翻訳されたニュースレターは、GitHub Actionsの各実行のアーティファクトとして保存されます：

1. Actions タブを開く
2. 実行履歴から目的の日付を選択
3. "Artifacts" セクションから `translated-newsletter-YYYY-MM-DD` をダウンロード

## ライセンス

MIT License

## 貢献

プルリクエストを歓迎します。大きな変更の場合は、まずイシューを作成して変更内容を議論してください。