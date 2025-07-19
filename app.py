import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime
from PIL import Image
from textblob import TextBlob
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.platypus import Image as RLImage
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
guardian_key = os.getenv("GUARDIAN_API_KEY")
newsdata_key = os.getenv("NEWSDATA_API_KEY")

st.set_page_config(page_title="Live News Sentiment Dashboard", layout="wide")

# Stylish background
page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] {{
    background-image: url("https://images.unsplash.com/photo-1522202176988-66273c2fd55f");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}}
[data-testid="stHeader"] {{
    background: rgba(255, 255, 255, 0.0);
}}
[data-testid="stSidebar"] {{
    background-color: rgba(255, 255, 255, 0.75);
}}
.block-container {{
    background-color: rgba(255, 255, 255, 0.88);
    border-radius: 12px;
    padding: 2rem;
}}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

st.title("📰 Live News Headlines Sentiment Dashboard")
st.markdown("#### Get real-time headlines and analyze sentiment of trending news stories!")

# Sidebar UI
st.sidebar.header("🟢 News Options")
country = st.sidebar.selectbox("🌐 Select Country", ["USA", "India"])
category = st.sidebar.selectbox("📂 Choose News Category", [
    "general", "politics", "business", "technology", "entertainment", "sports", "science", "health"
])
if st.sidebar.button("🔄 Refresh News Now"):
    st.rerun()

# Session cache to hold last headlines
if "cached_news" not in st.session_state:
    st.session_state.cached_news = {}

def fetch_news(country, category):
    try:
        if country == "India":
            url = f"https://content.guardianapis.com/search?q={category}&api-key={guardian_key}"
            response = requests.get(url)
            articles = response.json().get("response", {}).get("results", [])
            if not articles:
                return None
            news = [
                {
                    "title": article["webTitle"],
                    "source": "The Guardian",
                    "publishedAt": article["webPublicationDate"]
                }
                for article in articles
            ]
        else:
            url = f"https://newsdata.io/api/1/news?country=us&category={category}&language=en&apikey={newsdata_key}"
            response = requests.get(url)
            articles = response.json().get("results", [])
            if not articles:
                return None
            news = [
                {
                    "title": article["title"],
                    "source": article.get("source_id", "NewsData.io"),
                    "publishedAt": article["pubDate"]
                }
                for article in articles
            ]
        return news
    except Exception as e:
        st.error(f"API call failed: {e}")
        return None

def analyze_sentiment(news):
    for article in news:
        blob = TextBlob(article["title"])
        article["sentiment"] = round(blob.sentiment.polarity, 3)
    return news

def generate_pdf(df, filename="news_report.pdf"):
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("<b>News Sentiment Report</b>", styles["Title"]))
    story.append(Spacer(1, 12))

    for _, row in df.iterrows():
        story.append(Paragraph(f"<b>Title:</b> {row['title']}", styles["Normal"]))
        story.append(Paragraph(f"<b>Source:</b> {row['source']} | <b>Date:</b> {row['publishedAt']} | <b>Sentiment:</b> {row['sentiment']}", styles["Normal"]))
        story.append(Spacer(1, 12))

    doc.build(story)
    return filename

# Load news or fallback
cache_key = f"{country}_{category}"
latest_news = fetch_news(country, category)

if latest_news:
    news_data = analyze_sentiment(latest_news)
    st.session_state.cached_news[cache_key] = news_data
else:
    if cache_key in st.session_state.cached_news:
        news_data = st.session_state.cached_news[cache_key]
        st.info("📘 API limit reached or no new updates. Showing previous headlines.")
    else:
        st.error("❌ Could not fetch news and no previous headlines available.")
        st.stop()

df = pd.DataFrame(news_data)
df.sort_values("publishedAt", ascending=False, inplace=True)

selected_sources = st.sidebar.multiselect("🧾 Filter by Source", options=df["source"].unique(), default=list(df["source"].unique()))
df = df[df["source"].isin(selected_sources)]

st.subheader("📰 Latest Headlines")
for _, row in df.iterrows():
    with st.expander(row["title"]):
        st.markdown(f"**📰 Source:** {row['source']}")
        st.markdown(f"**📅 Published At:** {row['publishedAt']}")
        st.markdown(f"**💬 Sentiment Score:** `{row['sentiment']}`")

st.subheader("📊 Sentiment Distribution")
sentiment_labels = df["sentiment"].apply(lambda x: "Positive" if x > 0 else ("Negative" if x < 0 else "Neutral"))
sentiment_counts = sentiment_labels.value_counts().reset_index()
sentiment_counts.columns = ["Sentiment", "Count"]

fig = px.pie(sentiment_counts, values="Count", names="Sentiment", title="Headline Sentiment Breakdown",
             color_discrete_map={"Positive": "green", "Neutral": "gray", "Negative": "red"})
st.plotly_chart(fig, use_container_width=True)

# PDF Download (Chart not embedded)
if st.button("📥 Download PDF Report"):
    report_file = f"{country}_{category}_news_report.pdf"
    pdf_path = generate_pdf(df, filename=report_file)
    with open(pdf_path, "rb") as f:
        st.download_button("⬇️ Download News PDF", f, file_name=report_file, mime="application/pdf")
