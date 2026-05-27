# Skill: Remove Duplicate News

## Purpose
Detect and remove duplicate fintech news stories from multiple sources.

## Steps

### Step 1 — Compare Titles
Check semantic similarity between article titles.

### Step 2 — Compare Summaries
Identify articles discussing the same event or announcement.

### Step 3 — Select Best Source
Prioritize trusted sources in this order:
1. Reuters
2. Bloomberg
3. TechCrunch
4. Finextra
5. CoinDesk

### Step 4 — Remove Duplicates
Keep only one version of duplicate stories.

## Rules
- Preserve highest quality article
- Avoid repeated headlines
- Keep unique fintech events only