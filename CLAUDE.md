# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Japanese AI Newsletter Translation Archive System that automatically translates AI newsletters from English to Japanese. The system is designed to be fully automated with minimal maintenance, running on GitHub Actions every 6 hours on weekdays with Azure OpenAI GPT-5 for translation. Translated content is stored as GitHub Actions artifacts (30-day retention) and notifications are sent to Discord with summaries.

## Architecture

- **Frontend**: Static HTML/CSS landing page served from gh-pages branch (public/index.html) - informational only
- **Backend**: GitHub Actions workflow (.github/workflows/pipeline.yml) that runs every 6 hours on weekdays (00:00, 06:00, 12:00, 18:00 UTC)
- **Translation**: Azure OpenAI GPT-5 for English to Japanese translation
- **Storage**: GitHub Actions artifacts for storing translated content (30-day retention)
- **Notifications**: Discord webhook for success notifications with summaries
- **Monitoring**: Optional Slack/Discord notifications on failure

## Development Commands

Based on the PRD, the following Makefile targets should be available:

```bash
make venv          # Create Python virtual environment
make test-run      # Process latest feed and translate (no publishing)
```

## Pipeline Components

The automated pipeline consists of these Python scripts (in scripts/ directory):

1. **fetch.py** - Retrieves RSS feed from configured source, writes YYYY-MM-DD_issue.html & YYYY-MM-DD_meta.json, checks against latest.txt for duplicates
2. **convert.py** - Converts HTML to Markdown using html2text
3. **translate.py** - Translates English to Japanese using Azure OpenAI GPT-5
4. **summarize.py** - Extracts title and ~1500 character summary for Discord notification
5. **tweet.py** - Posts a short summary (≤140 chars) to Twitter/X with link to full article

All files use YYYY-MM-DD date prefixes for organization and artifact storage. The latest.txt file tracks the last processed GUID to prevent duplicate processing.

## Required Secrets

The following GitHub Secrets must be configured:

- `FEED_URL` - RSS feed URL
- `AOAI_ENDPOINT` - Azure OpenAI endpoint
- `AOAI_KEY` - Azure OpenAI API key
- `AOAI_DEPLOYMENT` - Azure OpenAI GPT-5 deployment name
- `DISCORD_WEBHOOK` - Discord webhook URL for success notifications (optional)
- `SLACK_WEBHOOK` - Slack webhook URL for error notifications (optional)
- `TWITTER_API_KEY` - Twitter/X API key for posting tweets (optional)
- `TWITTER_API_SECRET` - Twitter/X API secret (optional)
- `TWITTER_ACCESS_TOKEN` - Twitter/X access token (optional)
- `TWITTER_ACCESS_TOKEN_SECRET` - Twitter/X access token secret (optional)

## Translation Guidelines

The system uses a specific Japanese translation prompt (prompts/translator.txt) with these rules:
- Headers in full-width characters
- Proper nouns and company names kept in original language
- Maintain Markdown formatting for lists
- Use polite business Japanese (丁寧体), not casual speech

## Error Handling

- Feed returns 304 or duplicate GUID (checked against latest.txt) → job exits successfully (skip)
- Azure OpenAI 429 errors → retry with exponential backoff (3x)
- Any failure → sends Slack/Discord alert
- Quality check must score ≥ 0.95 or build fails
- Successful translation → updates latest.txt with processed GUID via git commit

## Performance Targets

- Pipeline latency: < 5 minutes per run
- Error rate: < 1% monthly
- Cost: < $3/month at 30 issues
- GitHub Action duration: ≤ 300 seconds

## Development Environment

Uses Python virtual environment with dependencies defined in pyproject.toml. All scripts share the same virtualenv for consistency.

## Key Differences from Original PRD

The system has evolved from the original email distribution design:
- **No Buttondown integration**: System focuses on archival, not email distribution
- **Discord notifications**: Replaced email delivery with Discord webhooks
- **Simplified architecture**: No email templates, subscriber management, or publishing steps
- **Archive-focused**: Emphasis on storing translations as GitHub Actions artifacts

## Discord Notification Format

When a translation completes successfully, the system sends a Discord webhook with:
- Title: "🗾 AI技術ニュースレター - YYYY-MM-DD"
- Summary: ~1500 characters extracted from the translated content
- Link: Direct link to the published article on GitHub Pages
- Footer: "Translated by Azure OpenAI GPT-5"

Note: The system no longer sends notifications when there is no new content.

## Twitter/X Integration

When new content is translated, the system automatically posts a tweet with:
- Short summary (≤100 characters) extracted from the translated content
- Direct link to the full article: `https://yipg.github.io/ainews/newsletters/YYYY-MM-DD.html`
- Total tweet length limited to 140 characters