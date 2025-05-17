
"""
📄 Bestand: bias_logger.py
🔍 Doel: Logt alleen bias naar Supabase bij verandering
🧩 Gebruikt door: htf_bias_checker, kernel
📦 Behoort tot: aion_core/utils
🧠 Verwacht implementatie van: get_last_bias_state, log_bias_data
"""

import logging
from aion_core.database.supabase_reader import get_last_bias_state
from aion_core.extensions.supabase_writer import log_bias_data

logger = logging.getLogger("AION")

def log_if_bias_changed(symbol: str, timeframe: str, bias: str, source: str):
    try:
        last = get_last_bias_state(symbol)
        if last.get("bias") != bias:
            log_bias_data(symbol, timeframe, bias, source)
        else:
            logger.debug(f"🔁 Bias ongewijzigd voor {symbol} ({bias}) — geen logging")
    except Exception as e:
        logger.error(f"❌ Bias logging failed voor {symbol}: {e}")
