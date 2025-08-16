# 📰 Fake News Detection Web App

This is a **hybrid fake news detector** built with Streamlit and Hugging Face Transformers.  
It verifies news headlines by combining **web scraping + fact-checking + AI (BERT)**.

---

## 🚀 How It Works
1. User enters a **news headline**.
2. The app searches **Google News** for matching articles.
3. It cross-checks **fact-checking sites** like Snopes & AltNews.
4. If no trusted sources are found, a **fine-tuned BERT model** predicts whether it's ✅ Real or ❌ Fake.

---

## 🛠️ Tech Stack
- **Python** + **Streamlit** (web app)
- **Hugging Face Transformers** (BERT, T5 Summarizer)
- **Torch** + **Safetensors**
- **BeautifulSoup4** + **Newspaper3k** (web scraping)
- **Google News RSS** + **Fact-checking sites (Snopes, AltNews)**

---

## 📌 Example Headlines to Test
- ✅ Real: *"Chandrayaan-3 lands on the south pole of the Moon."*  
- ❌ Fake: *"NASA confirms the Sun will rise from the west in 2030."*  
- ⚖️ Ambiguous: *"Amazon to accept Bitcoin for payments by 2026."*  

---

## 📄 License
This project is licensed under the **MIT License** – see [LICENSE](./LICENSE).

👨‍💻 Built by [Your Name]
