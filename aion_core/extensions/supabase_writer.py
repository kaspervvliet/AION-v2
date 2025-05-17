
"""
📄 Bestand: aion_core/extensions/supabase_writer.py
🔍 Doel: Logging naar Supabase-tabellen (bias, signals, equity, reflections)
🧩 Gebruikt door: strategy_executor.py, main_live.py
📦 Behoort tot: aion_core
🧠 Verwacht implementatie van: supabase client uit supabase_logger.py
"""

from aion_core.database.supabase_logger import supabase
import logging
import uuid
import time


logger = logging.getLogger('AION')

def log_bias_data(symbol: str, timeframe: str, bias: str, source: str):
    if not supabase:
        logger.error('❌ Supabase-client niet geïnitialiseerd')
        return
    try:
        data = {
            "id": str(uuid.uuid4()),
            "symbol": symbol,
            "timeframe": timeframe,
            "bias": bias,
            "source": source,
            "timestamp": int(time.time())
        }
        supabase.table("bias_tracker").insert(data).execute()
    except Exception as e:
        logger.error(f"❌ Fout bij log_bias_data: {e}")


def log_signal_data(symbol: str, setup: dict, rr: float, reason: str):
    if not supabase:
        logger.error('❌ Supabase-client niet geïnitialiseerd')
        return
    try:
        data = {
            "id": str(uuid.uuid4()),
            "timestamp": int(time.time()),
            "symbol": symbol,
            "setup": setup,
            "rr": rr,
            "reason": reason
        }
        supabase.table("signals").insert(data).execute()
    except Exception as e:
        logger.error(f"❌ Fout bij log_signal_data: {e}")


def log_reflection_data(setup: dict, decision: str, outcome: str, explanation: str):
    if not supabase:
        logger.error('❌ Supabase-client niet geïnitialiseerd')
        return
    try:
        data = {
            "id": str(uuid.uuid4()),
            "timestamp": int(time.time()),
            "setup": setup,
            "decision": decision,
            "outcome": outcome,
            "explanation": explanation
        }
        supabase.table("reflections").insert(data).execute()
    except Exception as e:
        logger.error(f"❌ Fout bij log_reflection_data: {e}")


def log_equity_data(symbol: str, rr: float, result: float, confidence: float, balance: float):
    if not supabase:
        logger.error('❌ Supabase-client niet geïnitialiseerd')
        return
    try:
        data = {
            "timestamp": int(time.time()),
            "symbol": symbol,
            "rr": rr,
            "result": result,
            "confidence": confidence,
            "balance": balance
        }
        supabase.table("equity_log").insert(data).execute()
    except Exception as e:
        logger.error(f"❌ Fout bij log_equity_data: {e}")
