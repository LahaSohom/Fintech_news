import os
import re
import feedparser

from dotenv import load_dotenv
from openai import OpenAI

from datetime import datetime, timezone, timedelta
from dateutil import parser

# ---------------------------------------------------
# LOAD ENV VARIABLES
# ---------------------------------------------------

load_dotenv()

# ---------------------------------------------------
# GROQ CLIENT
# ---------------------------------------------------

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

# ---------------------------------------------------
# FALLBACK MODELS
# ---------------------------------------------------

MODELS = [
    "llama-3.3-70b-versatile",
    "deepseek-r1-distill-llama-70b",
    "mixtral-8x7b-32768",
    "gemma2-9b-it"
]

# ---------------------------------------------------
# RSS FEEDS (Branded Sources)
# ---------------------------------------------------

RSS_FEEDS = [
    "https://techcrunch.com/category/fintech/feed/",
    "https://www.finextra.com/rss/fullnews.aspx",
    "https://www.pymnts.com/feed/",
    "https://www.thefintechtimes.com/feed/",
    "https://www.fintechfutures.com/feed/",
    "https://www.tearsheet.co/feed/",
    "https://fintech.global/feed/",
    "https://thepaypers.com/rss.xml",
    "https://www.paymentsdive.com/feeds/news/",
    "https://thefinancialbrand.com/feed/",
    "https://americanbanker.com/rss",
    "https://fintechmagazine.com/rss",
    "https://thefinanser.com/feed/",
    "https://sifted.eu/feed/"
]

TRUSTED_SOURCES = [
    "TechCrunch", "Finextra", "PYMNTS", 
    "The Fintech Times", "Fintech Futures",
    "Tearsheet", "FinTech Global", "The Paypers", 
    "Payments Dive", "The Financial Brand", "American Banker",
    "FinTech Magazine", "The Finanser", "Sifted"
]

# ---------------------------------------------------
# ASK LLM WITH MODEL FALLBACK
# ---------------------------------------------------

def ask_llm(prompt):
    for model in MODELS:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.4,
                max_tokens=150
            )
            print(f"Using model: {model}")
            return response.choices[0].message.content
        except Exception as e:
            print(f"{model} failed")
            print(e)
    return "Unable to generate summary."

# ---------------------------------------------------
# CHECK LAST 24 HOURS
# ---------------------------------------------------

def is_within_24_hours(published_date):
    try:
        article_time = parser.parse(published_date)
        current_time = datetime.now(timezone.utc)
        difference = current_time - article_time
        return difference <= timedelta(hours=24)
    except Exception:
        return False

# ---------------------------------------------------
# FETCH NEWS
# ---------------------------------------------------

def fetch_news():
    articles = []
    seen_titles = set()

    for feed_url in RSS_FEEDS:
        try:
            feed = feedparser.parse(feed_url)
            source_name = feed.feed.get("title", "Unknown Source")

            # ✅ Allow trusted sources by substring match (case-insensitive)
            if not any(trusted.lower() in source_name.lower() for trusted in TRUSTED_SOURCES):
                continue

            for entry in feed.entries:
                published = entry.get("published", "")
                if not is_within_24_hours(published):
                    continue

                title = entry.get("title", "").strip()
                summary = entry.get("summary", "").strip()
                url = entry.get("link", "").strip()   # ✅ Capture article link

                if not title or not summary or not url:
                    continue

                normalized_title = title.lower()
                if normalized_title in seen_titles:
                    continue
                seen_titles.add(normalized_title)

                articles.append({
                    "title": title,
                    "summary": summary,
                    "published": published,
                    "source": source_name,
                    "url": url   # ✅ Include URL
                })

        except Exception as e:
            print(f"Feed Error: {feed_url}")
            print(e)

    return articles

# ---------------------------------------------------
# RANK NEWS
# ---------------------------------------------------

def rank_news(articles):
    fintech_keywords = [
        "ai", "bank", "payment", "crypto", "fintech", "startup",
        "funding", "regulation", "digital", "investment", "fraud",
        "cybersecurity", "open banking", "embedded finance"
    ]

    ranked_articles = []
    for article in articles:
        score = 0
        combined_text = (article["title"] + " " + article["summary"]).lower()
        for keyword in fintech_keywords:
            if keyword in combined_text:
                score += 1
        article["importance_score"] = score
        ranked_articles.append(article)

    ranked_articles.sort(key=lambda x: x["importance_score"], reverse=True)
    return ranked_articles

# ---------------------------------------------------
# CLEAN AI OUTPUT
# ---------------------------------------------------

def clean_summary(text):
    text = re.sub(r'<.*?>', '', text)
    text = (
        text.replace("```html", "")
            .replace("```markdown", "")
            .replace("```", "")
            .replace("#", "")
            .replace("*", "")
            .replace("<br>", " ")
    )
    return text.strip()

# ---------------------------------------------------
# SUMMARIZE NEWS
# ---------------------------------------------------

def summarize_news(articles):
    summarized_articles = []
    for article in articles[:5]:
        prompt = f"""
You are a professional fintech news summarizer.

TASK:
Summarize the fintech news article in ONLY 2 concise professional sentences.

STRICT RULES:
- Return ONLY plain text
- DO NOT use HTML
- DO NOT use markdown
- DO NOT use code blocks
- DO NOT use bullet points
- DO NOT use symbols like ``` or ###
- DO NOT generate tags like <div>, <span>, <p>
- DO NOT format the response
- ONLY return the summary text

ARTICLE TITLE:
{article['title']}

ARTICLE SUMMARY:
{article['summary']}
"""
        ai_summary = ask_llm(prompt)
        ai_summary = clean_summary(ai_summary)

        summarized_articles.append({
            "title": article["title"],
            "summary": ai_summary,
            "published": article["published"],
            "source": article["source"],
            "importance_score": article["importance_score"],
            "url": article["url"]   # ✅ Keep URL in final output
        })

    return summarized_articles

# ---------------------------------------------------
# MAIN AGENT PIPELINE
# ---------------------------------------------------

def run_agent():
    articles = fetch_news()
    ranked_articles = rank_news(articles)
    summarized_articles = summarize_news(ranked_articles)
    return summarized_articles
