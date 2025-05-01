# 📄 Bestand: strategy_validator.py
# Dynamische loader voor strategieën + debug output

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

    print("🔍 Strategieën laden uit:", base_dir)

    for file in os.listdir(base_dir):
        if file.endswith(".py") and not file.startswith("__"):
            module_name = file.replace(".py", "")
            full_path = f"{STRATEGY_PATH}.{module_name}"

            try:
                mod = importlib.import_module(full_path)
                for _, obj in inspect.getmembers(mod, inspect.isclass):
                    if issubclass(obj, StrategyInterface) and obj is not StrategyInterface:
                        instance = obj()
                        print(f"✅ Strategie geladen: {obj.__name__} (name: '{instance.name}')")
                        strategies.append(instance)
            except Exception as e:
                print(f"⚠️ Kan {full_path} niet laden: {e}")
    return strategies

available_strategies = load_strategies()
