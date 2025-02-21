from quixstreams import Application
from functions.extract_data import extract_data
from functions.create_postgres_zink import create_postgres_sink

def main():
    app = Application(
        broker_address="localhost:9092",
        consumer_group="ADA_coin_group",
        auto_offset_reset="earliest",
    )
    coin_topic = app.topic(name= "ADA_coins", value_deserializer="json")
    
    sdf = app.dataframe(topic= coin_topic)
    
    
    # transformation 
    sdf = sdf.apply(extract_data)
    
    sdf = sdf.update(lambda row: print(row))
    
    
    postgres_sink = create_postgres_sink("cardano")
    sdf.sink(postgres_sink)
    
    app.run()
    

if __name__=='__main__':
    main()