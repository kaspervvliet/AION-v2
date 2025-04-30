
"""
📄 Bestand: memory.py
🔍 Doel: Tijdelijke opslag van contextuele inzichten (bias, trades, state)
🧩 Gebruikt door: kernel, context_builder
📦 Behoort tot: aion_core/kernel
🧠 Verwacht implementatie van: recover_last_bias_state()
"""

from typing import Optional
from aion_core.database import supabase_logger
import logging

logger = logging.getLogger(__name__)

# Voorbeeld memory-structuur (vereenvoudigd)
current_bias = None
recent_signals = []

def recover_last_bias_state(symbol: str, timeframe: str) -> Optional[str]:
    """Haalt de laatst bekende bias op uit Supabase en slaat deze lokaal op."""
    global current_bias
    bias = supabase_logger.get_last_bias_state(symbol, timeframe)
    if bias:
        current_bias = bias
        logger.info(f"[MEMORY] Herstelde bias state: {bias}")
    else:
        logger.warning("[MEMORY] Geen eerdere bias state gevonden.")
    return bias
