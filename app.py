import requests
import pandas as pd
from datetime import datetime
from telegram import Bot
import os

# Load secrets from environment
TELEGRAM_TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
TELEGRAM_CHAT_ID = os.environ['TELEGRAM_CHAT_ID']

bot = Bot(token=TELEGRAM_TOKEN)

def fetch_nse_data():
    url = "https://www.niftyindices.com/Indices/Constituents/NIFTY-500"
    tables = pd.read_html(url)
    stock_list = tables[0]["Symbol"].tolist()
    return stock_list

def get_intraday_data(symbol):
    # Placeholder for API call like Upstox, Zerodha, etc.
    # Here we mock with random data
    from random import randint
    price = randint(100, 1000)
    volume = randint(1000, 100000)
    vwap = price + randint(-10, 10)
    return price, volume, vwap

def should_buy(price, volume, vwap):
    return price > vwap and volume > 10000

def scan_market():
    stock_list = fetch_nse_data()
    alerts = []

    for symbol in stock_list:
        try:
            price, volume, vwap = get_intraday_data(symbol)
            if should_buy(price, volume, vwap):
                alerts.append(f"📈 Buy Signal: {symbol} | Price: ₹{price} | VWAP: ₹{vwap} | Volume: {volume}")
        except:
            continue

    if alerts:
        message = "\n".join(alerts)
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
    else:
        print(f"[{datetime.now()}] No signals found.")

if __name__ == "__main__":
    scan_market()
