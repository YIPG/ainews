# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Japanese AI Newsletter Pipeline that automatically translates Smol AI newsletters from English to Japanese and publishes them via Buttondown. The system is designed to be fully automated with minimal maintenance, running on GitHub Actions with Azure OpenAI for translation.

## Architecture

- **Frontend**: Static HTML/CSS landing page served from gh-pages branch (public/index.html)
- **Backend**: GitHub Actions workflow (.github/workflows/pipeline.yml) that runs daily at 00:00 UTC
- **Translation**: Azure OpenAI GPT-4 for English to Japanese translation
- **Publishing**: Buttondown API for email distribution
- **Monitoring**: Optional Slack notifications on failure

## Development Commands

Based on the PRD, the following Makefile targets should be available:

```bash
make venv          # Create Python virtual environment
make test-run      # Process latest feed but do not publish
make send-draft    # Publish to Buttondown as draft
```

## Pipeline Components

The automated pipeline consists of these Python scripts (in scripts/ directory):

1. **fetch.py** - Retrieves RSS feed from news.smol.ai, writes issue.html & meta.json
2. **convert.py** - Converts HTML to Markdown using html2text
3. **translate.py** - Translates English to Japanese using Azure OpenAI
4. **render.py** - Composes email using Jinja2 template (templates/issue.j2)
5. **publish.py** - Publishes to Buttondown via REST API

## Required Secrets

The following GitHub Secrets must be configured:

- `FEED_URL` - RSS feed URL (https://news.smol.ai/feed/)
- `BD_API_KEY` - Buttondown API token
- `AOAI_ENDPOINT` - Azure OpenAI endpoint
- `AOAI_KEY` - Azure OpenAI API key
- `AOAI_DEPLOYMENT` - Azure OpenAI deployment name
- `SLACK_WEBHOOK` - Optional Slack webhook for notifications

## Translation Guidelines

The system uses a specific Japanese translation prompt (prompts/translator.txt) with these rules:
- Headers in full-width characters
- Proper nouns and company names kept in original language
- Maintain Markdown formatting for lists
- Use polite business Japanese (丁寧体), not casual speech

## Error Handling

- Feed returns 304 or no new GUID → job exits successfully (skip)
- Azure OpenAI 429 errors → retry with exponential backoff (3x)
- Any failure after translation → sends Slack alert
- Quality check must score ≥ 0.95 or build fails

## Performance Targets

- Pipeline latency: < 5 minutes per run
- Error rate: < 1% monthly
- Cost: < $3/month at 30 issues
- GitHub Action duration: ≤ 300 seconds

## Development Environment

Uses Python virtual environment with dependencies defined in pyproject.toml. All scripts share the same virtualenv for consistency.