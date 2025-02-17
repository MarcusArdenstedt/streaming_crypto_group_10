from constants import COINMARKET_API
from requests import Session, Timeout, TooManyRedirects
import requests  
import json

API_URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"


def get_latest_coin_data(target_symbol="BTC"):

    parameters = {"symbol": target_symbol, "convert": "USD"}
    headers = {
        "Accepts": "application/json",       
        "X-CMC_PRO_API_KEY": COINMARKET_API,
    }

    session = Session()
    session.headers.update(headers)     

    try:
        response = session.get(API_URL, params=parameters)  
        response.raise_for_status() 
        return response.json().get("data", {}).get(target_symbol, None)               
    except (ConnectionError, Timeout, TooManyRedirects, json.JSONDecodeError) as e:
        print(f"API request failed:{e}")
        return None
    
# Get real-time exchange rates using the API

def fetch_exchange_rates(base_currency="USD"):
    """ 从 API 获取最新汇率 , 默认查询的是以 USD 为基准的所有其他货币的汇率"""
    url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"
    
    session = Session()
    
    try:
        response = session.get(url)
        response.raise_for_status()
        data = response.json()       
        return data["rates"]      
    except requests.exceptions.RequestException as e:
        print(f"Failed to obtain exchange rate: {e}")
        return None
    
    
    
if __name__ == "__main__":
    exchange_rates = fetch_exchange_rates("USD") 
    for currency, rate in exchange_rates.items():
        print(f"{currency}: {rate}")





