
"""
📄 Bestand: adaptive_strategy_selector.py
🔍 Doel: Kiezen van geschikte strategie en adaptieve SL/TP afleiding
🧩 Gebruikt door: main_live, kernel
📦 Behoort tot: aion_core
🧠 Bevat: select_adaptive_strategy(), tune_sl_tp_from_performance()
"""

from typing import List, Tuple

def select_adaptive_strategy(context) -> object:
    """Placeholder functie voor strategie selectie obv context."""
    from aion_modules.strategies.rsi_sweep import Strategy
    return Strategy()

def tune_sl_tp_from_performance(trades: List[dict]) -> Tuple[float, float]:
    """Berekent een aangepast SL/TP-percentage op basis van recente prestaties."""
    if not trades:
        return 0.01, 0.02  # default SL/TP

    win_trades = [t for t in trades if t.get("outcome") == "win"]
    loss_trades = [t for t in trades if t.get("outcome") == "loss"]

    winrate = len(win_trades) / len(trades) if trades else 0.5

    avg_win_rr = sum(t.get("rr_achieved", 0) for t in win_trades) / len(win_trades) if win_trades else 1.5
    avg_loss_rr = sum(t.get("rr_achieved", 0) for t in loss_trades) / len(loss_trades) if loss_trades else -1

    # Simpele heuristiek
    target_rr = max(1.0, min(avg_win_rr * 0.9, 2.5))
    stop_rr = 1.0

    sl_pct = 0.01  # bijv. 1%
    tp_pct = sl_pct * target_rr

    return sl_pct, tp_pct
