import pandas as pd 
from datetime import datetime, timedelta
import yfinance as yf
import ta

class FetchData:
    """Fetch and process stock/crypto data, with EUR conversion and basic indicators."""

    def __init__(self):
        self.fx_ticker = "EURUSD=X"  # default for USD→EUR conversion

    def get_fx_rate(self, otherfx_ticker=None):
        """Get the latest FX rate (default: EUR/USD)."""
        ticker = otherfx_ticker if otherfx_ticker else self.fx_ticker
        data = yf.Ticker(ticker).history(period="1d")
        return data["Close"].iloc[-1] if not data.empty else None

    def convert_to_euro(self, data):
        """Convert OHLC prices from USD to EUR (Volume unchanged)."""
        rate = self.get_fx_rate()
        if rate:
            data[["Open", "High", "Low", "Close"]] *= rate
        return data

    def get_crypto_prices(self, ticker, period="1mo", interval="1d", in_euro=False):
        """Download crypto price data. Converts to EUR if requested."""
        end = datetime.now()
        if period == "1wk":
            start = end - timedelta(days=7)
            data = yf.download(ticker, start=start, end=end, interval=interval)
        else:
            data = yf.download(ticker, period=period, interval=interval)
        if data.empty:
            return data
        return self.convert_to_euro(data) if in_euro else data

    def get_stock_prices(self, ticker, period="1mo", interval="1d", in_euro=False):
        """Download stock price data. Converts to EUR if requested."""
        end = datetime.now()
        if period == "1wk":
            start = end - timedelta(days=7)
            data = yf.download(ticker, start=start, end=end, interval=interval)
        else:
            data = yf.download(ticker, period=period, interval=interval)
        if data.empty:
            return data
        return self.convert_to_euro(data) if in_euro else data

    def process_datas(self, data, convert_timezone=True):
        """Reset index, add 'Datetime' column, and optionally convert to US/Eastern."""
        if data.index.tzinfo is None:
            data.index = data.index.tz_localize("UTC")
        if convert_timezone:
            data.index = data.index.tz_convert("US/Eastern")
        data.reset_index(inplace=True)
        if "Date" in data.columns:
            data.rename(columns={"Date": "Datetime"}, inplace=True)
        return data

    def calculate_metrics(self, data):
        """Return last close, change, % change, high, low, and total volume."""
        last = data['Close'].iloc[0]
        prev = data['Close'].iloc[-1]
        change = last - prev
        pct = (change / prev) * 100
        return last, change, pct, float(data['High'].max()), float(data['Low'].min()), int(data['Volume'].sum())

    def add_technical_indicators(self, data):
        """Add SMA(20) and EMA(20) to the dataset."""
        data['SMA_20'] = ta.trend.sma_indicator(data['Close'], window=20)
        data['EMA_20'] = ta.trend.ema_indicator(data['Close'], window=20)
        return data


# --- Usage Examples ---
fetcher = FetchData()

# 1. Fetch Bitcoin prices in EUR
btc_data = fetcher.get_crypto_prices("BTC-USD", period="1mo", in_euro=True)

# 2. Fetch Apple stock prices in EUR
aapl_data = fetcher.get_stock_prices("AAPL", period="1mo", in_euro=True)

# 3. Add indicators + metrics
aapl_data = fetcher.add_technical_indicators(aapl_data)
metrics = fetcher.calculate_metrics(aapl_data)
print("AAPL Metrics:", metrics)
