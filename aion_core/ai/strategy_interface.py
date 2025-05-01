# 📄 Bestand: strategy_interface.py
# Abstracte interface voor alle strategieën in AION

from typing import List, Dict
from abc import ABC, abstractmethod

class StrategyInterface(ABC):
    name: str

    @abstractmethod
    def validate_market(self, recent_logs: List[Dict]) -> bool:
        """
        Return True als deze strategie van toepassing is op de gegeven logs.
        """
        pass
