"""
📄 Bestand: strategy_pool_initializer.py
🔍 Doel: Laadt alle strategy-klassen die StrategyInterface implementeren
🧩 Gebruikt door: morph_engine, strategy_tester
📦 Behoort tot: aion_core/
🧠 Verwacht implementatie van: StrategyInterface, importlib, inspect
"""

import importlib.util
import inspect
import logging
import os
from pathlib import Path
from aion_core.ai.strategy_interface import StrategyInterface

logger = logging.getLogger("AION")

STRATEGY_PATH = Path("aion_modules/strategies")

def load_strategies() -> list:
    strategies = []
    for file in STRATEGY_PATH.rglob("*.py"):
        module_name = file.stem
        spec = importlib.util.spec_from_file_location(module_name, file)
        module = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(module)
        except Exception as e:
            logger.error(f"❌ Laden mislukt voor {file}: {e}")
            continue

        for _, obj in inspect.getmembers(module, inspect.isclass):
            if issubclass(obj, StrategyInterface) and obj is not StrategyInterface:
                strategies.append(obj())
                logger.info(f"✅ Strategy geladen: {obj.__name__} uit {file}")
    return strategies

if __name__ == "__main__":
    pool = load_strategies()
    print(f"🔍 Strategieën geladen: {len(pool)}")
    for strat in pool:
        print(f" - {strat.__class__.__name__}")
