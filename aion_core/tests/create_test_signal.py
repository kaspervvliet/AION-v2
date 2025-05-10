"""
📄 Bestand: create_test_signal.py
🔍 Doel: Injecteert testsignaal in Supabase
🧩 Gebruikt door: ontwikkelaars voor testdoeleinden
📦 Behoort tot: root/test
🧠 Verwacht implementatie van: supabase_logger.insert_signal()
"""

import logging
import time
from aion_core.database import supabase_logger
from config import is_muted

logger = logging.getLogger("AION")

def insert_test_signal():
    if is_muted():
        logger.info("Create test signal is gemute — skipping.")
        return

    signal = {
        "symbol": "SOL/USDT",
        "entry": 158.5,
        "sl": 155.0,
        "tp": 165.0,
        "rr": 2.1,
        "type": "long",
        "source": "test",
        "timestamp": int(time.time())
    }

    try:
        supabase_logger.insert_signal(signal)
        logger.info("Testsignaal succesvol toegevoegd aan Supabase.")
    except Exception as e:
        logger.error(f"Fout bij test-signaal insert: {e}")

if __name__ == "__main__":
    insert_test_signal()
