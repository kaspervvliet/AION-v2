"""
📄 Bestand: adaptive_strategy_selector.py
🔍 Doel: Kiezen van geschikte strategie en adaptieve SL/TP afleiding
🧩 Gebruikt door: main_live, kernel
📦 Behoort tot: aion_core
🧠 Bevat: select_adaptive_strategy(), tune_sl_tp_from_performance()
"""

from typing import List, Tuple
from aion_core.strategy_pool_initializer import load_strategies
from aion_core.utils.logger import get_logger

logger = get_logger(__name__)
strategies = load_strategies()

def select_adaptive_strategy(context) -> object:
    for strat in strategies:
        try:
            if strat.validate_market(context.history):
                logger.info(f"[Selector] Geselecteerde strategie: {strat.name}")
                return strat
        except Exception as e:
            logger.warning(f"[Selector] Strategie {strat.name} faalt bij selectie: {e}")
    logger.warning("[Selector] Geen geschikte strategie gevonden.")
    return None

def tune_sl_tp_from_performance(trades: List[dict]) -> Tuple[float, float]:
    if not trades:
        return 0.01, 0.02
    win_trades = [t for t in trades if t.get("outcome") == "win"]
    loss_trades = [t for t in trades if t.get("outcome") == "loss"]
    winrate = len(win_trades) / len(trades) if trades else 0.5
    avg_rr_win = sum(t.get("rr_achieved", 2.0) for t in win_trades) / len(win_trades) if win_trades else 2.0
    adjusted_sl = 0.01 * (1.0 - winrate)
    adjusted_tp = 0.02 + (avg_rr_win * 0.005)
    logger.info(f"[Tuning] SL: {adjusted_sl:.4f}, TP: {adjusted_tp:.4f}, Winrate: {winrate:.2%}")
    return round(adjusted_sl, 4), round(adjusted_tp, 4)
