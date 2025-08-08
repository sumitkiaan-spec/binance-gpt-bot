import threading
import time
from flask import Flask
from chatgpt_strategy import get_signal
from binance_api import place_order
import json

app = Flask(__name__)

# Load config
with open("config.json", "r") as f:
    config = json.load(f)

def trading_bot():
    print("✅ Trading bot started...")
    while True:
        print("🔄 Fetching signal from ChatGPT...")
        signal = get_signal(config["pair"])
        print(f"📈 Signal: {signal}")

        if signal == "BUY" or signal == "SELL":
            print(f"🚀 Executing {signal} order for ${config['lot_size']}")
            place_order(config["pair"], signal, config["lot_size"], config["sl_percent"], config["tp_percent"])

        time.sleep(config["trade_interval"] * 60)  # interval in seconds

# Run bot in background
threading.Thread(target=trading_bot).start()

@app.route('/')
def home():
    return "Binance GPT Auto-Trading Bot is live!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
