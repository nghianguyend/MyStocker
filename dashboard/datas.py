import requests
import pandas as pd 
from datetime import datetime, timedelta
from dotenv import load_dotenv
import yfinance as yf
import pytz
import ta
class FetchData :
    def __init__(self) :
        self.crypto_url = "https://api.coingecko.com/api/v3/simple/price"
    def get_cryto_prices(self) :
        try :
            params = {
                'ids': 'bitcoin,ethereum,cardano,dogecoin,solana,polkadot,litecoin,tron,chainlink,polygon',
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
    
        
    def get_stock_prices(self, ticker, period="1mo", interval="1d"):
        end_date = datetime.now()
        if period == "1wk":
            start_date = end_date - timedelta(days=7)
            stock_info = yf.download(ticker, start=start_date, end=end_date, interval=interval)
        else:
            stock_info = yf.download(ticker, period=period, interval=interval)
        return stock_info
    
    def process_datas(self, data) :
        if data.index.tzinfo == None :
            data.index = data.index.tz_localize("UTC")
        data.index = data.index.tz_convert("US/Eastern")
        data.reset_index(inplace=True)
        if "Date" in data.columns:
            data.rename(columns={"Date": "Datetime"}, inplace=True)
        return data