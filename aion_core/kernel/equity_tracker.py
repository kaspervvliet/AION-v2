"""
📄 Bestand: equity_tracker.py
🔍 Doel: Logt equity-states van strategieën naar Supabase
🧩 Gebruikt door: backtests, live-trading reflectie
📦 Behoort tot: aion_core/kernel/
🧠 Verwacht implementatie van: supabase_writer, logger
"""

import time
from aion_core.utils.logger import logger
from aion_core.database.supabase_writer import insert_row


def log_equity_snapshot(signal: dict, result: str, balance: float):
    """
    Logt equity na een trade (win/loss) met contextuele metadata
    """
    try:
        if not signal or "entry" not in signal or "stop" not in signal or "tp" not in signal:
            logger.warning("⚠️ Onvolledig signaal — geen equity log")
            return False

        payload = {
            "timestamp": time.time(),
            "symbol": signal.get("symbol"),
            "strategy": signal.get("strategy"),
            "direction": signal.get("direction"),
            "entry": signal.get("entry"),
            "stop": signal.get("stop"),
            "tp": signal.get("tp"),
            "result": result,
            "balance": balance
        }

        result = insert_row("equity_log", payload)
        if result["success"]:
            logger.info("✅ Equity snapshot gelogd.")
            return True
        else:
            logger.error(f"❌ Fout bij equity-log: {result['error']}")
            return False
    except Exception as e:
        logger.error(f"❌ Exception bij equity log: {e}")
        return False
