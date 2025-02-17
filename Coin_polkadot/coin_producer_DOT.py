import time
from quixstreams import Application   # 流式数据处理的库，处理 Kafka 消息的对象，负责从 Kafka 中获取数据和发布数据。
import json
from pprint import pprint
from connect_api import get_latest_coin_data, fetch_exchange_rates

TARGET_COIN = "DOT"
CURRENCY = "SEK"      # 目标货币（可以选择 SEK, NOK, DKK 等）

# Get exchange rate
exchange_rates = fetch_exchange_rates()

def convert_price(usd_price, CURRENCY="SEK"):
    """ 使用 API 获取的实时汇率转换 USD 价格 """
    if exchange_rates and CURRENCY in exchange_rates:
        return round(usd_price * exchange_rates[CURRENCY], 2)
    return usd_price     # 如果汇率不可用，返回 USD 价格


# 创建了一个 Quix Streams 的应用实例，创建了一个名为 coins 的 Kafka 主题，输出JSON，连接到本地的 Kafka 服务，
def main():
    app = Application(broker_address="localhost:9092", consumer_group="DOT_coin_group")
    coins_topic = app.topic(name="DOT_coins", value_serializer="json")

    # 获取所有北欧国家的货币符号
    nordic_countries = ["SEK", "NOK", "DKK", "ISK", "FIM"]      # 可以根据需要添加更多货币

    # 获取 Kafka 生产者对象 producer，负责向 Kafka 主题发送消息。
    with app.get_producer() as producer:

        while True:
            coin_latest = get_latest_coin_data(TARGET_COIN)

            # 获取原始美元价格
            usd_price = coin_latest["quote"]["USD"]["price"]

            # 在 coin_latest["quote"] 中新增北欧国家的货币价格，ex  "NOK": {"price": 17200.60}
            for currency in nordic_countries:
                local_price = convert_price(usd_price, currency)
                coin_latest["quote"][currency] = {"price": local_price}      

            # 将获取到的数据序列化为 Kafka 消息
            kafka_message = coins_topic.serialize(key=coin_latest["symbol"], value=coin_latest)

            # 打印日志显示各个货币的价格, "SEK: 18000, NOK: 17100, DKK: 13500, ISK: 252000, FIM: 11340"
            price_info = ", ".join([f"{cur}: {coin_latest['quote'][cur]['price']}" for cur in nordic_countries])
            print(f"produce event with key = {kafka_message.key}, price = {price_info}")

            # 将序列化后的消息发送到 Kafka 主题 coins 中
            producer.produce(topic=coins_topic.name, key=kafka_message.key, value=kafka_message.value)

            time.sleep(30)    # 每次抓取数据后会有 30 秒的延迟


if __name__ == "__main__":
    main()

# 在 coin_consumer.py 中消费到的 coin_latest 将会直接包含类似下面的数据结构
# {
#   "symbol": "ETH",
#   "name": "Ethereum",
#   "quote": {
#     "USD": {
#       "price": 1800.45,
#       "volume_24h": 150000000
#     },
#     "SEK": {
#       "price": 16250.50
#     },
#     "NOK": {
#       "price": 17200.60
#     },
#     "DKK": {
#       "price": 12000.75
#     },
#     "ISK": {
#       "price": 240000
#     },
#     "FIM": {
#       "price": 10800
#     }
#   }
# }





