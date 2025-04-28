
"""
📄 Bestand: bias_tracker.py
🔍 Doel: Detectie van bullish/bearish bias per timeframe
🧩 Gebruikt door: context_updater
📦 Behoort tot: aion_core/extensions
🧠 Verwacht implementatie van: supabase_logger.py
"""

import logging
from aion_core.database.supabase_logger import insert_via_edge
import os
from datetime import datetime
from dotenv import load_dotenv

# Laad .env variabelen indien lokaal
load_dotenv()

logger = logging.getLogger(__name__)

SUPABASE_TABLE_BIAS = "bias_tracker"

def determine_bias(current_close: float, previous_close: float) -> str:
    """Bepaal bullish, bearish of neutral bias."""
    if current_close > previous_close:
        return "bullish"
    elif current_close < previous_close:
        return "bearish"
    else:
        return "neutral"

def log_bias(symbol: str, timeframe: str, current_close: float, previous_close: float, timestamp: int) -> None:
    """Log de bepaalde bias naar Supabase."""
    bias = determine_bias(current_close, previous_close)

    payload = {
        "symbol": symbol,
        "timeframe": timeframe,
        "timestamp": timestamp,
        "bias": bias,
        "source": "basic_structure"
    }

    result = insert_via_edge(SUPABASE_TABLE_BIAS, payload)

    if result:
        logger.info(f"✅ Bias '{bias}' gelogd voor {symbol} {timeframe}.")
    else:
        logger.warning(f"⚠️ Bias logging mislukt voor {symbol} {timeframe}.")

def analyse_recent_candles(candle_data: list, symbol: str, timeframe: str) -> None:
    """Analyseer de laatste twee candles van een symbol/timeframe."""
    if len(candle_data) < 2:
        logger.warning(f"⚠️ Niet genoeg candles voor bias analyse {symbol} {timeframe}.")
        return

    previous_candle = candle_data[-2]
    current_candle = candle_data[-1]

    previous_close = previous_candle.get("close")
    current_close = current_candle.get("close")
    timestamp = current_candle.get("timestamp")

    if previous_close is not None and current_close is not None:
        log_bias(symbol, timeframe, current_close, previous_close, timestamp)
    else:
        logger.error(f"❌ Fout: Close waarden missen in candles {symbol} {timeframe}.")
