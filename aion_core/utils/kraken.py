"""
📄 Bestand: kraken.py
🔍 Doel: Haalt OHLC-data op van Kraken API
🧩 Gebruikt door: strategieën, backtest
📦 Behoort tot: aion_core/utils/
🧠 Verwacht implementatie van: get_ohlc_kraken()
"""

import requests
import pandas as pd
import time
import os
import logging

logger = logging.getLogger("AION")

TIMEOUT = int(os.getenv("KRAKEN_TIMEOUT", 10))
RETRIES = int(os.getenv("KRAKEN_RETRIES", 3))

def get_ohlc_kraken(pair: str = "SOLUSD", interval: int = 60, since: int = None) -> pd.DataFrame:
    """
    Haalt OHLC-data op van Kraken API en converteert naar DataFrame.
    """
    url = f"https://api.kraken.com/0/public/OHLC?pair={pair}&interval={interval}"
    if since:
        url += f"&since={since}"

    for attempt in range(RETRIES):
        try:
            response = requests.get(url, timeout=TIMEOUT)
            response.raise_for_status()
            data = response.json()

            key = list(data["result"].keys())[0]
            ohlc = data["result"][key]
            df = pd.DataFrame(ohlc, columns=[
                "timestamp", "open", "high", "low", "close", "vwap", "volume", "count"
            ])
            df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")
            df = df.astype({"open": float, "high": float, "low": float, "close": float})
            logger.info(f"✅ OHLC-data opgehaald: {len(df)} rijen")
            return df

        except Exception as e:
            logger.warning(f"Fout bij ophalen Kraken OHLC (poging {attempt + 1}): {e}")
            time.sleep(2)

    logger.error("❌ Gefaalde poging tot ophalen Kraken-data na retries.")
    return pd.DataFrame()
