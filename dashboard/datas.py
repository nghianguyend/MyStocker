import requests
import pandas as pd 
from datetime import datetime, timedelta
import yfinance as yf
import pytz
import ta
class FetchData :
    def __init__(self) :
        self.crypto_url = "https://api.coingecko.com/api/v3/simple/price" 
        
    def get_cryto_prices(self, coins="bitcoin,ethereum,cardano,dogecoin,solana,polkadot,litecoin,tron,chainlink,polygon") :
        try :
            params = {
                'ids': coins,
                'vs_currencies': 'usd,eur',
                'include_24hr_change': 'true'
            }
            resp = requests.get(self.crypto_url, params=params, timeout=10)
            resp.raise_for_status()
            if resp.status_code == 200 :
                datas = resp.json()
                # return data.items()
                coin_list = []
                
                for name, coin_info in datas.items() :
                    coin_list.append({
                        'coin' : name.title(),
                        'usd_price' : coin_info['usd'], 
                        'usd_exchange' : coin_info['usd_24h_change'],
                        'eur_price' : coin_info['eur'],
                        'eur_exchange' : coin_info['eur_24h_change'],
                        'time' : datetime.now()
                    })
                return pd.DataFrame(coin_list)       
        except requests.exceptions.HTTPError as error:
            print("HTTP error:", error)
        except requests.exceptions.RequestException as error:
            print("Request failed:", error)
        return None
    
    def get_crypto_metrics(self, data, currency="USD") :
        if currency.upper() == "EUR" :
            price = data['eur_price']
            change = data['eur_exchange']
        else : 
            price = data['usd_price']
            change = data['usd_exchange']
        return price, change
        
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