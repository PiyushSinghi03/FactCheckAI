import requests
import difflib
import torch
import pickle
from bs4 import BeautifulSoup
from transformers import BertTokenizer, BertForSequenceClassification, pipeline
from safetensors.torch import load_file

# Load tokenizer & model
tokenizer_path = "bert_fake_news_model"
tokenizer = BertTokenizer.from_pretrained(tokenizer_path)

model_path = "bert_fake_news_model/model.safetensors"
try:
    model = BertForSequenceClassification.from_pretrained(tokenizer_path)
    model.load_state_dict(load_file(model_path))
    model.eval()
except Exception as e:
    print(f"⚠️ Error loading NLP model: {e}")
    model = None

# NLP Summarizer
summarizer = pipeline("summarization", model="t5-small")

# Function to scrape Google News RSS
def get_news_articles(query):
    search_url = f"https://news.google.com/rss/search?q={query.replace(' ', '+')}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(search_url, headers=headers)

    if response.status_code != 200:
        print("\n❌ Failed to fetch news.")
        return []

    soup = BeautifulSoup(response.content, "lxml-xml")
    items = soup.find_all("item")

    news_links = []
    for item in items[:5]:  # Top 5 results
        title = item.title.text
        link = item.link.text
        summary = summarize_news(title)
        
        similarity = difflib.SequenceMatcher(None, query.lower(), title.lower()).ratio()
        if similarity >= 0.5:   # adjust threshold (0.5–0.7 works well)
            news_links.append((title, link, summary))

    return news_links

# Function to summarize news headlines
def summarize_news(text):
    return summarizer(text, max_length=50, min_length=10, do_sample=False)[0]['summary_text']

# Function to check fact-checking websites
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
                if a_tag and "href" in a_tag.attrs:   # ✅ safe check
                    fact_results.append((article.text.strip(), a_tag["href"]))
    return fact_results
# Function to classify fake news using BERT
def classify_news(text):
    if model is None:
        return "⚠️ Model is not loaded. Cannot analyze."

    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)

    prediction = torch.argmax(outputs.logits, dim=1).item()
    return "likely to be a ✅ Real News" if prediction == 1 else "likely to be a ❌ Fake News "

# Main Execution
if __name__ == "__main__":
    query = input("📰 Enter the news headline to verify: ")

    # Step 1: Check Google News
    news_articles = get_news_articles(query)
    if news_articles:
        print("\n✅ Trusted Sources Found! This news is likely to be verified.\n")
        for i, (title, link, summary) in enumerate(news_articles, 1):
            print(f"{i}. {title}\n   🔗 {link}\n   📌 Summary: {summary}\n")
    else:
        print("\n⚠️ No relevant articles found on Google News.")

    # Step 2: Check Fact-Checking Websites
    fact_check_articles = get_fact_check_articles(query)
    if fact_check_articles:
        print("\n✅ Fact-Check Reports Found:\n")
        for i, (title, link) in enumerate(fact_check_articles, 1):
            print(f"{i}. {title}\n   🔗 {link}\n")
    else:
        print("\n⚠️ No fake reports found.")

    # Step 3: If No Trusted Sources, Use NLP Fake News Detection
    if not news_articles and not fact_check_articles:
        print("\n⚠️ No trusted sources found! Running NLP analysis...\n")
        print(f"🤖 AI Analysis: {classify_news(query)}")
