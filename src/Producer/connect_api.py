from constants.constants import API_KEY
from requests import Session, Timeout, TooManyRedirects  
import json

API_URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"

def get_latest_coin_data(target_symbol="BTC"):

    parameters = {"symbol": target_symbol, "convert": "USD"}
    headers = {
        "Accepts": "application/json",       
        "X-CMC_PRO_API_KEY": API_KEY,}

    session = Session()
    session.headers.update(headers)    

    try:
        response = session.get(API_URL, params=parameters)  
        response.raise_for_status() 
        return response.json().get("data", {}).get(target_symbol, None)               
    except (ConnectionError, Timeout, TooManyRedirects, json.JSONDecodeError) as e:
        print(f"API request failed:{e}")
        return None