import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def get_signal(pair):
    try:
        prompt = f"Based on current market trends and recent BTC/USDT 5-minute data, should I BUY or SELL {pair}? Reply with only one word: BUY, SELL or HOLD."

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
        print(f"❌ GPT failed: {e}")
        return "HOLD"
