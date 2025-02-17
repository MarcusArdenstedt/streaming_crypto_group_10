from common.constants import COINMARKETCAP_API
from requests import Session, Timeout, TooManyRedirects
import requests  
import json

API_URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"

# 1. 从 CoinMarketCap API 获取指定加密货币（默认为 "BTC" 比特币）的最新数据
def get_latest_coin_data(target_symbol="BTC"):

    parameters = {"symbol": target_symbol, "convert": "USD"}
    # 发送请求时的参数：传入的加密货币符号（如 "BTC"），返回的数据中包含以美元（USD）计价的信息。
    headers = {
        "Accepts": "application/json",       
        "X-CMC_PRO_API_KEY": COINMARKETCAP_API,
    }

    session = Session()
    session.headers.update(headers)      # 发送 HTTP 请求， 将请求头添加到会话中。

    try:
        response = session.get(API_URL, params=parameters)    # 发送 HTTP GET 请求
        response.raise_for_status()  # 检查 HTTP 状态码（非 200 会报错）
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
        data = response.json()       # 返回的响应数据（通常是 JSON 格式）解析为 Python 字典
        return data["rates"]         # 提取 rates 键对应的值, 一堆国家的汇率字典
    except requests.exceptions.RequestException as e:
        print(f"Failed to obtain exchange rate: {e}")
        return None
    
    
    
if __name__ == "__main__":
    exchange_rates = fetch_exchange_rates("USD")  # 获取基于 USD 的汇率
    for currency, rate in exchange_rates.items():
        print(f"{currency}: {rate}")



