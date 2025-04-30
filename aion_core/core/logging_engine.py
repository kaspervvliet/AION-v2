
"""
📄 Bestand: logging_engine.py
🔍 Doel: Logging van kernelbesluiten, setups en Supabase-interactie
🧩 Gebruikt door: kernel, streamlit, CLI
📦 Behoort tot: aion_core/core
🧠 Gebruikt: log_context uit utils/logtools
"""

import logging
from aion_core.utils.logtools import log_context
from aion_core.database.supabase_logger import log_bias_state, get_last_bias_state

logger = logging.getLogger(__name__)

def log_decision(symbol: str, timeframe: str, decision: dict):
    with log_context("Log kernelbesluit"):
        logger.info(f"[{symbol} @ {timeframe}] 📣 Besluit: {decision['status']} ({decision['confidence']}) – {decision['reason']}")
        log_bias_state(symbol, timeframe, decision.get("bias", "unknown"))

def fetch_previous_bias(symbol: str, timeframe: str):
    with log_context("Fetch laatste bias"):
        return get_last_bias_state(symbol, timeframe)
