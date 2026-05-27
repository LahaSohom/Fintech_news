import re

# ---------------------------------------------------
# CLEAN AI OUTPUT
# ---------------------------------------------------

def clean_ai_text(text):

    # Remove HTML tags
    text = re.sub(r'<.*?>', '', text)

    # Remove markdown/code syntax
    text = (
        text
        .replace("```html", "")
        .replace("```markdown", "")
        .replace("```", "")
        .replace("#", "")
        .replace("*", "")
        .replace("<br>", " ")
    )

    return text.strip()

# ---------------------------------------------------
# REMOVE DUPLICATE ARTICLES
# ---------------------------------------------------

def remove_duplicates(articles):

    unique_articles = []
    seen_titles = set()

    for article in articles:

        normalized_title = article["title"].lower()

        if normalized_title not in seen_titles:

            seen_titles.add(normalized_title)

            unique_articles.append(article)

    return unique_articles

# ---------------------------------------------------
# CALCULATE IMPORTANCE SCORE
# ---------------------------------------------------

def calculate_importance(article):

    fintech_keywords = [
        "ai",
        "bank",
        "payment",
        "crypto",
        "fintech",
        "startup",
        "funding",
        "regulation",
        "digital",
        "investment",
        "cybersecurity",
        "open banking",
        "embedded finance"
    ]

    score = 0

    combined_text = (
        article["title"] + " " + article["summary"]
    ).lower()

    for keyword in fintech_keywords:

        if keyword in combined_text:
            score += 1

    return score

# ---------------------------------------------------
# SORT ARTICLES BY IMPORTANCE
# ---------------------------------------------------

def sort_by_importance(articles):

    return sorted(
        articles,
        key=lambda x: x["importance_score"],
        reverse=True
    )