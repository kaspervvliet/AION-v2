
## Bestand: aion_core/database/supabase_logger.py

"""
📄 Bestand: aion_core/database/supabase_logger.py
🔍 Doel: Centraal loggen van AION data naar Supabase (context, trades, bias, equity, reflections).
🧩 Gebruikt door: Strategie-modules, core engine
📦 Behoort tot: aion_core/database
🧠 Verwacht implementatie van: supabase_client
"""

from aion_core.database.supabase_client import supabase
from aion_core.utils.logger import log

def log_context(context_data: dict):
    try:
        supabase.table("context").insert(context_data).execute()
        log("Context gelogd.", level="info")
    except Exception as e:
        log(f"Fout bij loggen context: {e}", level="error")


def log_trade_result(trade_data: dict):
    try:
        supabase.table("trades").insert(trade_data).execute()
        log("Trade result gelogd.", level="info")
    except Exception as e:
        log(f"Fout bij loggen trade result: {e}", level="error")


def log_htf_bias(bias_data: dict):
    try:
        supabase.table("htf_bias_log").insert(bias_data).execute()
        log("HTF bias gelogd.", level="info")
    except Exception as e:
        log(f"Fout bij loggen HTF bias: {e}", level="error")


def log_equity_update(equity_data: dict):
    try:
        supabase.table("equity_log").insert(equity_data).execute()
        log("Equity update gelogd.", level="info")
    except Exception as e:
        log(f"Fout bij loggen equity update: {e}", level="error")


def log_reflection(reflection_data: dict):
    try:
        supabase.table("reflections").insert(reflection_data).execute()
        log("Reflection gelogd.", level="info")
    except Exception as e:
        log(f"Fout bij loggen reflection: {e}", level="error")
