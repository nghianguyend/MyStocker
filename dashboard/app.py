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

if __name__ == "__main__":
    main()




# def make_graph(stock_data, revenue_data, stock):
#     fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
#     stock_data_specific = stock_data[stock_data.Date <= '2021-06-14']
#     revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']
#     fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific.Date, infer_datetime_format=True), y=stock_data_specific.Close.astype("float"), name="Share Price"), row=1, col=1)
#     fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific.Date, infer_datetime_format=True), y=revenue_data_specific.Revenue.astype("float"), name="Revenue"), row=2, col=1)
#     fig.update_xaxes(title_text="Date", row=1, col=1)
#     fig.update_xaxes(title_text="Date", row=2, col=1)
#     fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
#     fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
#     fig.update_layout(showlegend=False,
#     height=900,
#     title=stock,
#     xaxis_rangeslider_visible=True)
#     fig.show()
#     from IPython.display import display, HTML
#     fig_html = fig.to_html()
#     display(HTML(fig_html))