
"""
📄 Bestand: sl_tp_injector.py
🔍 Doel: Injecteert adaptieve SL/TP waarden in signalen op basis van performance
🧩 Gebruikt door: alle strategieën via signal manager of directe injectie
📦 Behoort tot: aion_core/extensions
🧠 Roept tune_sl_tp_from_performance() aan
"""

from aion_core.adaptive_strategy_selector import tune_sl_tp_from_performance

def apply_adaptive_sl_tp(signal: dict, trades: list) -> None:
    """Stelt SL/TP in op het signal dict obv recente performance."""
    sl, tp = tune_sl_tp_from_performance(trades)
    signal['sl_pct'] = sl
    signal['tp_pct'] = tp
