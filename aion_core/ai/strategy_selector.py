# 📄 Bestand: strategy_selector.py
# Selecteert de best passende strategie op basis van validatie

from typing import List, Dict, Optional
from aion_core.ai.strategy_validator import available_strategies, StrategyInterface

def select_best_strategy(logs: List[Dict]) -> Optional[StrategyInterface]:
    """
    Roept alle strategieën aan met logs, retourneert eerste geldige match.
    Later uitbreidbaar met scoringsmodel of GPT.
    """
    for strategy in available_strategies:
        try:
            if strategy.validate_market(logs):
                return strategy
        except Exception as e:
            print(f"⚠️ Validatie fout bij {strategy.name}: {e}")
    return None
