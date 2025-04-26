"""
📄 Bestand: htf_context.py
🔍 Doel: Ophalen en interpreteren van higher timeframe candles
🧩 Gebruikt door: kernel.py, web_entry.py
📦 Behoort tot: aion_core.context
🧠 Verwacht implementatie van: requests, pandas, safe logging
"""

import time
import requests
import pandas as pd
from aion_core.utils.logger import logger

DEBUG_HTF = True

KRAKEN_URL = "https://api.kraken.com/0/public/OHLC"

def fetch_htf_candles(symbol: str = "SOLUSDT", interval: int = 60, retries: int = 3) -> list:
    attempt = 0
    while attempt < retries:
        try:
            params = {
                "pair": symbol,
                "interval": interval,
                "since": int(time.time()) - (3 * 24 * 60 * 60)
            }
            response = requests.get(KRAKEN_URL, params=params, timeout=10)
            response.raise_for_status()
            raw = response.json()

            if "error" in raw and raw["error"]:
                logger.warning(f"[HTF] Kraken API error: {raw['error']}")
                attempt += 1
                continue

            key = next((k for k in raw["result"].keys() if k != "last"), None)
            if not key:
                logger.warning("[HTF] Geen valide dataset gevonden in Kraken response.")
                attempt += 1
                continue

            candles = raw["result"][key]

            if DEBUG_HTF:
                logger.info(f"[HTF-DEBUG] 📊 Fetched {len(candles)} raw candles from Kraken.")

            if len(candles) < 20:
                logger.warning(f"[HTF] 📉 Te weinig candles ontvangen: {len(candles)}")
                attempt += 1
                continue

            return candles

        except Exception as e:
            logger.warning(f"[HTF] ❌ Fout bij ophalen HTF candles: {e}")
            attempt += 1

    logger.error("[HTF] 🚨 Alle pogingen gefaald om candles op te halen.")
    return []

def determine_htf_bias(candles: list) -> str:
    if not candles or len(candles) < 20:
        if DEBUG_HTF:
            logger.info(f"[HTF-DEBUG] ❗ Ontvangen candles: {len(candles)} — skipping bias calc.")
        logger.warning("[HTF] Onvoldoende candles voor biasbepaling.")
        return "neutral"

    df = pd.DataFrame(candles, columns=[
        "time", "open", "high", "low", "close", "vwap", "volume", "count"
    ])

    df["close"] = pd.to_numeric(df["close"], errors="coerce")
    df.dropna(subset=["close"], inplace=True)

    if DEBUG_HTF:
        logger.info(f"[HTF-DEBUG] ✅ {len(df)} valid candles after parsing.")

    if len(df) < 20:
        logger.warning("[HTF] 📉 Te weinig valide closes voor biasbepaling na parsing.")
        return "neutral"

    delta = df["close"].iloc[-1] - df["close"].iloc[-10]

    if delta > 0:
        return "bullish"
    elif delta < 0:
        return "bearish"
    else:
        return "neutral"