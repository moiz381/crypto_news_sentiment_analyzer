# crypto_news_sentiment_analyzer
📰 Crypto News Sentiment Analyzer
A real-time sentiment analysis web app for cryptocurrency-related financial news headlines. Powered by FinBERT, this tool helps traders, investors, and analysts assess market sentiment (Positive, Negative, or Neutral) based on the latest news.

🚀 Features
🔍 Analyze multiple crypto news headlines at once

📁 Upload CSV files containing bulk headlines

📊 Visualize sentiment distribution with bar and line charts

🕒 View historical sentiment trends over time

📦 Log analysis results to both CSV and SQLite

📰 Fetch and display live news from RSS feeds (e.g., CryptoPanic)

☁️ Easily deployable on Streamlit Cloud

🧠 Model Used
yiyanghkust/finbert-tone - A transformer-based BERT model trained on financial text for tone classification.

Sentiment labels: Positive, Neutral, Negative

🧰 Tech Stack
Python 3.10

Streamlit

HuggingFace Transformers

Pandas, Matplotlib, Seaborn

SQLite

RSS Feed Parsing

📂 Project Structure
Crypto_News_Sentiment_Analyzer/
├── app.py                  # Streamlit app
├── sentiment_analyzer.py   # FinBERT analysis logic
├── utils.py                # Helper functions for preprocessing, plotting, and storage
├── sample_news.csv         # Sample news headlines
├── requirements.txt        # Python dependencies
├── database.db             # SQLite database (auto-created)
└── README.md               # Project overview

🛠️ Setup Instructions
Clone the Repository
git clone https://github.com/moiz381/crypto_news_sentiment_analyzer.git
cd crypto-news-sentiment-analyzer

Install Requirements
pip install -r requirements.txt

Run the App
streamlit run app.py

🌐 Streamlit Cloud Deployment
Push your code to a GitHub repository.
Go to Streamlit Cloud and link your GitHub repo.
Click Deploy – that’s it!

📈 Future Improvements
Fine-tune FinBERT on crypto-specific datasets

Integrate with real-time financial news APIs

Improve handling of short or ambiguous headlines

Add multilingual support

⚠️ Known Issues
Live news feed may fail if the RSS source (e.g., CryptoPanic) is unavailable

Large CSV files may slow down analysis performance
