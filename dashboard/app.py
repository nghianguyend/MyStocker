import yfinance as yf
from datetime import datetime
import pandas as pd;
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datas import FetchData

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


