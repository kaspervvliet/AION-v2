
"""
📄 Bestand: aion_core/extensions/context_updater.py
🔍 Doel: Periodiek ophalen van verse Kraken-data en loggen naar Supabase context tabel + bias analyse
🧩 Gebruikt door: toekomstige datafundering en strategie-engine
📦 Behoort tot: AION V2 uitbreidingen
🧠 Verwacht implementatie van: requests, supabase_logger, bias_tracker
"""

import os
import time
import logging
from aion_core.utils.kraken import get_ohlc_latest
from aion_core.database.supabase_logger import insert_via_edge
from aion_core.extensions.bias_tracker import analyse_recent_candles

# Configuratie (Render-ready)
SYMBOL = os.getenv("AION_SYMBOL", "SOL/USDT")
TIMEFRAMES = ["15m", "1h", "4h", "1d"]
SLEEP_SECONDS = int(os.getenv("AION_CONTEXT_UPDATE_INTERVAL", 900))  # standaard 15 min

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_and_log(symbol: str, timeframe: str):
    """Haalt laatste candle op en logt naar Supabase + analyseert bias"""
    try:
        logger.info(f"Fetching {symbol} {timeframe} candle...")

        candle = get_ohlc_latest(symbol, timeframe)

        if not candle:
            logger.warning(f"Geen candle ontvangen voor {symbol} {timeframe}")
            return

        required_keys = ["time", "open", "high", "low", "close", "volume"]
        if not all(k in candle for k in required_keys):
            logger.warning(f"Candle ontbreekt verplichte velden: {candle}")
            return

        payload = {
            "symbol": symbol,
            "timeframe": timeframe,
            "timestamp": int(candle["time"]),
            "open": float(candle["open"]),
            "high": float(candle["high"]),
            "low": float(candle["low"]),
            "close": float(candle["close"]),
            "volume": float(candle["volume"]),
            "note": "auto-logged by context_updater"
        }

        result = insert_via_edge("context", payload)

        if result:
            logger.info(f"✅ {symbol} {timeframe} candle succesvol gelogd.")
            # Simuleer candles voor bias analyse (fake data array)
            fake_candles = [
                {"close": float(candle["close"]) - 0.5, "timestamp": int(candle["time"]) - 900},
                {"close": float(candle["close"]), "timestamp": int(candle["time"])}
            ]
            analyse_recent_candles(fake_candles, symbol, timeframe)
        else:
            logger.warning(f"⚠️ Supabase insert mogelijk mislukt.")

    except Exception as e:
        logger.error(f"Fout tijdens fetch_and_log: {e}")

def run_context_updater():
    """Hoofdlus: update context periodiek"""
    logger.info("🚀 Context Updater gestart...")

    while True:
        for timeframe in TIMEFRAMES:
            fetch_and_log(SYMBOL, timeframe)

        logger.info(f"Sleeping {SLEEP_SECONDS} seconden tot volgende update...")
        time.sleep(SLEEP_SECONDS)

if __name__ == "__main__":
    run_context_updater()
