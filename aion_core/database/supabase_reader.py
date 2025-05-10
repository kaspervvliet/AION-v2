"""
📄 Bestand: supabase_reader.py
🔍 Doel: Leest signalen en biasstatus uit Supabase
🧩 Gebruikt door: backtest, logging_engine
📦 Behoort tot: aion_core/database/
🧠 Verwacht implementatie van: get_last_bias_state(), get_best_strategy()
"""

import logging
from typing import Dict, Any
from aion_core.database.supabase_client import supabase

logger = logging.getLogger("AION")

def get_last_bias_state(symbol: str = "SOL/USDT") -> Dict[str, Any]:
    try:
        res = supabase.table("aion_bias").select("*").eq("symbol", symbol).order("id", desc=True).limit(1).execute()
        data = res.data[0] if res.data else {}
        logger.info("🔁 Laatste bias opgehaald")
        return data
    except Exception as e:
        logger.error(f"❌ Fout bij ophalen bias: {e}")
        return {}

def get_last_signal(symbol: str = "SOL/USDT") -> Dict[str, Any]:
    try:
        res = supabase.table("aion_signals").select("*").eq("symbol", symbol).order("id", desc=True).limit(1).execute()
        data = res.data[0] if res.data else {}
        logger.info("📡 Laatste signaal opgehaald")
        return data
    except Exception as e:
        logger.error(f"❌ Fout bij ophalen signaal: {e}")
        return {}

def get_best_strategy() -> Dict[str, Any]:
    try:
        res = supabase.table("aion_backtests").select("*").order("rr", desc=True).limit(1).execute()
        data = res.data[0] if res.data else {}
        logger.info("🏆 Beste strategie opgehaald")
        return data
    except Exception as e:
        logger.error(f"❌ Fout bij ophalen beste strategie: {e}")
        return {}

if __name__ == "__main__":
    print(get_last_bias_state())
    print(get_last_signal())
    print(get_best_strategy())
