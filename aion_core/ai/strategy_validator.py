# 📄 Bestand: strategy_validator.py
# Dynamische loader voor alle strategy validators in aion_modules/strategies/

from typing import List, Dict, Type
import importlib
import os
import inspect
from aion_core.ai.strategy_interface import StrategyInterface

STRATEGY_PATH = "aion_modules.strategies"

def load_strategies() -> List[StrategyInterface]:
    strategies = []
    base_dir = os.path.join(os.path.dirname(__file__), "../../aion_modules/strategies")
    base_dir = os.path.abspath(base_dir)

    for file in os.listdir(base_dir):
        if file.endswith(".py") and not file.startswith("__"):
            module_name = file.replace(".py", "")
            full_path = f"{STRATEGY_PATH}.{module_name}"

            try:
                mod = importlib.import_module(full_path)
                for _, obj in inspect.getmembers(mod, inspect.isclass):
                    if issubclass(obj, StrategyInterface) and obj is not StrategyInterface:
                        strategies.append(obj())
            except Exception as e:
                print(f"⚠️ Kan {full_path} niet laden: {e}")
    return strategies

available_strategies = load_strategies()
