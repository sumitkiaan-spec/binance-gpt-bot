import openai
import os
from binance.client import Client

openai.api_key = os.getenv("OPENAI_API_KEY")
binance_client = Client(os.getenv("API_KEY"), os.getenv("SECRET_KEY"))

def get_signal(pair):
    try:
        # Fetch recent price data
        ticker = binance_client.get_symbol_ticker(symbol=pair)
        price = float(ticker["price"])

        # Fetch RSI and EMAs (simple simulation, you can improve it later)
        klines = binance_client.get_klines(symbol=pair, interval=Client.KLINE_INTERVAL_5MINUTE, limit=21)
        closes = [float(kline[4]) for kline in klines]  # Close prices

        if len(closes) < 21:
            print("⚠️ Not enough data to calculate indicators")
            return "HOLD"

        ema_8 = sum(closes[-8:]) / 8
        ema_21 = sum(closes[-21:]) / 21

        # Calculate RSI (simplified)
        deltas = [closes[i+1] - closes[i] for i in range(len(closes)-1)]
        gains = [delta for delta in deltas if delta > 0]
        losses = [-delta for delta in deltas if delta < 0]
        avg_gain = sum(gains[-14:]) / 14 if gains else 0.0001
        avg_loss = sum(losses[-14:]) / 14 if losses else 0.0001
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))

        # Build intelligent prompt
        prompt = f"""
        You are a crypto trading assistant.

        BTC/USDT market snapshot:
        - Current price: ${price:,.2f}
        - RSI(14): {rsi:.2f}
        - EMA(8): {ema_8:.2f}
        - EMA(21): {ema_21:.2f}
        - EMA(8) > EMA(21): {"Yes" if ema_8 > ema_21 else "No"}

        Based on this data, should I BUY, SELL, or HOLD BTC/USDT right now?
        Respond with one word only: BUY, SELL or HOLD.
        """

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )

        answer = response.choices[0].message.content.strip().upper()
        if answer in ["BUY", "SELL", "HOLD"]:
            return answer
        else:
            return "HOLD"

    except Exception as e:
        print(f"❌ GPT signal generation failed: {e}")
        return "HOLD"
