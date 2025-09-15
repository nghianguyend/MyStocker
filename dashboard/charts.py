import requests
import pandas as pd 
from datetime import datetime
from dotenv import load_dotenv
import os

class FetchData :
    def __init__(self) :
        load_dotenv()
        self.crypto_api = os.getenv("COINAPI_KEY")
        self.base_url = "https://rest.coinapi.io/v1"
        
        if not self.crypto_api:
            raise ValueError("No API key found. Set COINAPI_KEY in .env")

        self.headers = {"X-CoinAPI-Key": self.crypto_api}
        
    def get_exchange_rate(self, base="BTC", quote="USD"):
        """Fetch latest exchange rate for base/quote pair"""
        url = f"{self.base_url}/exchangerate/{base}/{quote}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
        