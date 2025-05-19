
"""
📄 Bestand: candle_manager.py
🔍 Doel: Efficiënt ophalen en cachen van OHLC-data per timeframe
🧩 Gebruikt door: kernel, signal_engine
📦 Behoort tot: aion_core/utils
🧠 Verwacht implementatie van: get_ohlc_kraken(symbol, interval)
"""

import time
from typing import Optional
import pandas as pd
from aion_core.utils.kraken import get_ohlc_kraken

# Interne cache per timeframe
ohlc_cache = {
    "15m": {"timestamp": 0, "data": None},
    "1h": {"timestamp": 0, "data": None},
    "4h": {"timestamp": 0, "data": None},
    "1d": {"timestamp": 0, "data": None},
}

def kraken_interval_for(tf: str) -> int:
    return {
        "15m": 15,
        "1h": 60,
        "4h": 240,
        "1d": 1440,
    }[tf]

def should_fetch_ohlc(tf: str, last_ts: int) -> bool:
    interval_map = {
        "15m": 15 * 60,
        "1h": 60 * 60,
        "4h": 4 * 60 * 60,
        "1d": 24 * 60 * 60,
    }
    now = int(time.time())
    interval = interval_map[tf]
    return (now // interval) > (last_ts // interval)

def get_fresh_ohlc(symbol: str, tf: str) -> Optional[pd.DataFrame]:
    cache = ohlc_cache[tf]
    if should_fetch_ohlc(tf, cache["timestamp"]):
        df = get_ohlc_kraken(symbol, interval=kraken_interval_for(tf))
        if not df.empty:
            cache["timestamp"] = int(time.time())
            cache["data"] = df
    return cache["data"]
