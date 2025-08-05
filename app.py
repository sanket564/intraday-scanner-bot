import requests
import time
from datetime import datetime
import pandas as pd

# === USER CONFIG ===
TELEGRAM_BOT_TOKEN = '8392997604:AAG2TRfmLemLTLjU9ngoS-vypxCwZcKDWQQ'
TELEGRAM_CHAT_ID = '1471908211'

# === SETTINGS ===
NSE_API_URL = "https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%20500"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "application/json"
}


def fetch_stock_data():
    session = requests.Session()
    session.headers.update(HEADERS)

    try:
        response = session.get(NSE_API_URL, timeout=10)
        data = response.json()
        stocks = data['data']
        return pd.DataFrame(stocks)
    except Exception as e:
        print(f"Failed to fetch stock data: {e}")
        return pd.DataFrame()


def calculate_vwap(df):
    # Fake VWAP logic (mock) for demo
    # In real life, fetch minute-wise OHLCV data from paid APIs like Zerodha/Alpaca
    df['vwap'] = (df['lastPrice'].astype(float) + df['dayHigh'].astype(float) + df['dayLow'].astype(float)) / 3
    return df


def strategy_vwap_volume(df):
    df['lastPrice'] = df['lastPrice'].astype(float)
    df['vwap'] = df['vwap'].astype(float)
    df['volume'] = df['volume'].astype(int)

    alerts = []

    for _, row in df.iterrows():
        # Buy: Price > VWAP and volume high
        if row['lastPrice'] > row['vwap'] and row['volume'] > 500000:
            alerts.append(f"🟢 BUY {row['symbol']} @ ₹{row['lastPrice']} | VWAP ₹{round(row['vwap'], 2)}")
        # Sell: Price < VWAP and volume high
        elif row['lastPrice'] < row['vwap'] and row['volume'] > 500000:
            alerts.append(f"🔴 SELL {row['symbol']} @ ₹{row['lastPrice']} | VWAP ₹{round(row['vwap'], 2)}")
    
    return alerts


def send_telegram_message(msg):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": msg
        }
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Telegram error: {e}")


def main():
    print(f"Started scanning at {datetime.now()}")
    df = fetch_stock_data()
    if df.empty:
        print("No data received.")
        return

    df = calculate_vwap(df)
    alerts = strategy_vwap_volume(df)

    if alerts:
        msg = f"🚨 VWAP + Volume Alerts [{datetime.now().strftime('%H:%M:%S')}]:\n" + "\n".join(alerts)
        send_telegram_message(msg)
    else:
        print("No signals found.")


if __name__ == "__main__":
    main()
