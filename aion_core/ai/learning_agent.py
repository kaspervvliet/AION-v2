"""
📄 Bestand: learning_agent.py
🔍 Doel: Zelflerende module die strategie-prestaties analyseert en strategiekeuze optimaliseert
🧩 Gebruikt door: adaptive_strategy_selector, main_live, backtest_engine
📦 Behoort tot: aion_core/ai
🧠 Analyseert Supabase-trades, houdt strategie-scores bij, en stuurt tuning aan
"""

from collections import defaultdict
from aion_core.database.supabase_reader import load_recent_trades
from aion_core.utils.logger import get_logger
from typing import Dict, List

logger = get_logger(__name__)
strategy_scores: Dict[str, float] = defaultdict(lambda: 1.0)

def analyze_performance(trades: List[dict]) -> Dict[str, float]:
    scores = defaultdict(list)
    for trade in trades:
        strat = trade.get("strategy")
        if not strat:
            continue
        rr = trade.get("rr_achieved", 1.0)
        outcome = trade.get("outcome")
        if outcome == "win":
            scores[strat].append(rr)
        elif outcome == "loss":
            scores[strat].append(-1 * rr)
    result = {}
    for strat, rr_list in scores.items():
        if rr_list:
            avg_score = sum(rr_list) / len(rr_list)
            result[strat] = round(avg_score, 3)
    return result

def update_strategy_scores():
    trades = load_recent_trades(limit=100)
    perf = analyze_performance(trades)
    for strat, score in perf.items():
        strategy_scores[strat] = score
    logger.info(f"[Agent] Strategie-scores geüpdatet: {strategy_scores}")

def rank_strategies(available: List[str]) -> List[str]:
    return sorted(available, key=lambda s: -strategy_scores.get(s, 0))

def get_top_strategy(available: List[str]) -> str:
    ranked = rank_strategies(available)
    if ranked:
        logger.info(f"[Agent] Beste strategie op basis van score: {ranked[0]}")
        return ranked[0]
    logger.warning("[Agent] Geen scorende strategie beschikbaar.")
    return None
