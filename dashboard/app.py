import plotly.graph_objects as go
import plotly.express as px
from datas import FetchData
import streamlit as st
import pandas as pd

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
    "Bitcoin (BTC)": "BTC-USD",
    "Ethereum (ETH)": "ETH-USD",
    "Cardano (ADA)": "ADA-USD",
    "Dogecoin (DOGE)": "DOGE-USD",
    "Solana (SOL)": "SOL-USD",
    "Polkadot (DOT)": "DOT-USD",
    "Litecoin (LTC)": "LTC-USD",
    "Tron (TRX)": "TRX-USD",
    "Chainlink (LINK)": "LINK-USD",
    "Polygon (MATIC)": "MATIC-USD"
}

#Get GeckoAPI coin_id
coin_id = name_to_id[crypto_choice]

# Fetcher instance
fetcher = FetchData()

# Fetch Crypto Prices 
in_eur = currency_type == "EUR"
st.subheader(f"Crypto Prices : {crypto_choice}")
crypto_data = fetcher.get_crypto_prices(coin_id, period_to_id[period], interval_mapping[period_to_id[period]], in_euro=in_eur)
last_close_crypto, change_crypto, pct_change_crypto, high_crypto, low_crypto, volume_crypto = fetcher.calculate_metrics(crypto_data)

# Display Crypto
st.metric(
    label=f"{crypto_choice} Price From {period}",
    value=f"{float(last_close_crypto):.2f} {'EUR' if in_eur else 'USD'}",
    delta=f"Changes : {float(change_crypto):.2f} ({float(pct_change_crypto):.2f} %)"
)

col1_crypto, col2_crypto, col3_crypto = st.columns(3)
col1_crypto.metric("High", f"{high_crypto:.2f} {currency_type}")
col2_crypto.metric("Low", f"{low_crypto:.2f} {currency_type}")
col3_crypto.metric("Volume", f"{volume_crypto:,}")

if isinstance(crypto_data.columns, pd.MultiIndex):
    crypto_data.columns = [col[0] for col in crypto_data.columns]

crypto_data = crypto_data.reset_index()
if 'Date' in crypto_data.columns:
    crypto_data.rename(columns={'Date': 'Datetime'}, inplace=True)

# Ensure numeric
for col in ['Open','High','Low','Close','Volume']:
    crypto_data[col] = pd.to_numeric(crypto_data[col], errors='coerce')

# Plot
max_points = 50
plot_data = crypto_data.tail(max_points)
fig = go.Figure()
if chart_type == "Candlestick":
    fig.add_trace(go.Candlestick(
        x=plot_data['Datetime'],
        open=plot_data['Open'],
        high=plot_data['High'],
        low=plot_data['Low'],
        close=plot_data['Close'],
        name="Price"
    ))
else:  # Line chart
    fig.add_trace(go.Scatter(
        x=plot_data['Datetime'],
        y=plot_data['Close'],
        mode='lines',
        name="Close Price"
    ))
fig.update_layout(title=f'{crypto_choice} {period.upper()} Chart',
                  xaxis_title='Time',
                  yaxis_title='Price ({})'.format('EUR' if in_eur else 'USD'),
                  height=600)
st.plotly_chart(fig, use_container_width=True)

# Fetch Stock Prices
st.subheader(f"Stock Prices : {symbol}")
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
col1.metric("High", f"{high:.2f} {currency_type}")
col2.metric("Low", f"{low:.2f} {currency_type}")
col3.metric("Volume", f"{volume:,}")

if isinstance(stock_data.columns, pd.MultiIndex):
    stock_data.columns = [col[0] for col in stock_data.columns]

stock_data = stock_data.reset_index()
if 'Date' in stock_data.columns:
    stock_data.rename(columns={'Date': 'Datetime'}, inplace=True)

# Ensure numeric
for col in ['Open','High','Low','Close','Volume']:
    stock_data[col] = pd.to_numeric(stock_data[col], errors='coerce')

# Plot
max_points = 70
plot_data = stock_data.tail(max_points)
fig = go.Figure()
if chart_type == "Candlestick":
    fig.add_trace(go.Candlestick(
        x=plot_data['Datetime'],
        open=plot_data['Open'],
        high=plot_data['High'],
        low=plot_data['Low'],
        close=plot_data['Close'],
        name="Price"
    ))
else:  # Line chart
    fig.add_trace(go.Scatter(
        x=plot_data['Datetime'],
        y=plot_data['Close'],
        mode='lines',
        name="Close Price"
    ))
fig.update_layout(title=f'{symbol} {period.upper()} Chart',
                  xaxis_title='Time',
                  yaxis_title='Price ({})'.format('EUR' if in_eur else 'USD'),
                  height=600)
st.plotly_chart(fig, use_container_width=True)
    
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

def main():
    fetcher = FetchData()
    # --- Test Crypto Prices ---
    print("Fetching crypto prices...")
    crypto_df = fetcher.get_crypto_prices(coin_id, period_to_id[period], interval_mapping[period_to_id[period]], in_euro=in_eur)
    if crypto_df is not None:
        print(crypto_df.head(), "\n")

    # --- Test Stock Prices ---
    print("Fetching stock prices for AAPL (Apple)...")
    stock_df = fetcher.get_stock_prices("AAPL", period="5d", interval="1d", in_euro=True)
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


