import streamlit as st
import requests
import yfinance as yf
from datetime import date
import pandas as pd
import matplotlib.pyplot as plt


START = "2020-06-06"
TODAY = str(date.today())

st.title("Halal Stockbot")

st.markdown("""
**Halal stocks are shares of companies that comply with Islamic (Shariah) law. They avoid businesses involving interest (riba), alcohol, gambling, pork, and other prohibited activities.  
This app helps you forecast prices and show related news for stocks generally considered Shariah-compliant.**
""")

# Halal stock tickers - you can expand this list
stocks = ("AAPL", "MSFT", "NVDA", "TSLA", "COST", "INTC", "PFE", "AZN", "RMV")
selected_stock = st.selectbox("Select a halal stock for analysis:", stocks)

# Load data caching for performance
@st.cache_data
def load_stock_data(ticker):
    df = yf.download(ticker, START, TODAY)
    df.reset_index(inplace=True)
    df['Date'] = pd.to_datetime(df['Date']).dt.date  # convert datetime to date only
    return df.sort_values('Date')

data_load_state = st.text("Loading stock data...")
stock_data = load_stock_data(selected_stock)
data_load_state.text("Done!")

st.subheader("This Month's Stock Data")
st.write(stock_data.tail(30))

st.subheader(f"Stock prices for {selected_stock}")

#Stock price fluctuations over last decade

def plot_with_matplotlib(data):
    plt.figure(figsize=(10,5))
    plt.plot(data['Date'], data['Open'], label='Open Price')
    plt.plot(data['Date'], data['Close'], label='Close Price')
    plt.title("Stock Prices")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    st.pyplot(plt)

plot_with_matplotlib(stock_data)

# News API config
NEWS_API_KEY = "250036ce678d4b1e8c90e9d9e232fda1"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

def get_financial_news(query, page_size=5):
    params = {
        "q": query,
        "sortBy": "publishedAt",
        "language": "en",
        "pageSize": page_size,
        "apiKey": NEWS_API_KEY,
    }
    response = requests.get(NEWS_ENDPOINT, params=params)
    if response.status_code == 200:
        return response.json().get("articles", [])
    else:
        st.error(f"Error fetching news: {response.status_code}")
        return []

st.subheader(f"Latest News Related to {selected_stock}")

news_articles = get_financial_news(selected_stock)

if news_articles:
    for article in news_articles:
        st.markdown(f"### [{article['title']}]({article['url']})")
        st.write(f"*Source:* {article['source']['name']}  |  *Published:* {article['publishedAt'][:10]}")
        st.write(article['description'] or "No description available.")
        st.write("---")
else:
    st.write("No news found for this stock.")


