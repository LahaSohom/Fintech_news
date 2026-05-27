# Skill: Fetch Fintech News

## Purpose
Fetch the latest fintech news articles from trusted global news sources using RSS feeds.

## Trusted Sources
- TechCrunch Fintech
- Finextra
- Reuters Business
- PYMNTS
- CoinDesk

## Steps

### Step 1 — Connect to RSS Feeds
Retrieve the latest fintech news entries from all configured RSS feeds.

### Step 2 — Parse Feed Data
Extract:
- title
- summary
- article_url
- source
- published_date

### Step 3 — Normalize Data
Convert all article data into a consistent JSON structure.

### Step 4 — Return Articles
Return a clean list of fintech news articles for further processing.

## Rules
- Only use trusted sources
- Ignore malformed articles
- Ignore empty summaries
- Avoid duplicate RSS entries