from requests import Session, Timeout, TooManyRedirects
import requests  
import json


    
# Get real-time exchange rates using the API

def fetch_exchange_rates(base_currency="USD", rate ="SEK"):
    """ 从 API 获取最新汇率 , 默认查询的是以 USD 为基准的所有其他货币的汇率"""
    url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"
    
    session = Session()
    
    try:
        response = session.get(url)
        response.raise_for_status()
        data = response.json()       
        return data["rates"][rate]
    except requests.exceptions.RequestException as e:
        print(f"Failed to obtain exchange rate: {e}")
        return None
    
    
    
if __name__ == "__main__":
    exchange_rates = fetch_exchange_rates("USD") 
    
    # for currency, rate in exchange_rates.items():
    #     print(f"{currency}: {rate}")





