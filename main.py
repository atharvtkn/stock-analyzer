import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os

class StockAnalyzer:
    def __init__(self):
        self.path = 'stocks.csv'
        self.figure = None

    def fetch_data(self, symbol, period):
        try:
            df = yf.download(symbol, period=period, interval='1d', progress=False, auto_adjust=False)
            if df.empty:
                return False, "No data found. Check the ticker symbol."

            df.reset_index(inplace=True)
            df['Symbol'] = symbol.upper()

            file_exists = os.path.exists(self.path)
            df.to_csv(self.path, mode='a', index=False, header=not file_exists)

            return True, df
        except Exception as e:
            return False, str(e)

    def show_summary(self, df):
        symbol = df['Symbol'].iloc[0]
        current_price = float(df['Close'].iloc[-1])
        high = float(df['High'].max())
        low = float(df['Low'].min())
        avg = float(df['Close'].mean())

        return f"""📊 Stock Summary: {symbol}
    Current Price: ${current_price:.2f}
    High: ${high:.2f}
    Low: ${low:.2f}
    Average: ${avg:.2f}
    Days: {len(df)}"""


    def visualize(self, df):
        self.figure = plt.figure(figsize=(8, 5))
        plt.plot(df['Date'], df['Close'], color='#1E88E5', label='Close Price', linewidth=2)
        plt.xticks(rotation=45)
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Price (USD)', fontsize=12)
        plt.title(f"{df['Symbol'].iloc[0]} Stock Price Trend", fontsize=14, fontweight='bold')
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.legend()
        plt.tight_layout()
        plt.show(block=False)

    def clear_data(self):
        if os.path.exists(self.path):
            open(self.path, 'w').close()
