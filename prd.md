ign Document — Japanese AI Newsletter Pipeline (Smol AI → Buttondown)

Version: 0.1   Author: ChatGPT   Status: Draft


---

1. Objective

Provide a minimal‑maintenance pipeline that

1. Lets users subscribe via a single email field (Buttondown embed on a static page).


2. Retrieves the news@smol.ai RSS feed once a day.


3. Produces a high‑quality Japanese translation.


4. Publishes the translated issue through Buttondown as an email broadcast.



Goal: fully automated, <$1/month runtime under MS employee Azure credit.


---

2. Scope

In scope – frontend landing page, GitHub Actions workflow, translation via Azure OpenAI (GPT‑4.1), Buttondown API integration, basic monitoring.

Out of scope – paid subscription tiers, analytics beyond Buttondown default, multi‑language support.



---

3. Glossary

Term	Definition

Issue	One Smol AI newsletter article (HTML)
Pipeline	The GH Actions job that processes an issue.
BD	Buttondown.
AOAI	Azure OpenAI.



---

4. Architecture Overview

User ──▶ Static Site (GitHub Pages) ──▶ Buttondown (Subscriber DB)
                                             ▲
                                             │ (REST API)
GitHub Actions ── cron 00:00 UTC ──▶ Pipeline ─┘

Static site is pure HTML/CSS served from gh-pages branch.

Pipeline lives in main branch under .github/workflows/pipeline.yml.

AOAI handles translation; secrets stored in GitHub Secrets.



---

5. Component Design

5.1 Static Landing Page

File: public/index.html

Uses BD embed form:

<form action="https://buttondown.email/api/emails/subscribe" method="post" target="popupwindow" onsubmit="window.open('https://buttondown.email/<ACCOUNT>', 'popupwindow');return true;">
  <input type="email" name="email" placeholder="メールアドレス" required>
  <input type="hidden" name="embed" value="1">
  <button type="submit">購読する</button>
</form>

Optional reCaptcha is disabled (set in BD dashboard).


5.2 GitHub Actions Workflow

Step	Tool	Key Points

fetch_feed	feedparser	Save latest entry GUID to artifact latest.txt for dedup.
html_to_md	html2text==2020.1.16	Preserve headings/links.
translate	openai>=1.3.5 (Azure)	System prompt stored in repo prompts/translator.txt. Temperature 0.2, max_tokens 4096.
quality_check	same AOAI call	Ask model to detect missing sentences & hallucinations. Fail build if score < 0.95.
compose_email	Jinja2 template	Template at templates/issue.j2 (front‑matter for BD).
publish	curl to BD REST	POST /emails with draft=false.
notify	actions/slack@v2 (optional)	Alert on failure.


5.2.1 Secrets

Name	Used by	Example

FEED_URL	fetch_feed	https://news.smol.ai/feed/
BD_API_KEY	publish	xxxxxxxx_token
AOAI_ENDPOINT	translate	https://aoai-jp-east.openai.azure.com/
AOAI_KEY	translate	xxxxxxxxxxxx
AOAI_DEPLOYMENT	translate	gpt4-1-translation
SLACK_WEBHOOK	notify	(optional)


5.3 Translation Prompt (system)

あなたはバイリンガル編集者です。入力はMarkdownの英語ニュースレターです。以下のルールで日本語に翻訳してください。
- 見出しは全角。
- 固有名詞・社名は原文のまま。
- 箇条書きはMarkdownのまま保持。
- 口語ではなく、ビジネス向けの丁寧体。

5.4 Error Handling

If feed returns 304 or no new GUID → job exits 0 (skip).

If AOAI raises 429 → retry w/ exponential backoff 3×.

Any failure after translate sends Slack alert.



---

6. Data Flow Detail

1. Pull RSS: python scripts/fetch.py writes issue.html & meta.json.


2. Convert: python scripts/convert.py issue.html > issue.md.


3. Translate: python scripts/translate.py issue.md > issue_ja.md.


4. Compose: python scripts/render.py meta.json issue_ja.md > email.html.


5. Publish: python scripts/publish.py email.html.



All scripts share a common virtualenv defined in pyproject.toml.


---

7. Non‑Functional Requirements

Area	Target

Latency	< 5 min per run (AOAI biggest chunk)
Error rate	< 1% monthly (manual resend allowed)
Cost	< $3/month at 30 issues
Security	All secrets via GitHub OIDC (no plaintext).



---

8. Local Development (Makefile targets)

make venv          # create .venv
make test-run      # process latest feed but do not publish
make send-draft    # publish to BD as draft


---

9. Future Work

Switch BD→Listmonk+SES for cost scaling.

Add caching to avoid re‑translating unchanged sentences.

Hook Lighthouse CI for landing page accessibility.

Multilingual (en → ja/ko/zh) via matrix job.



---

10. Acceptance Criteria (for AI Coding Agent)

1. gh workflow run publishes a real Buttondown email in draft mode when a new RSS item appears.


2. Generated email passes BD preview with correct Japanese, links, and no layout break.


3. On second run with no new item, workflow exits successfully without sending.


4. Total GitHub Action duration ≤ 300 sec.


5. README includes setup guide & secrets list.




---

End of Document

