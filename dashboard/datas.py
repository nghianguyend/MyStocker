import requests
import pandas as pd 
from datetime import datetime, timedelta
import yfinance as yf
import pytz
import ta
class FetchData :
    
    def get_crypto_prices(self, ticker, period="1mo", interval="1d", in_euro=False) :
        end_date = datetime.now()
        if period == "1wk":
            start_date = end_date - timedelta(days=7)
            stock_info = yf.download(ticker, start=start_date, end=end_date, interval=interval)
        else:
            stock_info = yf.download(ticker, period=period, interval=interval)
        if stock_info.empty:
            return stock_info
        if in_euro:
            fx = yf.Ticker("EURUSD=X")
            conversion_rate = fx.history(period="1d")["Close"].iloc[-1]
            for col in ["Open", "High", "Low", "Close"] :
                stock_info[col] *= conversion_rate
        return stock_info
        
    def get_stock_prices(self, ticker, period="1mo", interval="1d", in_euro=False):
        end_date = datetime.now()
        if period == "1wk":
            start_date = end_date - timedelta(days=7)
            stock_info = yf.download(ticker, start=start_date, end=end_date, interval=interval)
        else:
            stock_info = yf.download(ticker, period=period, interval=interval)
        if stock_info.empty:
            return stock_info
        if in_euro:
            fx = yf.Ticker("EURUSD=X")
            conversion_rate = fx.history(period="1d")["Close"].iloc[-1]
            for col in ["Open", "High", "Low", "Close"] :
                stock_info[col] *= conversion_rate
        return stock_info

    
    def process_datas(self, data, convert_timezone=True) :
        if data.index.tzinfo == None :
            data.index = data.index.tz_localize("UTC")
        if convert_timezone :
            data.index = data.index.tz_convert("US/Eastern")
        data.reset_index(inplace=True)
        if "Date" in data.columns:
            data.rename(columns={"Date": "Datetime"}, inplace=True)
        return data
    
    def calculate_metrics(self, data) :
        last_close = data['Close'].iloc[0]
        prev_close = data['Close'].iloc[-1]
        change = last_close - prev_close
        pct_change = (change / prev_close) * 100
        high = float(data['High'].max())
        low = float(data['Low'].min())
        volume = int(data['Volume'].sum())
        return last_close, change, pct_change, high, low, volume
    
    def add_technical_indicators(self, data):
        data['SMA_20'] = ta.trend.sma_indicator(data['Close'], window=20)
        data['EMA_20'] = ta.trend.ema_indicator(data['Close'], window=20)
        return data