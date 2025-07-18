
# AI Newsletter Japan

A Japanese translation and archive system for AI newsletters – Automatically translates AI newsletter content into Japanese, archives it via GitHub Actions, and sends notifications to Discord.

**🌐 Live Site: https://yipg.github.io/ainews/**

## Overview

This project is an automated pipeline that retrieves the latest AI newsletters from specified RSS feeds, translates them into Japanese using Azure OpenAI GPT-4o, and publishes them to a GitHub Pages website. A summary is also sent to Discord upon completion.

## Features

* 🔄 Automatic retrieval and deduplication from RSS feeds
* 🌐 High-quality Japanese translation via Azure OpenAI GPT-4o
* ✅ Automatic translation quality check (score ≥ 0.95)
* 📖 Auto-publishing to GitHub Pages with RSS feed
* 💬 Discord webhook notifications with summary
* 🕐 Runs automatically on weekdays at 15:00 UTC (8:00 AM Pacific Time)
* 🔔 Optional error notifications via Slack and Discord

## Setup

### Prerequisites

* Python 3.8 or later
* Azure OpenAI account with GPT-4o deployment
* GitHub account (for GitHub Actions)
* Discord Webhook URL (optional, for notifications)

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/ainews.git
cd ainews
```

### 2. Set up the virtual environment

```bash
make venv
```

### 3. Set environment variables

Set the following environment variables for local testing:

```bash
export FEED_URL="your-rss-feed-url"
export AOAI_ENDPOINT="https://your-resource.openai.azure.com/"
export AOAI_KEY="your-azure-openai-key"
export AOAI_DEPLOYMENT="your-gpt4o-deployment-name"
export DISCORD_WEBHOOK="your-discord-webhook-url"  # optional
export SLACK_WEBHOOK="your-slack-webhook-url"      # optional
```

### 4. Set GitHub Secrets

Go to GitHub repo: Settings → Secrets and variables → Actions, and add the following secrets:

* `FEED_URL` – RSS feed URL
* `AOAI_ENDPOINT` – Azure OpenAI endpoint
* `AOAI_KEY` – Azure OpenAI API key
* `AOAI_DEPLOYMENT` – GPT-4o deployment name
* `DISCORD_WEBHOOK` – Discord webhook URL (optional)
* `SLACK_WEBHOOK` – Slack webhook URL (optional)

### 5. Enable GitHub Pages

1. Go to Settings → Pages
2. Source: Deploy from a branch
3. Branch: `main` / folder: `/docs`
4. Save

### 6. Schedule automation

GitHub Actions will run automatically on weekdays at 15:00 UTC (8:00 AM PT). Manual runs are also possible.

## Usage

### Local test run (without publishing)

```bash
make test-run
```

You can check the result in the generated `email.html` file.

This command fetches and translates the latest feed but does not publish it. The translation result is saved as `YYYY-MM-DD_translated.md`.

### Run GitHub Actions manually

1. Open the Actions tab
2. Select the "AI Newsletter Pipeline" workflow
3. Click "Run workflow"

## Project Structure

```
ainews/
├── scripts/              # Pipeline scripts
│   ├── fetch.py         # RSS feed fetching
│   ├── convert.py       # HTML to Markdown conversion
│   ├── translate.py     # Japanese translation
│   └── summarize.py     # Discord summary generation
├── prompts/             # Prompt templates
│   └── translator.txt   # Translation prompt
├── docs/                # GitHub Pages content
│   ├── index.html       # Landing page
│   ├── feed.xml         # RSS feed
│   └── newsletters/     # Published newsletters
├── .github/
│   └── workflows/
│       └── pipeline.yml # GitHub Actions workflow
├── pyproject.toml       # Python project config
├── Makefile             # Dev commands
├── latest.txt           # Processed GUID tracking
├── PRD.md               # Product requirements doc
├── CLAUDE.md            # Claude Code guidance
└── README.md            # This file
```

## Troubleshooting

### Translation Quality Error

If the quality score is below 0.95, translation fails. Check the following:

* Azure OpenAI quota limits
* GPT-4 deployment configuration
* Contents of the prompt file

### RSS Feed Error

* Delete `latest.txt` to reset duplication checks
* Ensure the feed URL is correct

### Discord Notification Error

* Check if the webhook URL is valid
* Verify Discord server permissions

## Access Translated Newsletters

All translated newsletters are available on the live website:

* **Live Site**: https://yipg.github.io/ainews/
* **RSS Feed**: https://yipg.github.io/ainews/docs/feed.xml
* **Archive**: Browse all newsletters from the homepage

GitHub Actions artifacts are also retained for 30 days as backup.

## License

MIT License

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
