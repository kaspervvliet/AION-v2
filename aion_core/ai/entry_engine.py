# 📄 Bestand: entry_engine.py
# Genereert entry, SL, TP en risk:reward op basis van gekozen strategie en context

from typing import Dict, Tuple
import random

def generate_entry_payload(strategy_name: str) -> Dict:
    """
    Simuleert entry-logica. In productie vervang je dit per strategie.
    Voorbeeldwaarden nu statisch/random.
    """
    entry_price = round(random.uniform(100, 120), 2)
    stop_loss = round(entry_price - random.uniform(1, 3), 2)
    take_profit = round(entry_price + random.uniform(2, 6), 2)

    rr = round((take_profit - entry_price) / max((entry_price - stop_loss), 0.01), 2)

    return {
        "strategy": strategy_name,
        "entry": entry_price,
        "stop_loss": stop_loss,
        "take_profit": take_profit,
        "risk_reward_ratio": rr
    }
