import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datas import FetchData
import streamlit as st

st.set_page_config(layout="wide")
st.title("📈 Real Time Stock and Crypto Dashboard")

# Sidebar
st.sidebar.header("Dashboard Controls")
symbol = st.sidebar.text_input("Stock Symbol", value="AAPL")
crypto_choice = st.sidebar.selectbox(
    "Crypto", 
    ["Bitcoin (BTC)", 
    "Ethereum (ETH)", 
    "Cardano (ADA)", 
    "Dogecoin (DOGE)", 
    "Solana (SOL)", 
    "Polkadot (DOT)", 
    "Litecoin (LTC)", 
    "Tron (TRX)", 
    "Chainlink (LINK)", 
    "Polygon (MATIC)"]
)
period = st.sidebar.selectbox("Time Period", ["1 Day", "1 Week", "1 Month", "1 Year", "Max"])
currency_type = st.sidebar.selectbox("Currency", ["USD", "EUR"])
chart_type = st.sidebar.selectbox("Chart Type", ["Candlestick", "Line"])
indicators = st.sidebar.multiselect("Technical Indicators", ["SMA 20", "EMA 20"])
period_to_id = {
    "1 Day" : "1d", 
    "1 Week" : "1wk", 
    "1 Month" : "1mo", 
    "1 Year" : "1y", 
    "Max" : "max"
}
interval_mapping = {
    "1d" : "1m",
    "1wk" : "30m",
    "1mo" : "1d",
    "1y" : "1wk",
    "max" : "1wk",
}
name_to_id = {
    "Bitcoin (BTC)": "bitcoin",
    "Ethereum (ETH)": "ethereum",
    "Cardano (ADA)": "cardano",
    "Dogecoin (DOGE)": "dogecoin",
    "Solana (SOL)": "solana",
    "Polkadot (DOT)": "polkadot",
    "Litecoin (LTC)": "litecoin",
    "Tron (TRX)": "tron",
    "Chainlink (LINK)": "chainlink",
    "Polygon (MATIC)": "polygon"
}

#Get GeckoAPI coin_id
coin_id = name_to_id[crypto_choice]

# Fetcher instance
fetcher = FetchData()

# Fetch Crypto Prices 
st.subheader(f"Crypto Prices : {crypto_choice}")
crypto_data = fetcher.get_cryto_prices(coin_id)
crypto_price, crypto_change = fetcher.get_crypto_metrics(crypto_data, currency=currency_type)
crypto_change_pct=crypto_change*100
# Display Crypto
st.metric(
    label=f"Current {crypto_choice} Price",
    value=f"{float(crypto_price):.2f} {currency_type}",
    delta=f"Changes : {float(crypto_change):.2f} ({float(crypto_change_pct):.2f} %)"
)
# Fetch Stock Prices
st.subheader(f"Stock Prices : {symbol}")
in_eur = currency_type == "EUR"
stock_data = fetcher.get_stock_prices(symbol, period_to_id[period], interval_mapping[period_to_id[period]], in_euro=in_eur)
stock_data = fetcher.process_datas(stock_data, convert_timezone=True)
last_close, change, pct_change, high, low, volume = fetcher.calculate_metrics(stock_data)

# Display Stocks
st.metric(
    label=f"{symbol} Price From {period}",
    value=f"{float(last_close):.2f} {'EUR' if in_eur else 'USD'}",
    delta=f"Changes : {float(change):.2f} ({float(pct_change):.2f} %)"
)


col1, col2, col3 = st.columns(3)
col1.metric("High", f"{high:.2f} USD")
col2.metric("Low", f"{low:.2f} USD")
col3.metric("Volume", f"{volume:,}")
    
# Show metrics
# st.metric(label="Last Close", value=f"${metrics[0]:.2f}")
# st.metric(label="Change", value=f"${metrics[1]:.2f}")
# st.metric(label="% Change", value=f"{metrics[2]:.2f}%")
# st.metric(label="High", value=f"${metrics[3]:.2f}")
# st.metric(label="Low", value=f"${metrics[4]:.2f}")

# Make Stock Chart 
# fig = make_subplots(rows=1, cols=1)
# fig.add_trace(go.Candlestick(
#     x=stock_df['Date'],
#     open=stock_df['Open'],
#     high=stock_df['High'],
#     low=stock_df['Low'],
#     close=stock_df['Close'],
#     name=symbol
# ))
# st.plotly_chart(fig, use_container_width=True)

# def main():
#     fetcher = FetchData()
#     # --- Test Crypto Prices ---
#     print("Fetching crypto prices...")
#     crypto_df = fetcher.get_cryto_prices()
#     if crypto_df is not None:
#         print(crypto_df.head(), "\n")

#     # --- Test Stock Prices ---
#     print("Fetching stock prices for AAPL (Apple)...")
#     stock_df = fetcher.get_stock_prices("AAPL", period="5d", interval="1d")
#     print("Before reset_index():")
#     print(stock_df.head(), "\n")   # Date is in the index

#     # Process the data (with reset_index)
#     stock_df = fetcher.process_datas(stock_df)
#     print("After process_datas (reset_index applied):")
#     print(stock_df.head())         # Datetime is now a column
    
#     stock_datas = fetcher.calculate_metrics(stock_df)
#     print(stock_datas)

# if __name__ == "__main__":
#     main()


