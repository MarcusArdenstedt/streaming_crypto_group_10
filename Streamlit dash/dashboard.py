import sys
import os

sys.path.append(os.path.abspath("../streaming_crypto_group_10"))
import streamlit as st  
from streamlit_autorefresh import st_autorefresh
from sqlalchemy import create_engine
import pandas as pd
from constants.constants import (POSTGRES_DBNAME, POSTGRES_HOST, POSTGRES_PASSWORD, POSTGRES_PORT, POSTGRES_USER)
from charts import line_chart

currency = ["SEK", "NOK", "DKK", "EUR", "USD"]
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
    

    st.selectbox("Choose currency to show", currency)
    if currency == "SEK":
       pass
   
   
    st.markdown("## Latest price in USD for Cardano")
    price_chart = line_chart(x= df.index, y= df["price_usd"], title= "price USD")
    st.pyplot(price_chart)


if __name__ == "__main__":
    main()