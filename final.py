# ====================================
# final.py — GenAI Backend for FactCheckAI
# ====================================

import requests
import difflib
from bs4 import BeautifulSoup
from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()
os.getenv("GOOGLE_API_KEY")
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

# --------------------------
# 📰 Fetch News Articles
# --------------------------
def get_news_articles(query):
    search_url = f"https://news.google.com/rss/search?q={query.replace(' ', '+')}+when:90d"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(search_url, headers=headers)

    if response.status_code != 200:
        return []

    soup = BeautifulSoup(response.content, "lxml-xml")
    items = soup.find_all("item")

    news_links = []
    for item in items[:5]:  # Top 5 results
        title = item.title.text
        link = item.link.text
        similarity = difflib.SequenceMatcher(None, query.lower(), title.lower()).ratio()
        if similarity >= 0.5:
            news_links.append((title, link))

    return news_links

# --------------------------
# 🕵️ Fetch Fact-Checking Articles
# --------------------------
def get_fact_check_articles(query):
    fact_check_sites = [
        f"https://www.snopes.com/?s={query.replace(' ', '+')}",
        f"https://www.altnews.in/?s={query.replace(' ', '+')}"
    ]

    fact_results = []
    for site in fact_check_sites:
        response = requests.get(site, headers={"User-Agent": "Mozilla/5.0"})
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            articles = soup.find_all("h2", limit=3)
            for article in articles:
                a_tag = article.find("a")
                if a_tag and "href" in a_tag.attrs:
                    fact_results.append((article.text.strip(), a_tag["href"]))
    return fact_results

# --------------------------
# 🤖 Gemini-based Fake News Reasoning
# --------------------------
def classify_news_with_gemini(text, news_articles=None, fact_articles=None):
    """Use Gemini via LangChain to reason about the authenticity of the headline."""
    news_summary = ""
    if news_articles:
        news_summary = "\n".join([f"- {title}: {link}" for title, link in news_articles])
    if fact_articles:
        fact_summary = "\n".join([f"- {title}: {link}" for title, link in fact_articles])
    else:
        fact_summary = "No direct fact-check reports found."

    prompt = PromptTemplate.from_template("""
    You are an expert fact-checking AI.
    Analyze the following headline and related evidence to determine if it's likely REAL or FAKE.
    Be concise and evidence-based.

    Headline: "{headline}"

    Related News Articles:
    {news_summary}

    Fact-Checking Sources:
    {fact_summary}

    Respond strictly in this format:
    Verdict: (Real/Fake)
    Reason: <brief reason>
    """)

    chain_input = prompt.format(
        headline=text,
        news_summary=news_summary or "No related news found.",
        fact_summary=fact_summary
    )

    response = llm.invoke(chain_input)
    return response.content
