from quixstreams import Application
from quixstreams.sinks.community.postgresql import PostgreSQLSink
from constants import (
    POSTGRES_DBNAME,
    POSTGRES_HOST,
    POSTGRES_PASSWORD,
    POSTGRES_PORT,
    POSTGRES_USER)
from pprint import pprint

# 🔹 **数值格式化函数**，转换为 K / M / B 形式
def format_number(num):
    if num >= 1_000_000_000:
        return f"{num / 1_000_000_000:.1f}B"  # 10 亿 = 1B
    elif num >= 1_000_000:
        return f"{num / 1_000_000:.1f}M"  # 100 万 = 1M
    elif num >= 1_000:
        return f"{num / 1_000:.1f}K"  # 1 千 = 1K
    return str(num)

# 解析 Kafka 消息数据 message,是来自 Kafka 的 JSON 数据,返回一个 Python 字典，用于后续存入数据库.
def extract_coin_data(message):
    latest_quote = message["quote"]["USD"]
    return{
        "coin": message["name"],
        "price_usd": round(latest_quote["price"], 2),
        "SEK": round(message["quote"].get("SEK", {}).get("price", 0), 2),
        "NOK": round(message["quote"].get("NOK", {}).get("price", 0), 2),
        "DKK": round(message["quote"].get("DKK", {}).get("price", 0), 2),
        "ISK": round(message["quote"].get("ISK", {}).get("price", 0), 2),
        "FIM": round(message["quote"].get("FIM", {}).get("price", 0), 2),
        "volume_24h": format_number(latest_quote["volume_24h"]),  # 24h 交易量格式化
        "volume_change_24h": round(latest_quote.get("volume_change_24h", 0), 2),  # 24h 交易量变化
        "updated": message["last_updated"]
    }

# 创建 PostgreSQL 数据库 Sink, 目标表是 bitcoin.
def create_postgres_sink():
    sink = PostgreSQLSink(
        host=POSTGRES_HOST, # type: ignore
        port=POSTGRES_PORT, # type: ignore
        dbname=POSTGRES_DBNAME, # type: ignore
        user=POSTGRES_USER,  # type: ignore
        password=POSTGRES_PASSWORD, # type: ignore
        table_name="cardano",
        schema_auto_update=True,)    # 如果数据模式变了（比如新字段），自动更新 PostgreSQL 表结构。
    
    return sink

# 1. 主程序逻辑, Application 连接 Kafka， app 是实例
def main():
    app = Application(
        broker_address="localhost:9092",
        consumer_group="ADA_coin_group",        # Kafka 消费者组（多个 consumer 共享读取）
        auto_offset_reset="earliest",
    )

    # 2. 订阅 Kafka 主题 coins，消息格式是 JSON
    #  app 是 Application 类的一个实例，代表 QuixStreams 的应用对象。它的作用是 管理 Kafka 连接、订阅主题、处理数据流，并最终存入数据库。
    coins_topic = app.topic(name="ADA_coins", value_deserializer="json")

    sdf = app.dataframe(topic=coins_topic)

    # 3. transformations, 转换数据：从 Kafka 消息中提取 coin、price_usd、volume、updated 等字段
    sdf = sdf.apply(extract_coin_data)

    # 4. 处理后的数据存入 PostgreSQL bitcoin 表
    # sink to postgres
    postgres_sink = create_postgres_sink()

    sdf.sink(postgres_sink)

    # 每次收到 Kafka 消息，就打印处理后的 coin_data
    sdf.update(lambda transformed_data: pprint(transformed_data))
    
    # 5. 启动 QuixStreams 应用，消费 Kafka 数据，并存入数据库
    app.run()  

if __name__ == "__main__":
    main()












