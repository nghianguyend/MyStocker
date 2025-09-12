import yfinance as yf
from datetime import datetime

stock = yf.Ticker("MSFT")
stock_data = stock.history(period="max")

print(stock_data)
