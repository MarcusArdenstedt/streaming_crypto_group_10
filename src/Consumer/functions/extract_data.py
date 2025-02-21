def extract_data(message):
    quote = message["quote"]["USD"]
    return {
        "coin": message["name"],
        "total_supply": message["total_supply"],
        "price_usd": quote["price"],
        "volume": quote["volume_24h"],
        "volume_change": quote["volume_change_24h"],
        "percent_change": quote["percent_change_1h"],
        "percent_change_24h": quote["percent_change_24h"],
        "percent_change_7d": quote["percent_change_7d"],
        "percent_change_30d": quote["percent_change_30d"],
        "updated": message["last_updated"] 
    }
