"""
📄 Bestand: signal_engine.py
🔍 Doel: [AUTO-GEGENEREERD: controleer doel handmatig]
🧩 Gebruikt door: onbekend
📦 Behoort tot: aion_core
🧠 Laatst geüpdatet: 2025-04-25
"""

import logging
logger = logging.getLogger(__name__)

from aion_core.kernel import trade_explainer
from aion_core.supabase_client import insert
from aion_core.kernel import reflection

def propose_trade(run_id: str, setup: dict, outcome: dict, decision: str, confidence: float, reason: str):
    rr = outcome.get("rr", 0)
    if decision != "GO" or rr < 1.5:
        logger.info(f"[SIGNAL] Trade genegeerd: status={decision}, rr={rr}")
        return None

    explanation = trade_explainer.explain_decision(setup, decision, confidence, reason)

    signal = {
        "run_id": run_id,
        "setup": setup,
        "outcome": outcome,
        "confidence": confidence,
        "reason": reason,
        "rr": rr,
        "explanation": explanation,
        "timestamp": outcome.get("timestamp")
    }

    logger.info("[SIGNAL] 💡 Voorstel gegenereerd:")
    logger.info(explanation)

    insert("signals", signal)
    return signal
