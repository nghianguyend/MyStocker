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
            resp = requests.get(self.crypto_url, params=params)
            resp.raise_for_status()
            if resp.status_code == 200 :
                data = resp.json()
                return data
        except requests.exceptions.HTTPError as e:
            print("HTTP error:", e)
        except requests.exceptions.RequestException as e:
            print("Request failed:", e)
        return None
        