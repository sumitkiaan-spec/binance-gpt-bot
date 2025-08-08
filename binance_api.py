import os
from binance.client import Client

API_KEY = os.getenv("API_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")

client = Client(API_KEY, SECRET_KEY)

def place_order(pair, side, amount_usdt, sl_percent, tp_percent):
    try:
        price = float(client.get_symbol_ticker(symbol=pair)["price"])
        quantity = round(amount_usdt / price, 6)

        order = client.create_order(
            symbol=pair,
            side=side.upper(),
            type="MARKET",
            quantity=quantity
        )
        print(f"✅ Trade Executed: {side} {quantity} {pair} @ {price}")

    except Exception as e:
        print(f"❌ Trade failed: {e}")
