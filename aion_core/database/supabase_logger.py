"""
📄 Bestand: supabase_logger.py
🔍 Doel: Logt signalen en backtests naar Supabase
🧩 Gebruikt door: executor, tester
📦 Behoort tot: aion_core/database/
🧠 Verwacht implementatie van: upload_signal(), upload_backtest_results()
"""

import logging
from typing import Dict, Any
from aion_core.database.supabase_client import supabase

logger = logging.getLogger("AION")

def upload_signal(signal: Dict[str, Any]) -> None:
    try:
        supabase.table("aion_signals").insert(signal).execute()
        logger.info("🚀 Signaal geüpload naar Supabase")
    except Exception as e:
        logger.error(f"❌ Fout bij upload_signal: {e}
Payload: {signal}")

def upload_backtest_results(result: Dict[str, Any]) -> None:
    try:
        supabase.table("aion_backtests").insert(result).execute()
        logger.info("📈 Backtest geüpload naar Supabase")
    except Exception as e:
        logger.error(f"❌ Fout bij upload_backtest_results: {e}
Payload: {result}")

if __name__ == "__main__":
    dummy = {"entry": 100, "sl": 95, "tp": 110, "symbol": "SOL/USDT"}
    upload_signal(dummy)
    upload_backtest_results({**dummy, "rr": 2.0})

def upload_equity(equity: Dict[str, Any]) -> None:
    try:
        supabase.table("equity_log").insert(equity).execute()
        logger.info("💾 Equity geüpload naar Supabase")
    except Exception as e:
        logger.error(f"❌ Fout bij upload_equity: {e}\nPayload: {equity}")

def upload_reflection(reflection: Dict[str, Any]) -> None:
    try:
        supabase.table("reflections").insert(reflection).execute()
        logger.info("🧠 Reflectie geüpload naar Supabase")
    except Exception as e:
        logger.error(f"❌ Fout bij upload_reflection: {e}\nPayload: {reflection}")