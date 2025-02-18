import streamlit as st
from millify import millify

def crypto_info(df, currency_code):
    column_1, column_2, column_3 = st.columns(3)
    column_1.metric("Volume", millify(df["volume"].tail(1)), f"{millify(df['volume_change'].tail(1))}%", border=True,)
    column_2.metric("price change 1h", f"{millify(df['price_usd'].tail(1), precision = 2)}{currency_code}", f"{millify(df['percent_change'].tail(1), precision = 2)}%", border=True)
    column_3.metric("Price change 24h", f"{millify(df['price_usd'].tail(1), precision= 2)}{currency_code}", f"{millify(df['percent_change_24h'].tail(1))}%", border=True)