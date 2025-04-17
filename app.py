import streamlit as st
from transformers import BertTokenizer, BertForSequenceClassification, TextClassificationPipeline
import pandas as pd
import matplotlib.pyplot as plt
import feedparser
import os
import sqlite3
from datetime import datetime

# Set Streamlit config
st.set_page_config(page_title="Crypto News Sentiment Analyzer", page_icon="💹", layout="centered")

# Load FinBERT
@st.cache_resource
def load_model():
    MODEL_NAME = "yiyanghkust/finbert-tone"
    tokenizer = BertTokenizer.from_pretrained(MODEL_NAME)
    model = BertForSequenceClassification.from_pretrained(MODEL_NAME)
    classifier = TextClassificationPipeline(model=model, tokenizer=tokenizer, return_all_scores=True)
    return classifier

classifier = load_model()

# Emoji map
sentiment_emoji = {"positive": "🟢", "neutral": "🟡", "negative": "🔴"}

# App Title
st.title("💹 Crypto News Sentiment Analyzer")
st.markdown("Analyze crypto headlines using **FinBERT**, visualize trends, upload CSVs, and save sentiment history.")

# Upload CSV
uploaded_file = st.file_uploader("📤 Upload a CSV file (must include a 'headline' column):", type="csv")

# Manual Input
st.subheader("📝 Or Enter Headlines Manually")
manual_input = st.text_area("Enter multiple headlines (one per line)...", height=150)

# Merge headlines from upload/manual
headlines = []

if uploaded_file:
    try:
        df_uploaded = pd.read_csv(uploaded_file)
        if "headline" in df_uploaded.columns:
            headlines.extend(df_uploaded["headline"].dropna().tolist())
        else:
            st.error("CSV must contain a 'headline' column.")
    except Exception as e:
        st.error(f"Failed to read CSV: {e}")

if manual_input:
    lines = [line.strip() for line in manual_input.split("\n") if line.strip()]
    headlines.extend(lines)

# Analyze Button
if st.button("🔍 Analyze Headlines"):
    if not headlines:
        st.warning("No headlines provided.")
    else:
        results = []
        for hl in headlines:
            prediction = classifier(hl)[0]
            top = sorted(prediction, key=lambda x: x['score'], reverse=True)[0]
            results.append({
                "Date": datetime.now().strftime("%Y-%m-%d"),
                "Headline": hl,
                "Sentiment": top["label"].capitalize(),
                "Confidence": top["score"]
            })

        df_results = pd.DataFrame(results)
        st.subheader("📄 Sentiment Results")
        st.dataframe(df_results)

        # Save results
        if not os.path.exists("logs"):
            os.makedirs("logs")
        csv_path = f"logs/sentiment_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        df_results.to_csv(csv_path, index=False)

        # Save to SQLite DB
        conn = sqlite3.connect("logs/sentiment_log.db")
        df_results.to_sql("sentiment_data", conn, if_exists="append", index=False)
        conn.close()

        st.success(f"Results saved to CSV and local database.")

        # Bar chart
        st.subheader("📊 Sentiment Distribution")
        fig, ax = plt.subplots()
        df_results["Sentiment"].value_counts().plot(kind="bar", color=["green", "yellow", "red"], ax=ax)
        ax.set_ylabel("Number of Headlines")
        st.pyplot(fig)

        # Confidence trend
        st.subheader("📈 Confidence Trend")
        st.line_chart(df_results.set_index("Headline")["Confidence"])

# Show historical data
st.subheader("📜 Historical Sentiment Log")
if os.path.exists("logs/sentiment_log.db"):
    conn = sqlite3.connect("logs/sentiment_log.db")
    df_history = pd.read_sql_query("SELECT * FROM sentiment_data", conn)
    st.dataframe(df_history.sort_values("Date", ascending=False).head(50))
    conn.close()

    # Chart of sentiment trends over time
    st.subheader("📆 Sentiment Over Time")
    daily_sentiment = df_history.groupby(["Date", "Sentiment"]).size().unstack().fillna(0)
    st.line_chart(daily_sentiment)

# Live News Feed
st.subheader("📰 Live Crypto News Feed (from CryptoPanic)")
feed = feedparser.parse("https://cryptopanic.com/news/rss/")
if feed.entries:
    for entry in feed.entries[:5]:
        st.markdown(f"- [{entry.title}]({entry.link})")
else:
    st.write("Unable to load live news.")

# Footer
st.markdown('<div class="footer">© 2025 Hafiz Moiz Ali. All rights reserved.</div>', unsafe_allow_html=True)
