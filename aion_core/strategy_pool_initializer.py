
"""
📄 Bestand: strategy_pool_initializer.py
🔍 Doel: Dynamisch laden van alle geldige strategieklassen
🧩 Gebruikt door: kernel.signal_engine, backtest_engine
📦 Behoort tot: aion_core
🧠 Verwacht implementatie van: StrategyInterface subclasses in aion_modules/strategies/
"""

import importlib.util
import os
import inspect
from aion_core.ai.strategy_interface import StrategyInterface

STRATEGY_PATH = os.path.join(os.path.dirname(__file__), "..", "aion_modules", "strategies")


def load_strategies():
    strategies = []

    for file in os.listdir(STRATEGY_PATH):
        if not file.endswith(".py") or file.startswith("__"):
            continue

        filepath = os.path.join(STRATEGY_PATH, file)
        modulename = file[:-3]
        spec = importlib.util.spec_from_file_location(modulename, filepath)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        for name, obj in inspect.getmembers(module, inspect.isclass):
            if issubclass(obj, StrategyInterface) and obj is not StrategyInterface:
                strategies.append(obj())

    return strategies


if __name__ == "__main__":
    for strat in load_strategies():
        print(f"Loaded: {strat.name} - {strat.get_metadata()['description']}")
