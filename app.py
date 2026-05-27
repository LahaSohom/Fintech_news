import streamlit as st
from agents import run_agent
import re

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="AI Fintech News Agent",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------

st.markdown("""
<style>
/* Hide Streamlit Branding */
#MainMenu, footer, header {visibility: hidden;}

/* Main Background */
.stApp {
    background:
        radial-gradient(circle at top left, rgba(59,130,246,0.15), transparent 25%),
        radial-gradient(circle at bottom right, rgba(124,58,237,0.15), transparent 25%),
        linear-gradient(135deg,#0f172a 0%,#111827 50%,#020617 100%);
    color: white;
    min-height: 100vh;
}

/* Main Container */
.block-container {padding: 2rem 0; max-width: 1200px;}

/* Title */
.main-title {
    font-size: 3.5rem; font-weight: 800; text-align: center;
    color: white; margin-bottom: 10px; letter-spacing: -1px;
}

/* Subtitle */
.sub-title {
    text-align: center; font-size: 1.1rem; color: #cbd5e1; margin-bottom: 50px;
}

/* Glass Card */
.news-card {
    background: rgba(255,255,255,0.08);
    border-radius: 24px; padding: 30px; margin-bottom: 30px;
    backdrop-filter: blur(18px); -webkit-backdrop-filter: blur(18px);
    border: 1px solid rgba(255,255,255,0.12);
    box-shadow: 0 8px 32px rgba(0,0,0,0.35), inset 0 1px 1px rgba(255,255,255,0.08);
    transition: all 0.3s ease;
}
.news-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 16px 40px rgba(0,0,0,0.45), inset 0 1px 1px rgba(255,255,255,0.1);
}

/* News Title */
.news-title {font-size: 1.6rem; font-weight: 700; color: white; margin-bottom: 20px; line-height: 1.4;}

/* Badge Container */
.badge-container {margin-bottom: 18px;}

/* Source Badge */
.source-badge {
    display: inline-block; padding: 7px 14px; border-radius: 999px;
    background: rgba(59,130,246,0.18); color: #93c5fd;
    font-size: 0.82rem; font-weight: 600; margin-right: 10px;
    border: 1px solid rgba(147,197,253,0.2);
}

/* Importance Badge */
.importance-badge {
    display: inline-block; padding: 7px 14px; border-radius: 999px;
    background: rgba(16,185,129,0.18); color: #6ee7b7;
    font-size: 0.82rem; font-weight: 600;
    border: 1px solid rgba(110,231,183,0.2);
}

/* Summary */
.news-summary {color: #e2e8f0; line-height: 1.9; font-size: 1rem; margin-top: 15px;}
.news-summary p {margin: 0;}

/* Date */
.news-date {
    color: #94a3b8; margin-top: 24px; font-size: 0.85rem;
    border-top: 1px solid rgba(255,255,255,0.08); padding-top: 16px;
}

/* Button */
.stButton > button {
    width: 100%; border: none; border-radius: 14px; padding: 0.9rem 2rem;
    font-size: 1rem; font-weight: 700; color: white;
    background: linear-gradient(135deg,#2563eb,#7c3aed);
    box-shadow: 0 8px 20px rgba(37,99,235,0.25);
    transition: all 0.3s ease;
}
.stButton > button:hover {
    transform: scale(1.02);
    box-shadow: 0 12px 28px rgba(124,58,237,0.35);
}

/* Spinner Text */
.stSpinner > div {color: white;}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# HEADER
# ---------------------------------------------------

st.markdown('<div class="main-title">🚀 AI Fintech News Agent</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Top AI-powered fintech news from the last 24 hours</div>', unsafe_allow_html=True)

# ---------------------------------------------------
# BUTTON
# ---------------------------------------------------

if st.button("Fetch Latest Fintech News"):
    with st.spinner("Fetching latest fintech news..."):
        articles = run_agent()

        if not articles:
            st.warning("No fintech news found in the last 24 hours.")
        else:
            for article in articles:
            # Clean summary
                clean_summary = (
                    article.get('summary', '')
                    .replace("```html", "")
                    .replace("```markdown", "")
                    .replace("```", "")
                    .replace("<br>", " ")
                    .strip()
                )
                import re
                clean_summary = re.sub(r"<.*?>", "", clean_summary)

                # Render card with link
                st.markdown(f"""
                <div class="news-card">
                    <div class="news-title">📰 {article.get('title','')}</div>
                    <div class="badge-container">
                        <span class="source-badge">{article.get('source','')}</span>
                        <span class="importance-badge">⭐ Importance Score: {article.get('importance_score','')}</span>
                    </div>
                    <div class="news-summary">{clean_summary}</div>
                    <div class="news-date">⏰ Published: {article.get('published','')}</div>
                    <div style="margin-top:15px;">
                        🔗 <a href="{article.get('url','')}" target="_blank" style="color:#60a5fa; font-weight:600;">
                            Read Full Article
                        </a>
                    </div>
                </div>
                """, unsafe_allow_html=True)
