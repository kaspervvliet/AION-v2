"""
📄 Bestand: sl_tp_injector.py
🔍 Doel: Injecteert adaptieve SL/TP waarden in signalen op basis van performance
🧩 Gebruikt door: alle strategieën via signal manager of directe injectie
📦 Behoort tot: aion_core/extensions
🧠 Roept tune_sl_tp_from_performance() aan
"""

from aion_core.adaptive_strategy_selector import tune_sl_tp_from_performance
import logging
from typing import Any

logger = logging.getLogger("AION")

def apply_adaptive_sl_tp(signal: dict[str, Any], trades: list[dict[str, Any]]) -> None:
    """
    Stelt SL/TP in op het signal dict obv recente performance.
    """
    if not trades:
        logger.warning("⚠️ Geen trades beschikbaar voor SL/TP-aanpassing")
        return

    sl, tp = tune_sl_tp_from_performance(trades)
    signal['sl_pct'] = sl
    signal['tp_pct'] = tp
    logger.info(f"🎯 SL/TP geïnjecteerd: SL={sl}, TP={tp}")

if __name__ == "__main__":
    test_signal = {}
    dummy_trades = [
        {"rr": 2.1, "success": True},
        {"rr": 0.9, "success": False},
        {"rr": 1.8, "success": True},
    ]
    apply_adaptive_sl_tp(test_signal, dummy_trades)
    print(test_signal)
