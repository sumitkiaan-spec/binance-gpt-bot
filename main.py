import threading
import time
from flask import Flask

app = Flask(__name__)

def trading_bot():
    print("✅ Trading bot started...")
    while True:
        print("🤖 Bot is running... waiting for next signal")
        time.sleep(60)

# Start the bot in the background
threading.Thread(target=trading_bot).start()

@app.route('/')
def home():
    return "Binance GPT Trading Bot is running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
import time

print("Trading bot started...")

# This keeps the bot alive forever
while True:
    print("Bot is alive... waiting for next action...")
    time.sleep(60)
