"""
📄 Bestand: loader.py
🔍 Doel: Dynamisch laden van strategie-modules via importlib
🧩 Gebruikt door: main.py, backtest-engine
📦 Behoort tot: aion_core/
"""

import importlib.util
import os
import sys
from pathlib import Path

MODULES_PATH = Path("aion_modules")

class StrategyLoader:
    def __init__(self, modules_path=MODULES_PATH):
        self.modules_path = modules_path

    def list_available_strategies(self):
        """Retourneer een lijst van beschikbare strategie mappen."""
        return [d.name for d in self.modules_path.iterdir() if d.is_dir() and (d / "strategy.py").exists()]

    def load_strategy(self, strategy_name):
        """Laad de strategy.py module uit de opgegeven submap."""
        strategy_path = self.modules_path / strategy_name / "strategy.py"
        if not strategy_path.exists():
            raise FileNotFoundError(f"Strategy '{strategy_name}' niet gevonden.")

        module_name = f"aion_modules.{strategy_name}.strategy"
        spec = importlib.util.spec_from_file_location(module_name, strategy_path)
        strategy_module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = strategy_module
        spec.loader.exec_module(strategy_module)
        return strategy_module