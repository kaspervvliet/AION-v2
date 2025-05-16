
"""
📄 Bestand: context_manager.py
🔍 Doel: Maakt contextdict per timeframe voor evaluatie
🧩 Gebruikt door: backtest, strategie-evaluatie
📦 Behoort tot: aion_core/backtest/
🧠 Verwacht implementatie van: context per tf met bias, sweep, fvg etc.
"""

import logging
from typing import Dict, Any
import pandas as pd
from aion_core.context.context_engine import detect_bos, detect_choch
from aion_core.utils.kraken import get_ohlc_kraken

logger = logging.getLogger("AION")

def create_context(df: pd.DataFrame, timeframe: str, symbol: str = "SOL/USDT") -> Dict[str, Any]:
    """
    Genereert contextdict met relevante informatie per timeframe,
    inclusief HTF-data en BOS/CHoCH detectie.
    """
    if df.empty or not isinstance(df, pd.DataFrame):
        logger.warning(f"Lege of ongeldige DataFrame ontvangen voor {timeframe}.")
        return {}

    try:
        candles = df.to_dict("records")

        context = {
            "symbol": symbol,
            "timeframe": timeframe,
            "timestamp": candles[-1].get("timestamp"),
            "bos": detect_bos(candles, direction="bullish"),  # of dynamisch bepalen
            "choch": detect_choch(candles),
        }

        # Voeg HTF candles toe
        context["htf_data"] = {
            "1h": get_ohlc_kraken(symbol.replace("/", ""), interval=60).to_dict("records"),
            "4h": get_ohlc_kraken(symbol.replace("/", ""), interval=240).to_dict("records"),
            "1d": get_ohlc_kraken(symbol.replace("/", ""), interval=1440).to_dict("records")
        }

        logger.debug(f"🧠 Gemaakte context voor {timeframe}: {context}")
        return context

    except Exception as e:
        logger.error(f"Fout bij aanmaken context voor {timeframe}: {e}")
        return {}
