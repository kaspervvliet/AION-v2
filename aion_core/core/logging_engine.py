
"""
📄 Bestand: aion_core/core/logging_engine.py
🔍 Doel: Logging-coördinatie voor context en bias
🧩 Gebruikt door: main_live.py, web_entry.py
📦 Behoort tot: aion_core
🧠 Verwacht implementatie van: context logging, bias state updates
"""

from aion_core.utils.logger import log
from aion_core.database.supabase_logger import log_context_data
from aion_core.extensions.supabase_writer import log_bias_data as log_bias_state

def log_full_context(symbol: str, context: dict, timeframe: str):
    try:
        log_context_data(symbol, context)
        log("📤 Context gelogd naar Supabase")
    except Exception as e:
        log(f"⚠️ Fout bij log_context_data: {e}")

def log_bias(symbol: str, timeframe: str, bias: str, source: str = "engine"):
    try:
        log_bias_state(symbol, timeframe, bias, source)
        log("📌 Bias gelogd")
    except Exception as e:
        log(f"⚠️ Fout bij log_bias_state: {e}")
