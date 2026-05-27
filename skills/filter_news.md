# Skill: Filter Latest Fintech News

## Purpose
Keep only fintech news articles published within the last 24 hours.

## Steps

### Step 1 — Validate Published Date
Check the publication timestamp of every article.

### Step 2 — Remove Old Articles
Discard any article older than 24 hours.

### Step 3 — Validate Content
Remove:
- incomplete articles
- empty summaries
- invalid URLs

### Step 4 — Return Filtered Articles
Return only valid and recent fintech articles.

## Rules
- Timezone must be UTC
- Ignore articles with missing dates
- Keep only recent fintech-related content