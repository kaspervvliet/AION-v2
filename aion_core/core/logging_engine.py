"""
📄 Bestand: logging_engine.py
🔍 Doel: Logt kernelbesluiten en bias naar console en Supabase
🧩 Gebruikt door: signal_engine, backtest
📦 Behoort tot: aion_core/core/
🧠 Verwacht implementatie van: log_bias_state(), get_last_bias_state()
"""

import logging
from aion_core.utils.logtools import log_step
from aion_core.extensions.supabase_writer import log_bias_state
from aion_core.database.supabase_reader import get_last_bias_state
from typing import Any, Dict

logger = logging.getLogger("AION")

def log_decision(decision: Dict[str, Any]) -> None:
    """
    Logt besluitvorming inclusief status, confidence en strategy.
    """
    with log_step("Besluitlogica"):
        status = decision.get("status", "onbekend")
        confidence = decision.get("confidence")
        strategy = decision.get("strategy")
        logger.info(f"🤖 Besluitstatus: {status} — Strategie: {strategy} — Confidence: {confidence}")

def log_bias_and_decision(decision: Dict[str, Any], context: Dict[str, Any], symbol: str = "SOL/USDT") -> None:
    """
    Logt huidige bias + besluit naar Supabase.
    """
    bias = context.get("bias", "n.v.t")
    logger.info(f"🧭 Bias state: {bias}")
    payload = {
        "bias": bias,
        "symbol": symbol,
        "context": context,
        "decision": decision
    }
    log_bias_state(payload)

if __name__ == "__main__":
    test_decision = {"status": "GO", "confidence": 3, "strategy": "choch_bias"}
    test_context = {"bias": "long", "sweep": True}
    log_decision(test_decision)
    log_bias_and_decision(test_decision, test_context)

from aion_core.database.supabase_reader import get_last_bias_state
from typing import Optional

def fetch_previous_bias(symbol: str = "SOL/USDT") -> Optional[str]:
    """Haalt de laatst gelogde bias op voor een symbool."""
    state = get_last_bias_state(symbol)
    return state.get("bias") if state else None
