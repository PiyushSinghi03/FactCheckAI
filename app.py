# ====================================
# app.py — Enhanced UI for FactCheckAI
# ====================================

import streamlit as st
from final import get_news_articles, get_fact_check_articles, classify_news_with_gemini

# Streamlit Page Config
st.set_page_config(
    page_title="Fact Or Fake? - AI Fact Checker",
    page_icon="🧠",
    layout="wide",
)

# --------------------------
# 🌈 Modern UI Styling
# --------------------------
st.markdown("""
<style>
/* Background Gradient */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(145deg, #eef2f3 0%, #8e9eab 100%);
    font-family: 'Inter', sans-serif;
    color: #1C1C1C;
}

/* Title */
.title {
    text-align: center;
    font-size: 52px;
    font-weight: 800;
    color: #1C1C1C;
    margin-top: 30px;
}
.title span {
    color: #2e7d32;
}

/* Subtitle */
.subtitle {
    text-align: center;
    font-size: 18px;
    color: #555;
    margin-bottom: 25px;
}

/* Input box */
.stTextInput > div > div > input {
    background-color: #ffffff;
    color: #222;
    border-radius: 12px;
    border: 2px solid #2e7d32;
    padding: 14px;
    font-size: 16px;
}

/* Button */
.stButton > button {
    background-color: #2e7d32;
    color: white;
    font-weight: bold;
    font-size: 16px;
    border-radius: 10px;
    padding: 10px 24px;
    border: none;
    transition: all 0.3s ease;
}
.stButton > button:hover {
    background-color: #256428;
    transform: translateY(-2px);
}

/* Cards */
.card {
    background-color: white;
    border-radius: 16px;
    padding: 18px 22px;
    margin-top: 10px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.08);
}
.card a {
    text-decoration: none;
    color: #0078D4;
    font-weight: 600;
}

/* Verdict Styles */
.verdict-real {
    color: #2e7d32;
    font-weight: 700;
    font-size: 22px;
}
.verdict-fake {
    color: #c62828;
    font-weight: 700;
    font-size: 22px;
}
.reason {
    color: #333;
    font-size: 16px;
    margin-top: 6px;
}

/* Divider */
hr {
    border: 0;
    border-top: 1px solid #ccc;
    margin: 25px 0;
}
</style>
""", unsafe_allow_html=True)

# --------------------------
# 🧠 Header
# --------------------------
st.markdown("<div class='title'>Fact <span>Or Fake?</span></div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>AI-powered tool to verify news, rumors, and social media claims — instantly.</div>", unsafe_allow_html=True)
st.markdown("---")

# --------------------------
# 🧾 Input
# --------------------------
query = st.text_input("🔍 Enter a news headline to verify:")

if st.button("Check Authenticity"):
    if not query.strip():
        st.warning("⚠️ Please enter a headline first.")
    else:
        with st.spinner("🤖 Checking facts, fetching articles, and analyzing with AI..."):
            news_articles = get_news_articles(query)
            fact_check_articles = get_fact_check_articles(query)

        # --------------------------
        # 🗞 Trusted News Sources
        # --------------------------
        st.subheader("📰 Related News Sources")
        if news_articles:
            for i, (title, link) in enumerate(news_articles, 1):
                st.markdown(f"""
                <div class="card">
                    <b>{i}. <a href="{link}" target="_blank">{title}</a></b>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No relevant news articles found.")

        # --------------------------
        # 🔍 Fact-Check Reports
        # --------------------------
        st.subheader("✅ Fact-Checking Reports")
        if fact_check_articles:
            for i, (title, link) in enumerate(fact_check_articles, 1):
                st.markdown(f"""
                <div class="card">
                    <b>{i}. <a href="{link}" target="_blank">{title}</a></b>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No existing fact-check reports found online.")

        st.markdown("<hr>", unsafe_allow_html=True)

        # --------------------------
        # 🧠 Gemini AI Verdict
        # --------------------------
        st.subheader("🧠 AI Fact-Check Verdict")
        with st.spinner("Analyzing evidence and reasoning..."):
            result = classify_news_with_gemini(query, news_articles, fact_check_articles)

        verdict_line = ""
        reason_line = ""
        for line in result.splitlines():
            if line.lower().startswith("verdict:"):
                verdict_line = line.split(":", 1)[1].strip()
            elif line.lower().startswith("reason:"):
                reason_line = line.split(":", 1)[1].strip()

        # Verdict Display
        if "real" in verdict_line.lower():
            verdict_class = "verdict-real"
            emoji = "✅"
        elif "fake" in verdict_line.lower():
            verdict_class = "verdict-fake"
            emoji = "❌"
        else:
            verdict_class = ""
            emoji = "⚠️"

        st.markdown(f"""
        <div class="card">
            <div class="{verdict_class}">{emoji} Verdict: {verdict_line}</div>
            <div class="reason"><b>Reason:</b> {reason_line}</div>
        </div>
        """, unsafe_allow_html=True)
