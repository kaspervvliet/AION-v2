"""
📄 Bestand: adaptive_strategy_selector.py
🔍 Doel: Selecteert beste strategie op basis van recente performance
🧩 Gebruikt door: main_live, strategy_executor
📦 Behoort tot: aion_core/
🧠 Verwacht implementatie van: Supabase-reader, winrate-evaluatie, strategy pool
"""

import os
import logging
from aion_core.database.supabase_reader import fetch_strategy_stats

logger = logging.getLogger("AION")

MIN_WINRATE = float(os.getenv("MIN_WINRATE", 0.5))
MIN_TRADES = int(os.getenv("MIN_TRADES", 10))
FALLBACK_STRATEGY = os.getenv("FALLBACK_STRATEGY", "mean_revert_chopbox")

def select_best_strategy(strategies_stats: list[dict]) -> str:
    if not strategies_stats:
        logger.warning("Geen strategie-statistieken beschikbaar. Gebruik fallback.")
        return FALLBACK_STRATEGY

    # Filter op voldoende trades en winrate
    filtered = [
        s for s in strategies_stats
        if s.get("total_trades", 0) >= MIN_TRADES and s.get("winrate", 0) >= MIN_WINRATE
    ]

    if not filtered:
        logger.warning("Geen strategieën voldeden aan de selectiecriteria. Gebruik fallback.")
        return FALLBACK_STRATEGY

    # Sorteer op winrate aflopend
    sorted_strats = sorted(filtered, key=lambda x: x["winrate"], reverse=True)
    best = sorted_strats[0]["strategy"]
    logger.info(f"Geselecteerde strategie: {best} (winrate={sorted_strats[0]['winrate']})")
    return best

if __name__ == "__main__":
    # Dummy test
    dummy_data = [
        {"strategy": "a", "winrate": 0.4, "total_trades": 5},
        {"strategy": "b", "winrate": 0.6, "total_trades": 12},
        {"strategy": "c", "winrate": 0.8, "total_trades": 20},
    ]
    print(select_best_strategy(dummy_data))