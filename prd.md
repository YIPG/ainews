# Product Requirements Document — Japanese AI Newsletter Translation Archive

Version: 1.0   Author: AI Team   Status: Production

---

## 1. Objective

Provide a minimal-maintenance pipeline that:

1. Retrieves AI newsletters from RSS feeds daily (weekdays only)
2. Produces high-quality Japanese translations using Azure OpenAI GPT-5
3. Archives translated content as GitHub Actions artifacts (30-day retention)
4. Sends Discord notifications with summaries when new translations are available
5. Maintains a static landing page for project information

Goal: Fully automated, <$3/month runtime cost, zero-maintenance operation

---

## 2. Scope

**In scope:**
- Frontend landing page (static HTML/CSS)
- GitHub Actions workflow for automation
- Translation via Azure OpenAI GPT-5
- GitHub Actions artifact storage
- Discord webhook integration for notifications
- Basic error monitoring via Slack/Discord

**Out of scope:**
- Email distribution system
- Subscription management
- Paid tiers or monetization
- Multi-language support beyond Japanese
- Long-term archival beyond 30 days

---

## 3. Glossary

| Term | Definition |
|------|------------|
| Issue | One AI newsletter article (HTML/Markdown) |
| Pipeline | The GitHub Actions job that processes an issue |
| AOAI | Azure OpenAI |
| Artifact | GitHub Actions storage for translated content |
| GUID | Unique identifier for RSS feed items |

---

## 4. Architecture Overview

```
RSS Feed ──▶ GitHub Actions ──▶ Azure OpenAI ──▶ GH Artifacts
                    │                               │
                    └─── Weekdays 15:00 UTC ────────┘
                                                    │
                                                    ▼
                                            Discord Webhook
```

- Static site served from gh-pages branch (informational only)
- Pipeline runs in main branch via .github/workflows/pipeline.yml
- Translations stored as GitHub Actions artifacts
- Discord receives notifications with summaries

---

## 5. Component Design

### 5.1 Static Landing Page

**File:** `public/index.html`

Simple informational page explaining the project:
- Project description in Japanese
- Link to GitHub repository
- No subscription functionality (archive-only system)

### 5.2 GitHub Actions Workflow

| Step | Script | Description |
|------|--------|-------------|
| fetch_feed | `scripts/fetch.py` | Downloads RSS feed, saves HTML/metadata, checks GUID |
| convert | `scripts/convert.py` | Converts HTML to Markdown using html2text |
| translate | `scripts/translate.py` | Translates to Japanese via Azure OpenAI |
| summarize | `scripts/summarize.py` | Extracts title and ~1500 char summary |
| upload | GitHub Actions | Stores translated content as artifact |
| notify | Discord webhook | Sends summary with download link |
| update_guid | Git commit | Updates latest.txt with processed GUID |

### 5.3 Required Secrets

| Name | Purpose | Example |
|------|---------|---------|
| FEED_URL | RSS feed URL | https://example.com/feed/ |
| AOAI_ENDPOINT | Azure OpenAI endpoint | https://resource.openai.azure.com/ |
| AOAI_KEY | Azure OpenAI API key | xxxxxxxxxxxx |
| AOAI_DEPLOYMENT | GPT-5 deployment name | gpt-5-deployment |
| DISCORD_WEBHOOK | Discord notifications | https://discord.com/api/webhooks/... |
| SLACK_WEBHOOK | Error notifications (optional) | https://hooks.slack.com/... |

### 5.4 Translation Configuration

**System Prompt** (`prompts/translator.txt`):
- Business-appropriate Japanese (丁寧体)
- Preserve proper nouns in original language
- Full-width characters for headers
- Maintain Markdown formatting
- Temperature: 0.2, max_tokens: 4096

### 5.5 Error Handling

- Feed returns 304 or duplicate GUID → Skip (exit 0)
- Azure OpenAI 429 errors → Retry with exponential backoff (3x)
- Translation quality < 0.95 → Build fails
- Any failure → Slack/Discord alert sent

---

## 6. Data Flow

1. **Fetch:** RSS feed → `YYYY-MM-DD_issue.html` + `YYYY-MM-DD_meta.json`
2. **Convert:** HTML → `YYYY-MM-DD_markdown.md`
3. **Translate:** English Markdown → `YYYY-MM-DD_translated.md`
4. **Archive:** Upload all files as GitHub Actions artifact
5. **Notify:** Extract summary → Send to Discord with artifact link
6. **Track:** Update `latest.txt` with processed GUID

---

## 7. Non-Functional Requirements

| Area | Target |
|------|--------|
| Pipeline Latency | < 5 minutes per run |
| Error Rate | < 1% monthly |
| Cost | < $3/month (30 issues) |
| Retention | 30 days (GitHub Actions limit) |
| Schedule | Weekdays 15:00 UTC |
| Security | All secrets via GitHub Secrets |

---

## 8. Development Commands

```bash
make venv          # Create Python virtual environment
make test-run      # Process latest feed locally (no publishing)
```

---

## 9. Discord Notification Format

**Success Message:**
- Title: "🗾 AI技術ニュースレター - YYYY-MM-DD"
- Description: ~1500 character summary
- Link: Download full version from GitHub Actions
- Footer: "Translated by Azure OpenAI GPT-5"
- Color: Green (#00ff00)

**Error Message:**
- Title: "❌ Translation Pipeline Failed"
- Description: Error details
- Link: GitHub Actions logs
- Color: Red (#ff0000)

---

## 10. Migration from Original Design

This system has pivoted from the original email distribution design:

| Original | Current | Reason |
|----------|---------|---------|
| Buttondown email delivery | GitHub Actions artifacts | Simpler, no subscription management |
| Email subscriber database | Discord notifications | No user data to manage |
| Jinja2 email templates | Direct Markdown storage | Cleaner archival format |
| Daily at 00:00 UTC | Weekdays at 15:00 UTC | Better alignment with content publishing |

---

## 11. Future Considerations

- Add web UI to browse archived translations
- Implement RSS feed for translated content
- Support multiple newsletter sources
- Add search functionality for archives
- Consider long-term storage solution beyond 30 days

---

## 12. Acceptance Criteria

1. ✅ Pipeline successfully fetches and translates new RSS items
2. ✅ Translations achieve quality score ≥ 0.95
3. ✅ Discord receives formatted notifications with summaries
4. ✅ Duplicate items are skipped without errors
5. ✅ Total GitHub Action duration ≤ 300 seconds
6. ✅ All secrets properly configured and documented

---

End of Document