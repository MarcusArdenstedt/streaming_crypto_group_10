import streamlit as st  
from streamlit_autorefresh import st_autorefresh
from sqlalchemy import create_engine
import pandas as pd
from constants.constants import (POSTGRES_DBNAME, POSTGRES_HOST, POSTGRES_PASSWORD, POSTGRES_PORT, POSTGRES_USER)
from charts import line_chart
from rates_api import fetch_exchange_rates
from millify import millify
from print_crypto_info import crypto_info

currency = ["SEK", "NOK", "DKK", "EUR", "USD", "ISK"]
connection_string = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DBNAME}"

engine = create_engine(connection_string)

def load_data(query):
    with engine.connect() as conn:
        df = pd.read_sql(query, conn)
        df = df.set_index("timestamp")
        return df
           
    
    
def main():
    df = load_data("SELECT * FROM cardano;")

    st.markdown("# Streamed data for Cardano(ADA) from coinmarket")
    

    currency_code = st.selectbox("Choose currency to show", currency)
    st.markdown(f"## Latest price in {currency_code} for Cardano")
    if currency_code == "SEK":
        currency_rate = fetch_exchange_rates(rate=currency_code)
        price_chart = line_chart(x =df.index, y= (df["price_usd"] * currency_rate), title= f"Price {currency_code}")
        st.pyplot(price_chart)
    if currency_code == "NOK":
        currency_rate = fetch_exchange_rates(rate=currency_code)
        price_chart = line_chart(x =df.index, y= (df["price_usd"] * currency_rate), title= f"Price {currency_code}")
        st.pyplot(price_chart)
    if currency_code == "DKK":
        currency_rate = fetch_exchange_rates(rate=currency_code)
        price_chart = line_chart(x =df.index, y= (df["price_usd"] * currency_rate), title= f"Price {currency_code}")
        st.pyplot(price_chart)
    if currency_code == "EUR":
        currency_rate = fetch_exchange_rates(rate=currency_code)
        price_chart = line_chart(x =df.index, y= (df["price_usd"] * currency_rate), title= f"Price {currency_code}")
        st.pyplot(price_chart)
    if currency_code == "ISK":
        currency_rate = fetch_exchange_rates(rate=currency_code)
        price_chart = line_chart(x =df.index, y= (df["price_usd"] * currency_rate), title= f"Price {currency_code}")
        st.pyplot(price_chart)

    if currency_code == "USD":
        price_chart = line_chart(x= df.index, y= df["price_usd"], title= f"price {currency_code}")
        st.pyplot(price_chart)
        crypto_info(df, currency_code)
        # column_1, column_2, column_3 = st.columns(3)
        # column_1.metric("Volume", millify(df["volume"].tail(1)), f"{millify(df['volume_change'].tail(1))}%", border=True,)
        # column_2.metric("price change 1h", f"{millify(df['price_usd'].tail(1), precision = 2)}{currency_code}", f"{millify(df['percent_change'].tail(1), precision = 2)}%", border=True)
        # column_3.metric("Price change 24h", f"{millify(df['price_usd'].tail(1), precision= 2)}{currency_code}", f"{millify(df['percent_change_24h'].tail(1))}%", border=True)


if __name__ == "__main__":
    main()