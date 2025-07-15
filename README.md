# AI Newsletter Japan

日本語版AIニュースレター配信システム - Smol AI Newsの内容を自動的に日本語に翻訳してButtondownで配信します。

## 概要

このプロジェクトは、[Smol AI News](https://news.smol.ai)のRSSフィードから最新のAIニュースを取得し、Azure OpenAIを使用して日本語に翻訳し、Buttondown経由でメール配信する自動化パイプラインです。

## 機能

- 🔄 RSS フィードからの自動取得と重複チェック
- 🌐 Azure OpenAI GPT-4による高品質な日本語翻訳
- ✅ 翻訳品質の自動チェック（スコア0.95以上）
- 📧 Buttondown APIを使用した自動配信
- 🕐 毎日00:00 UTC（日本時間9:00）に自動実行
- 🔔 Slackへのエラー通知（オプション）

## セットアップ

### 前提条件

- Python 3.8以上
- Azure OpenAIアカウントとGPT-4デプロイメント
- Buttondownアカウント
- GitHubアカウント（GitHub Actions用）

### 1. リポジトリのクローン

```bash
git clone https://github.com/yourusername/ainews-jp.git
cd ainews-jp
```

### 2. 仮想環境のセットアップ

```bash
make venv
```

### 3. 環境変数の設定

ローカルテスト用に以下の環境変数を設定してください：

```bash
export FEED_URL="https://news.smol.ai/feed/"
export BD_API_KEY="your-buttondown-api-key"
export AOAI_ENDPOINT="https://your-resource.openai.azure.com/"
export AOAI_KEY="your-azure-openai-key"
export AOAI_DEPLOYMENT="your-gpt4-deployment-name"
export SLACK_WEBHOOK="your-slack-webhook-url"  # オプション
```

### 4. GitHub Secretsの設定

GitHub リポジトリの Settings → Secrets and variables → Actions で以下のシークレットを追加：

- `FEED_URL` - RSS フィードURL
- `BD_API_KEY` - Buttondown APIキー
- `AOAI_ENDPOINT` - Azure OpenAIエンドポイント
- `AOAI_KEY` - Azure OpenAI APIキー
- `AOAI_DEPLOYMENT` - GPT-4デプロイメント名
- `SLACK_WEBHOOK` - Slack Webhook URL（オプション）

### 5. GitHub Pagesの有効化

1. Settings → Pages
2. Source: Deploy from a branch
3. Branch: main / folder: /public
4. Save

### 6. Buttondown埋め込みフォームの設定

`public/index.html`の`YOUR_BUTTONDOWN_USERNAME`を実際のButtondownユーザー名に置き換えてください。

## 使用方法

### ローカルテスト（公開せずに実行）

```bash
make test-run
```

生成された`email.html`ファイルで結果を確認できます。

### ドラフトとして公開

```bash
make send-draft
```

### 手動でGitHub Actionsを実行

1. Actions タブを開く
2. "AI Newsletter Pipeline" ワークフローを選択
3. "Run workflow" をクリック

## プロジェクト構成

```
ainews-jp/
├── scripts/              # パイプラインスクリプト
│   ├── fetch.py         # RSSフィード取得
│   ├── convert.py       # HTML→Markdown変換
│   ├── translate.py     # 日本語翻訳
│   ├── render.py        # メールレンダリング
│   └── publish.py       # Buttondown公開
├── templates/           # Jinja2テンプレート
│   └── issue.j2        # メールテンプレート
├── prompts/            # プロンプト
│   └── translator.txt  # 翻訳プロンプト
├── public/             # 静的サイト
│   └── index.html      # ランディングページ
├── .github/
│   └── workflows/
│       └── pipeline.yml # GitHub Actions設定
├── pyproject.toml      # Pythonプロジェクト設定
├── Makefile           # 開発コマンド
└── README.md          # このファイル
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

### Buttondownエラー

- APIキーの有効性を確認
- アカウントの配信制限を確認

## ライセンス

MIT License

## 貢献

プルリクエストを歓迎します。大きな変更の場合は、まずイシューを作成して変更内容を議論してください。