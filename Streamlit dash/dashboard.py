import streamlit as st
from streamlit_autorefresh import st_autorefresh
from sqlalchemy import create_engine
import pandas as pd
from charts import line_chart
from constants import (
    POSTGRES_DBNAME,
    POSTGRES_HOST,
    POSTGRES_PASSWORD,
    POSTGRES_PORT,
    POSTGRES_USER)

# a connection to postgres， 连接 PostgreSQL 数据库
connection_string = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DBNAME}"

# 创建 SQLAlchemy 数据库引擎，用于执行 SQL 查询
engine = create_engine(connection_string)

# 定义数据加载函数，用于执行 SQL 查询
def load_data(query):
    with engine.connect() as conn:
        df = pd.read_sql(query, conn)   # 运行 SQL 语句，将查询结果存入 DataFrame
        df = df.set_index("timestamp")   # 将 timestamp 列设置为索引
        return df

# count 自定刷新网页, 每 10 秒（10,000 毫秒）刷新一次页面
count = st_autorefresh(interval=10 * 1000, limit=100, key="data_refresh")

def layout(): 
    df_ada = load_data("select * from cardano")
    df_dot = load_data("select * from polkadot")

    st.markdown("# Analysis of Cryptocurrencies")
    st.markdown("This is a simple dashboard about the latest market quote for Cryptocurrencies.")

    # table
    st.markdown("## Cardano and Polkadot Data")
    st.markdown("This will display live data from coin market API")
    st.markdown("Latest data for Cardano")
    st.dataframe(df_ada.tail())
    st.markdown("Latest data for Polkadot")
    st.dataframe(df_dot.tail())

    # Selectbox
    st.markdown("## Nordic countries selection.")
    st.markdown("Shows cryptocurrencies in different countries' currencies.")
    countries = ["Sweden", "Norway", "Denmark", "Iceland", "Finland"]   # ["SEK", "NOK", "DKK", "ISK", "FIM"]
    country = st.selectbox(
        "Which Nordic country to choose?", countries) 
    currencies = {"Sweden":"SEK", "Norway":"NOK", "Denmark":"DKK", "Iceland":"ISK", "Finland":"FIM"}
    currency = currencies.get(country, "Unknown")

    st.markdown(f"Now showing you the data in local currency from {country}.") 


    # metric
    labels = ("name", "price", "percent_change_24h")
    cols = st.columns(3)
    

    # Line chart - price
    st.markdown(f"## Chart showing the last currency price in {currency} ")
    st.pyplot(line_chart(df_ada, df_dot, "cardano", "polkadot", currency))




if __name__ == "__main__":
    layout()
    










