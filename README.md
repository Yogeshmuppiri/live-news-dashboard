# 📰 Live News Sentiment Dashboard

A real-time news sentiment analysis web application built with **Streamlit**, leveraging **GNews** and **New York Times** APIs to fetch headlines and visualize public sentiment with NLP techniques.

![App Screenshot](https://images.unsplash.com/photo-1522202176988-66273c2fd55f)

---

## 🚀 Features

- 🌍 Country selection: **USA** or **India**
- 🗂️ Category-based news: business, technology, sports, health, etc.
- 📊 Real-time sentiment analysis with **TextBlob**
- 📈 Interactive sentiment charts using **Plotly**
- 🧠 Cached fallback: shows previously fetched news if API limit is exceeded
- 📄 **PDF Report Export**: News + Sentiment + Chart in one downloadable report
- 💻 Stylish UI with full-width responsive layout and background image

---

## ⚙️ Tech Stack

- **Frontend & Backend**: Streamlit
- **APIs**:  
  - [New York Times Top Stories API](https://developer.nytimes.com/docs/top-stories-product/1/overview) (USA)  
  - [GNews API](https://gnews.io/) (India)
- **NLP**: TextBlob
- **Visualization**: Plotly & Matplotlib
- **PDF Reporting**: ReportLab
- **Environment**: Python 3.9+

---
🔄 ETL Process (Extract → Transform → Load)
This application implements a lightweight yet effective ETL (Extract, Transform, Load) pipeline to process live news data in real time:

✅ Extract
Fetches live news headlines from:

GNews API (for India)

New York Times Top Stories API (for USA)

Extracted fields:

title

source

publishedAt

description (for NYT)

🔁 Transform
Cleans and filters raw news data to ensure format consistency.
Applies sentiment analysis using TextBlob:
Calculates polarity score for each title.
Classifies each headline as Positive, Negative, or Neutral.
Prepares a structured Pandas DataFrame for visualization and export.

📥 Load
Loads the transformed data into:
An interactive Streamlit interface for real-time display.
Pie chart using Plotly to visualize sentiment distribution.
PDF report using ReportLab containing:
News headlines with sentiment labels
Timestamped metadata
Embedded sentiment chart

This ETL process makes the application ideal for lightweight real-time data pipelines, media monitoring, or dashboard reporting use cases with minimal setup.

## 🔐 Environment Variables

Create a `.env` file in your project root:

```env
GNEWS_API_KEY=your_gnews_key_here
NYT_API_KEY=your_nyt_key_here
