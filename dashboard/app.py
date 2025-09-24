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
chart_type = st.sidebar.selectbox("Chart Type", ["Candlestick", "Line"])
period_to_id = {
    "1 Day" : "1m", 
    "1 Week" : "30m", 
    "1 Month" : "1d", 
    "1 Year" : "1wk", 
    "Max" : "1wk"
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
st.subheader(f"Crypto Prices: {coin_id}")
crypto_df = fetcher.get_cryto_prices(coin_id)
if crypto_df is not None:
    st.dataframe(crypto_df.tail(5))  

# Fetch Stock Prices
st.subheader(f"Stock Prices: {symbol}")
stock_df = fetcher.get_stock_prices(symbol, period="5d", interval="1d")
stock_df = fetcher.process_datas(stock_df)
metrics = fetcher.calculate_metrics(stock_df)

# Show metrics
# st.metric(label="Last Close", value=f"${metrics[0]:.2f}")
# st.metric(label="Change", value=f"${metrics[1]:.2f}")
# st.metric(label="% Change", value=f"{metrics[2]:.2f}%")
# st.metric(label="High", value=f"${metrics[3]:.2f}")
# st.metric(label="Low", value=f"${metrics[4]:.2f}")

# Make Stock Chart 
fig = make_subplots(rows=1, cols=1)
fig.add_trace(go.Candlestick(
    x=stock_df['Date'],
    open=stock_df['Open'],
    high=stock_df['High'],
    low=stock_df['Low'],
    close=stock_df['Close'],
    name=symbol
))
st.plotly_chart(fig, use_container_width=True)

def main():
    fetcher = FetchData()
    # --- Test Crypto Prices ---
    print("Fetching crypto prices...")
    crypto_df = fetcher.get_cryto_prices()
    if crypto_df is not None:
        print(crypto_df.head(), "\n")

    # --- Test Stock Prices ---
    print("Fetching stock prices for AAPL (Apple)...")
    stock_df = fetcher.get_stock_prices("AAPL", period="5d", interval="1d")
    print("Before reset_index():")
    print(stock_df.head(), "\n")   # Date is in the index

    # Process the data (with reset_index)
    stock_df = fetcher.process_datas(stock_df)
    print("After process_datas (reset_index applied):")
    print(stock_df.head())         # Datetime is now a column
    
    stock_datas = fetcher.calculate_metrics(stock_df)
    print(stock_datas)

if __name__ == "__main__":
    main()


