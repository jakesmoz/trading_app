import tkinter as tk
from ui import setup_ui, update_recommendations
import ccxt
import numpy as np
import pandas as pd
import ta

# Info connection binance
binance = ccxt.binance({
    'enableRateLimit': True,
    'options': {
        'defaultType': 'spot'
    }
})

# Trading pairs, almal teenoor USDT stablecoin
trading_pairs = ['BTC/USDT', 'ETH/USDT', 'ADA/USDT', 'BNB/USDT', 'SOL/USDT', 'XRP/USDT', 'DOGE/USDT', 'TON/USDT',
                 'SHIB/USDT', 'AVAX/USDT', 'TRX/USDT', 'DOT/USDT']


# Funkies om historiese data te kry
def fetch_data(symbol, style='day'):
    limit = 60 if style == 'day' else 90 if style == 'swing' else 180
    timeframe = '1m' if style == 'day' else '1d' if style == 'swing' else '1w'
    candles = binance.fetch_ohlcv(symbol, timeframe, limit=limit)
    df = pd.DataFrame(candles, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    return df


# Funksie om aanwysers te bereken
def calculate_sma(dataframe, window=10):
    return ta.trend.sma_indicator(dataframe['close'], window)


def calculate_ema(dataframe, window=7):
    return ta.trend.ema_indicator(dataframe['close'], window)


def calculate_rsi(dataframe, window=7):
    return ta.momentum.rsi(dataframe['close'], window)


def calculate_stochastic(dataframe, window=14):
    stoch_k = ta.momentum.stoch(dataframe['high'], dataframe['low'], dataframe['close'], window)
    stoch_d = ta.momentum.stoch_signal(dataframe['high'], dataframe['low'], dataframe['close'], window)
    return stoch_k, stoch_d


# Funksie om voorstelle te maak i.t.v aanwysers
def analyze_data(symbol, style):
    df = fetch_data(symbol, style)
    df['sma'] = calculate_sma(df)
    df['ema'] = calculate_ema(df)
    df['rsi'] = calculate_rsi(df)
    df['stochastic_k'], df['stochastic_d'] = calculate_stochastic(df)

    recommendation = f"Analysis for {symbol} ({style} trading):\n"
    recommendation += f"SMA (10): {df['sma'].iloc[-1]:.2f}\n"
    recommendation += f"EMA (7): {df['ema'].iloc[-1]:.2f}\n"
    recommendation += f"RSI (7): {df['rsi'].iloc[-1]:.2f}\n"
    recommendation += f"Stochastic K: {df['stochastic_k'].iloc[-1]:.2f}\n"
    recommendation += f"Stochastic D: {df['stochastic_d'].iloc[-1]:.2f}\n"

    last_close = df['close'].iloc[-1]

    if df['rsi'].iloc[-1] < 30 and df['stochastic_k'].iloc[-1] < 20:
        take_profit = last_close * 1.02  # Vat wins teen 2%
        stop_loss = last_close * 0.98  # Stop loss teen 2% daling
        recommendation += f"Recommendation: Buy (Potential long position)\nSuggested Buy Price: {last_close:.2f}\nSuggested Take Profit: {take_profit:.2f}\nSuggested Stop Loss: {stop_loss:.2f}\n"
    elif df['rsi'].iloc[-1] > 70 and df['stochastic_k'].iloc[-1] > 80:
        take_profit = last_close * 0.98  # Take profit at 2% decrease
        stop_loss = last_close * 1.02  # Stop loss teen 2% increase
        recommendation += f"Recommendation: Sell (Potential short position)\nSuggested Sell Price: {last_close:.2f}\nSuggested Take Profit: {take_profit:.2f}\nSuggested Stop Loss: {stop_loss:.2f}\n"
    else:
        take_profit = last_close * 1.02
        stop_loss = last_close * 0.98
        recommendation += f"Recommendation: Trade with caution\nSuggested Take Profit: {take_profit:.2f}\nSuggested Stop Loss: {stop_loss:.2f}\n"

    return recommendation


def fetch_and_analyze(style):
    recommendations = ""
    for pair in trading_pairs:
        recommendations += analyze_data(pair, style)
        recommendations += "\n"
    update_recommendations(recommendations)


def main():
    root = tk.Tk()
    setup_ui(root, fetch_and_analyze)
    root.mainloop()


if __name__ == "__main__":
    main()

