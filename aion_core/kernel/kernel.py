"""
📄 Bestand: kernel.py
🔍 Doel: Vormt setup om naar strategy decision (entry validatie en executie)
🧩 Gebruikt door: signal_engine, strategy_executor, backtest
📦 Behoort tot: aion_core/kernel/
🧠 Verwacht implementatie van: strategie-evaluatie, contextvalidatie
"""

from aion_core.utils.logger import logger
from aion_core.knowledge.structure_awareness import detect_bos, detect_choc
from aion_core.knowledge.htf_bias_checker import get_htf_bias
from aion_core.knowledge.mtf_bias_checker import is_bias_consistent


def evaluate_entry(context: dict) -> dict:
    """
    Genereert een strategiebeslissing op basis van structuur en bias
    """
    try:
        if not context or "candles" not in context:
            raise ValueError("Geen geldige context")

        structure = context.get("structure", {})
        if not detect_bos(structure) and not detect_choc(structure):
            return {"status": "rejected", "reason": "❌ Geen BOS of CHoCH in structuur"}

        bias = get_htf_bias(context.get("symbol", ""))
        if bias not in ["bullish", "bearish"]:
            return {"status": "rejected", "reason": "⚠️ Onduidelijke bias"}

        direction = "long" if bias == "bullish" else "short"
        logger.info(f"✅ Entry geaccepteerd richting {direction.upper()}")

        return {
            "status": "accepted",
            "direction": direction,
            "context": context
        }

    except Exception as e:
        logger.error(f"❌ Kernel evaluatie mislukt: {e}")
        return {"status": "error", "reason": str(e)}