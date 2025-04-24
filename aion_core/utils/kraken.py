
import requests
import pandas as pd
from datetime import datetime

def fetch_candles_from_kraken(pair: str = "SOLUSDT", interval: str = "15") -> pd.DataFrame:
    """
    Haalt OHLCV-candles op van de Kraken API.
    Interval kan o.a. zijn: 1, 5, 15, 30, 60, 240, 1440 (in minuten).
    """
    interval_map = {
        "1m": "1", "5m": "5", "15m": "15", "30m": "30",
        "1h": "60", "4h": "240", "1d": "1440"
    }
    if interval not in interval_map and interval not in interval_map.values():
        raise ValueError(f"Unsupported interval: {interval}")

    kraken_interval = interval_map.get(interval, interval)
    url = f"https://api.kraken.com/0/public/OHLC?pair={pair}&interval={kraken_interval}"

    response = requests.get(url)
    response.raise_for_status()

    result = response.json()["result"]
    pair_key = next((k for k in result.keys() if k != "last"), None)
    raw_candles = result[pair_key]

    df = pd.DataFrame(raw_candles, columns=[
        "timestamp", "open", "high", "low", "close", "vwap", "volume", "count"
    ])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")
    df.set_index("timestamp", inplace=True)

    numeric_cols = ["open", "high", "low", "close", "vwap", "volume"]
    df[numeric_cols] = df[numeric_cols].astype(float)

    return df
