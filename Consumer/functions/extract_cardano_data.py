def extract_cardano_data(message):
    quote = message["quote"]["USD"]
    return {
        "coin": message["name"],
        "price_usd": quote["price"],
        "volume": quote["volume_24h"],
        "updated": message["last_updated"] 
    }
