import threading
import time
from flask import Flask
from chatgpt_strategy import get_signal
from binance_api import place_order
import json

app = Flask(__name__)

with open("config.json", "r") as f:
    config = json.load(f)

def trading_bot():
    print("✅ Trading bot started...")
    while True:
        print("🔁 Fetching GPT signal...")
        signal = get_signal(config["pair"])
        print(f"📈 Signal from GPT: {signal}")

        if signal in ["BUY", "SELL"]:
            print(f"🚀 Executing {signal} for ${config['lot_size']}...")
            place_order(config["pair"], signal, config["lot_size"], config["sl_percent"], config["tp_percent"])
        else:
            print("🟡 Holding position...")

        time.sleep(config["trade_interval"] * 60)

threading.Thread(target=trading_bot).start()

@app.route('/')
def home():
    return "Binance GPT Live Trading Bot is running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
