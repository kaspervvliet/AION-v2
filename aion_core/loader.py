"""
📄 Bestand: loader.py
🔍 Doel: Dynamisch laden van strategie-modules via importlib
🧩 Gebruikt door: main.py, backtest-engine
📦 Behoort tot: aion_core/
"""

import importlib.util
import os
import sys
import logging
from pathlib import Path
from types import ModuleType
from typing import List

logger = logging.getLogger("AION")

MODULES_PATH = Path("aion_modules")

class StrategyLoader:
    def __init__(self, modules_path: Path = MODULES_PATH):
        self.modules_path = modules_path

    def list_available_strategies(self) -> List[str]:
        """Retourneer een lijst van beschikbare strategie mappen."""
        return [d.name for d in self.modules_path.iterdir() if d.is_dir() and (d / "strategy.py").exists()]

    def load_strategy(self, strategy_name: str) -> ModuleType:
        """Laad de strategy.py module uit de opgegeven submap."""
        strategy_path = self.modules_path / strategy_name / "strategy.py"
        if not strategy_path.exists():
            logger.error(f"❌ Strategie '{strategy_name}' niet gevonden in {strategy_path}")
            raise FileNotFoundError(f"Strategy '{strategy_name}' niet gevonden.")

        module_name = f"aion_modules.{strategy_name}.strategy"
        spec = importlib.util.spec_from_file_location(module_name, strategy_path)
        strategy = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = strategy
        spec.loader.exec_module(strategy)
        logger.info(f"✅ Strategie geladen: {strategy_name}")
        return strategy

if __name__ == "__main__":
    loader = StrategyLoader()
    print("📦 Beschikbare strategieën:", loader.list_available_strategies())
    try:
        strat = loader.load_strategy("example")
        print("🎯 Strategie geladen:", strat)
    except Exception as e:
        print(f"⚠️ Fout bij laden: {e}")
