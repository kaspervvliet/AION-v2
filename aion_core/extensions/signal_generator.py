from aion_core.extensions.supabase_bias_and_signal_helper import upload_signal


"""
📄 Bestand: signal_generator.py
🔍 Doel: Genereren van trading signals obv context + bias
🧩 Gebruikt door: toekomstige strategieengine
📦 Behoort tot: aion_core/extensions
🧠 Verwacht implementatie van: supabase_logger
"""

import logging
import os
from aion_core.database.supabase_logger import insert_via_edge
from datetime import datetime
from dotenv import load_dotenv

# Laad .env variabelen indien lokaal
load_dotenv()

logger = logging.getLogger(__name__)

SUPABASE_TABLE_SIGNALS = "signals"

DEFAULT_RR = 1.5
DEFAULT_CONFIDENCE = 0.7

def generate_signal(symbol: str, timeframe: str, bias: str, price: float, timestamp: int) -> None:
    """Genereer en log een trading signal obv bias en huidige prijs."""
    if bias not in ["bullish", "bearish"]:
        logger.warning(f"⚠️ Ongeldige bias '{bias}' ontvangen. Geen signal aangemaakt.")
        return

    setup = {
        "entry": price,
        "type": "long" if bias == "bullish" else "short",
        "rr": DEFAULT_RR,
    }

    payload = {
        "symbol": symbol,
        "timeframe": timeframe,
        "timestamp": timestamp,
        "setup": setup,
        "reason": f"Auto-generated based on {bias} bias.",
        "rr": DEFAULT_RR,
        "confidence": DEFAULT_CONFIDENCE,
        "note": "auto-signal via signal_generator",
        "price": price,
        "status": "pending"
    }

    result = insert_via_edge(SUPABASE_TABLE_SIGNALS, payload)

    if result:
        logger.info(f"✅ Signal ({setup['type']}) succesvol gelogd voor {symbol} {timeframe}.")
    else:
        logger.warning(f"⚠️ Signal logging mislukt voor {symbol} {timeframe}.")

def create_signal_from_bias(context: dict, bias_info: dict) -> None:
    """Verwerk context en bias naar een signal."""
    try:
        symbol = context.get("symbol")
        timeframe = context.get("timeframe")
        price = context.get("close")
        timestamp = context.get("timestamp")
        bias = bias_info.get("bias")

        if None in (symbol, timeframe, price, timestamp, bias):
            logger.warning("⚠️ Incomplete data ontvangen voor signal generatie.")
            return

        generate_signal(symbol, timeframe, bias, price, timestamp)

    except Exception as e:
        logger.error(f"❌ Fout bij create_signal_from_bias: {e}")
