"""
📄 Bestand: htf_context.py
🔍 Doel: Bepalen van hogere timeframe (HTF) bias op basis van 1H candles
🧩 Gebruikt door: kernel.py
📦 Behoort tot: aion_core.context
🧠 Laatst geüpdatet: 2025-04-25
"""

import logging
import os
import requests
import pandas as pd
from datetime import datetime
from aion_core.supabase_client import insert

logger = logging.getLogger(__name__)

KRAKEN_URL = "https://api.kraken.com/0/public/OHLC"

def fetch_htf_candles(symbol: str = "SOLUSDT", interval: int = 60, limit: int = 100):
    try:
        params = {
            "pair": symbol,
            "interval": interval
        }
        response = requests.get(KRAKEN_URL, params=params)
        response.raise_for_status()
        raw = response.json()
        key = list(raw["result"].keys())[0]
        candles = raw["result"][key][-limit:]
        return candles
    except Exception as e:
        logger.warning(f"[HTF] ❌ Fout bij ophalen HTF candles: {e}")
        return []

def determine_htf_bias(candles: list) -> str:
    if not candles or len(candles) < 20:
        logger.warning("[HTF] Onvoldoende candles voor biasbepaling.")
        return "neutral"
    df = pd.DataFrame(candles, columns=[
        "time", "open", "high", "low", "close", "vwap", "volume", "count"
    ])
    df["close"] = pd.to_numeric(df["close"], errors="coerce")
    df.dropna(subset=["close"], inplace=True)

    if len(df) < 10:
        logger.warning("[HTF] Te weinig geldige closes.")
        return "neutral"

    trend = df["close"].iloc[-1] - df["close"].iloc[-10]
    if trend > 0:
        logger.info("[HTF] 📈 Bias: bullish")
        return "bullish"
    elif trend < 0:
        logger.info("[HTF] 📉 Bias: bearish")
        return "bearish"
    else:
        logger.info("[HTF] ⚖️ Bias: neutral")
        return "neutral"
