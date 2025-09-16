import requests
import pandas as pd 
from datetime import datetime
from dotenv import load_dotenv
import os

class FetchData :
    def __init__(self) :
        self.crypto_url = "https://api.coingecko.com/api/v3/simple/price"
    def get_cryto_prices(self) :
        try :
            params = {
                'ids' : 'bitcoin, ethereum, doge, cardano',
                'vs_currencies' : 'usd, eur',
                'include_24hr_change' : 'true'
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
                        'price' : coin_info['usd'],
                        'exchange' : coin_info['usd_24h_change'],
                        'time' : datetime.now()
                    })
                return pd.DataFrame(coin_list)
                
                
        except requests.exceptions.HTTPError as e:
            print("HTTP error:", e)
        except requests.exceptions.RequestException as e:
            print("Request failed:", e)
        return None
        