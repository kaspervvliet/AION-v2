"""
📄 Bestand: base_strategy.py
🔍 Doel: Abstracte basisstrategie voor AION-modules
🧩 Gebruikt door: Alle strategie-implementaties (CHoCH, FVG, etc.)
📦 Behoort tot: /
🧠 Verwacht implementatie van: StrategyInterface-methodes
"""

import logging
from abc import ABC, abstractmethod
from typing import Any

logger = logging.getLogger("AION")

class BaseStrategy(ABC):
    """
    Abstracte strategieklasse voor setup-validatie en signaalgeneratie.
    Elke subclass moet minimaal generate_signal() implementeren.
    """

    @abstractmethod
    def generate_signal(self, market_context: dict[str, Any]) -> dict:
        """
        Genereert een trading signaal gebaseerd op de huidige context.
        """
        pass

    def should_enter(self, conditions: dict[str, bool]) -> bool:
        """
        Geeft aan of de entrycondities geldig zijn.
        """
        valid = all(conditions.values())
        if not valid:
            logger.debug(f"Entry afgewezen: {conditions}")
        return valid

    def calculate_rr(self, entry: float, sl: float, tp: float) -> float:
        """
        Berekent risk:reward ratio.
        """
        if sl == entry:
            logger.warning("SL en entry zijn gelijk — R:R deling door nul voorkomen.")
            return 0.0
        return abs((tp - entry) / (entry - sl))