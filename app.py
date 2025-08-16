import streamlit as st
from final import get_news_articles, get_fact_check_articles, classify_news

st.set_page_config(page_title="Fake News Detector", layout="centered")

st.title("📰 Fake News Detection Web App")
st.write("Enter a news headline and let AI + trusted sources verify it for you.")

# Input
query = st.text_input("Enter a news headline:")

if st.button("Verify News"):
    if query.strip() == "":
        st.warning("⚠️ Please enter a headline.")
    else:
        with st.spinner("Verifying news..."):
            news_articles = get_news_articles(query)
            fact_check_articles = get_fact_check_articles(query)

        # ✅ Trusted sources
        if news_articles:
            st.success("✅ Trusted Sources Found!")
            for i, (title, link, summary) in enumerate(news_articles, 1):
                st.write(f"**{i}. {title}**")
                st.write(f"🔗 [Read more]({link})")
                st.caption(f"📌 Summary: {summary}")
        else:
            st.warning("⚠️ No relevant articles found on Google News.")

        # ✅ Fact-checks
        if fact_check_articles:
            st.success("✅ Fact-Check Reports Found")
            for i, (title, link) in enumerate(fact_check_articles, 1):
                st.write(f"**{i}. {title}**")
                st.write(f"🔗 [Read more]({link})")
        else:
            st.warning("⚠️ No fact-check reports found.")

        # ✅ Fallback AI
        if not news_articles and not fact_check_articles:
            st.info(f"🤖 AI Analysis: {classify_news(query)}")
