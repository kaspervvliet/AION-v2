
import requests
import os
import pandas as pd
from datetime import datetime
from aion_core.supabase_client import insert

def fetch_htf_candles(symbol: str, interval: str = "1H", limit: int = 100):
    url = f"https://api.kraken.com/ohlc/{symbol}?interval={interval}&limit={limit}"
    response = requests.get(url)
    if response.status_code != 200:
        print("[HTF] ❌ Kan HTF candles niet ophalen")
        return []
    return response.json()

def determine_htf_bias(candles: list) -> str:
    df = pd.DataFrame(candles)
    if df.empty or len(df) < 20:
        return "indecisive"
    df.columns = ["timestamp", "open", "high", "low", "close"]
    df["close"] = pd.to_numeric(df["close"])
    trend = df["close"].iloc[-1] - df["close"].iloc[-10]
    if trend > 0:
        return "bullish"
    elif trend < 0:
        return "bearish"
    return "indecisive"

def get_bias(symbol: str = "SOL/USDT") -> str:
    candles = fetch_htf_candles(symbol, interval="1H", limit=100)
    if not candles:
        return "indecisive"
    bias = determine_htf_bias(candles)
    timestamp = datetime.utcnow().isoformat()
    insert("htf_bias_log", {
        "timestamp": timestamp,
        "symbol": symbol,
        "bias": bias,
        "source": "1H"
    })
    return bias
