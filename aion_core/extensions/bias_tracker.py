"""
📄 Bestand: bias_tracker.py
🔍 Doel: Logt high timeframe bias naar Supabase
🧩 Gebruikt door: kernel, strategieën
📦 Behoort tot: aion_core/kernel/
🧠 Verwacht implementatie van: supabase_logger.insert_bias_log()
"""

import logging
from aion_core.database.supabase_writer import insert_bias_log

logger = logging.getLogger("AION")

def log_bias(symbol: str, bias_dict: dict):
    if "bias" not in bias_dict or "timestamp" not in bias_dict:
        logger.warning(f"Ongeldige bias input: {bias_dict}")
        return

    bias = bias_dict["bias"]
    timestamp = bias_dict["timestamp"]

    try:
        insert_bias_log({
            "symbol": symbol,
            "bias": bias,
            "timestamp": timestamp
        })
        logger.info(f"Bias log: {bias} voor {symbol} @ {timestamp}")
    except Exception as e:
        logger.error(f"Fout bij loggen van bias: {e}")

if __name__ == "__main__":
    # Dummy test
    dummy = {"bias": "long", "timestamp": "2025-05-09T14:00:00Z"}
    log_bias("SOL/USDT", dummy)