# ---------------------------------------------------
# AI PROMPTS
# ---------------------------------------------------

SUMMARY_PROMPT = """
You are a professional fintech news summarizer.

TASK:
Summarize the fintech news article in ONLY 2 concise professional sentences.

STRICT RULES:
- Return ONLY plain text
- DO NOT use HTML
- DO NOT use markdown
- DO NOT use code blocks
- DO NOT use bullet points
- DO NOT generate tags like <div>, <span>, <p>
- ONLY return summary text

ARTICLE TITLE:
{title}

ARTICLE SUMMARY:
{summary}
"""

RANKING_PROMPT = """
Analyze the importance of this fintech news article.

Consider:
- global financial impact
- AI innovation
- banking influence
- funding significance
- cybersecurity relevance
- fintech market importance

Return ONLY a score from 1 to 10.

ARTICLE:
{article}
"""

TRENDING_TOPICS_PROMPT = """
Analyze all fintech news articles and identify the top trending fintech topics.

Examples:
- Open Banking
- Embedded Finance
- AI Payments
- Crypto Regulation

Return ONLY topic names.
"""