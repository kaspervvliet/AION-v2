"""
📄 Bestand: base_strategy.py
🔍 Doel: Abstracte basisklasse voor alle strategie-modules
🧩 Gebruikt door: Modules in aion_modules/
📦 Behoort tot: aion_core/
🧠 Verwacht implementatie van: is_entry(), get_metadata(), validate_config()
"""

from abc import ABC, abstractmethod

class BaseStrategy(ABC):
    def __init__(self, config, context):
        """
        config: dict met parameters zoals TF, SL/TP, inputs
        context: AIONContext met datafeed, accountinfo, alerts
        """
        self.config = config
        self.context = context

    @abstractmethod
    def is_entry(self, candle_data):
        """Retourneer True/False voor entry-signaal op basis van candle_data."""
        pass

    @abstractmethod
    def get_metadata(self):
        """Retourneer dict met naam, versie, inputs, outputs voor UI/Supabase."""
        pass

    def validate_config(self):
        """Optioneel: valideer of config de vereiste velden bevat."""
        required = ["symbol", "timeframe", "sl", "tp"]
        for key in required:
            if key not in self.config:
                raise ValueError(f"Missing required config key: {key}")
        return True