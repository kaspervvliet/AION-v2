"""
📄 Bestand: strategy_interface.py
🔍 Doel: Interface voor AI-strategieën in AION
🧩 Gebruikt door: ai/learning_agent, morph_engine
📦 Behoort tot: aion_core/ai/
🧠 Verwacht implementatie van: StrategyInterface (abc)
"""

from abc import ABC, abstractmethod
from typing import Any

class StrategyInterface(ABC):
    @abstractmethod
    def generate_signal(self, market_context: dict[str, Any]) -> dict[str, Any]:
        """
        Genereert een signaalobject op basis van huidige marktomstandigheden.
        Vereist: bevat minimaal entry/sl/tp.
        """
        pass

    @abstractmethod
    def calculate_rr(self, entry: float, sl: float, tp: float) -> float:
        """
        Berekent risk:reward-verhouding voor een trade.
        """
        pass

    @abstractmethod
    def should_enter(self, conditions: dict[str, bool]) -> bool:
        """
        Beoordeelt of aan alle entrycondities is voldaan.
        """
        pass
