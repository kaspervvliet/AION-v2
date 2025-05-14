"""
📄 Bestand: supabase_writer.py
🔍 Doel: Schrijft signalen, bias en reflectie naar Supabase
🧩 Gebruikt door: strategy_executor, tester, engine
📦 Behoort tot: aion_core/extensions/
🧠 Verwacht implementatie van: upload_signal(), upload_backtest_results(), log_bias_state()
"""

import logging
from typing import Dict, Any
from aion_core.database.supabase_client import supabase

logger = logging.getLogger("AION")

def upload_signal(signal: Dict[str, Any]) -> None:
    try:
        supabase.table("aion_signals").insert(signal).execute()
        logger.info("🚀 Signaal geüpload")
    except Exception as e:
        logger.error(f"❌ upload_signal fout: {e}\nPayload: {signal}")

def upload_backtest_results(result: Dict[str, Any]) -> None:
    try:
        supabase.table("aion_backtests").insert(result).execute()
        logger.info("📈 Backtestresultaat geüpload")
    except Exception as e:
        logger.error(f"❌ upload_backtest_results fout: {e}\nPayload: {result}")

def upload_reflection_result(result: Dict[str, Any]) -> None:
    try:
        supabase.table("aion_reflections").insert(result).execute()
        logger.info("🧠 Reflectie geüpload")
    except Exception as e:
        logger.error(f"❌ upload_reflection_result fout: {e}\nPayload: {result}")

def log_bias_state(payload: Dict[str, Any]) -> None:
    try:
        supabase.table("aion_bias").insert(payload).execute()
        logger.info("🧭 Biaslog geüpload")
    except Exception as e:
        logger.error(f"❌ log_bias_state fout: {e}\nPayload: {payload}")

if __name__ == "__main__":
    dummy = {"symbol": "SOL/USDT", "rr": 2.0, "entry": 158, "sl": 155, "tp": 165}
    upload_signal(dummy)
    upload_backtest_results(dummy)
    upload_reflection_result({**dummy, "reflection": "Test reflectie"})
    log_bias_state({"bias": "long", "symbol": "SOL/USDT", "context": {}, "decision": {}})
