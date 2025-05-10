"""
📄 Bestand: htf_bias_checker.py
🔍 Doel: Detecteert HTF-bias op basis van MA20 en MA50
🧩 Gebruikt door: kernel, strategieën, bias_tracker
📦 Behoort tot: aion_core/knowledge/
🧠 Verwacht implementatie van: pandas, logger
"""

import pandas as pd
from aion_core.utils.logger import logger


def get_htf_bias(symbol: str) -> str:
    """
    Simpele MA-biasdetector: MA20 > MA50 = bullish
    """
    try:
        df = fetch_ohlc_data(symbol, tf="4h", limit=60)  # placeholder
        if df is None or len(df) < 50:
            logger.warning("⚠️ Te weinig candles voor HTF-bias.")
            return "neutral"

        df["ma20"] = df["close"].rolling(20).mean()
        df["ma50"] = df["close"].rolling(50).mean()

        if pd.isnull(df["ma20"].iloc[-1]) or pd.isnull(df["ma50"].iloc[-1]):
            logger.warning("⚠️ MA-data onvolledig.")
            return "neutral"

        if df["ma20"].iloc[-1] > df["ma50"].iloc[-1]:
            return "bullish"
        elif df["ma20"].iloc[-1] < df["ma50"].iloc[-1]:
            return "bearish"
        else:
            return "neutral"

    except Exception as e:
        logger.error(f"❌ Fout in HTF-biasdetector: {e}")
        return "neutral"


def fetch_ohlc_data(symbol: str, tf: str = "4h", limit: int = 60) -> pd.DataFrame:
    """
    Dummy loader — te vervangen door kraken.get_ohlc() of context
    """
    # Voor testdoeleinden return lege DataFrame
    return pd.DataFrame(columns=["close"])
