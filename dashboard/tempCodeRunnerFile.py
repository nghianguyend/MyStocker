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
st.subheader(f"Crypto Prices: {coin_id}")
crypto_df = fetcher.get_cryto_prices(coin_id)
if crypto_df is not None:
    st.dataframe(crypto_df.tail(5))  

# Fetch Stock Prices
st.subheader(f"Stock Prices: {symbol}")
in_eur = currency_type == "EUR"
stock_data = fetcher.get_stock_prices(symbol, period_to_id[period], interval_mapping[period_to_id[period]], in_euro=in_eur)
stock_data = fetcher.process_datas(stock_data, convert_timezone=True)
last_close, change, pct_change, high, low, volume = fetcher.calculate_metrics(stock_data)

# Display
st.metric(
    label=f"{symbol} Price From {period}",
    value=f"{float(last_close):.2f} {'EUR' if in_eur else 'USD'}",
    delta=f"Changes : {float(change):.2f} ({float(pct_change):.2f} %)"
)


col1, col2, col3 = st.columns(3)