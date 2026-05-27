# 🚀 AI Fintech News Agent

An AI-powered fintech news platform that fetches the latest fintech news articles from trusted global sources, filters news from the last 24 hours, ranks important stories, and generates professional AI summaries using Groq LLM models.

---

# ✨ Features

- Fetches real-time fintech news
- Filters articles from the last 24 hours
- Removes duplicate news
- Ranks important fintech stories
- AI-generated summaries
- Multiple Groq fallback LLM models
- Modern glassmorphism UI
- Built with Streamlit

---

# 📰 Trusted News Sources

- TechCrunch Fintech
- Finextra
- PYMNTS
- Reuters
- CoinDesk

---

# 🧠 AI Models Used

This project uses free Groq-hosted models:

- llama-3.3-70b-versatile
- deepseek-r1-distill-llama-70b
- mixtral-8x7b-32768
- gemma2-9b-it

If one model fails or reaches rate limit, another model automatically runs.

---

# 📂 Project Structure

```bash
Fintech_news/
│
├── .env
├── .gitignore
├── README.md
├── requirements.txt
│
├── agents.py
├── app.py
├── prompts.py
├── tools.py
│
├── skills/
│   ├── fetch_news.md
│   ├── filter_news.md
│   ├── deduplicate_news.md
│   ├── rank_news.md
│   ├── summarize_news.md
│   └── publish_news.md
```

---

# ⚙️ Installation

## 1. Clone Repository

```bash
git clone https://github.com/yourusername/Fintech_news.git
```

---

## 2. Open Project

```bash
cd Fintech_news
```

---

## 3. Create Virtual Environment

```bash
python -m venv venv
```

---

## 4. Activate Virtual Environment

### Windows

```bash
.\venv\Scripts\Activate
```

### Mac/Linux

```bash
source venv/bin/activate
```

---

## 5. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Setup Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key_here
```

---

# ▶️ Run The Project

```bash
streamlit run app.py
```

---

# 🌐 Streamlit UI Features

- Dark fintech dashboard
- Glassmorphism cards
- Responsive layout
- AI-generated summaries
- Importance score badges
- Real-time fintech news

---

# 📌 Future Improvements

- Trending fintech topics
- Sentiment analysis
- Auto-refresh every 24 hrs
- News category filters
- Source logos
- Cloud deployment

---

# 👨‍💻 Built With

- Python
- Streamlit
- Groq API
- RSS Feeds
- OpenAI SDK

---

# 📜 License

MIT License