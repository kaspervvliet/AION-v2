
"""
📄 Bestand: mtf_bias_checker.py
🔍 Doel: Checkt of bias consistent is over meerdere timeframes en logt resultaat
🧩 Gebruikt door: pre-analyse, signal_engine
📦 Behoort tot: aion_core/knowledge/
🧠 Verwacht implementatie van: log_if_bias_changed
"""

from typing import Dict
from aion_core.utils.bias_logger import log_if_bias_changed

def is_bias_consistent(biases: Dict[str, str], symbol: str = "", source: str = "mtf_bias_checker") -> bool:
    """
    Geeft True als alle biaswaarden identiek zijn over timeframes.
    Logt consistentie-status naar bias_tracker.
    """
    consistent = len(set(biases.values())) == 1
    bias_value = "consistent" if consistent else "inconsistent"

    if symbol:
        log_if_bias_changed(symbol=symbol, timeframe="mtf", bias=bias_value, source=source)

    return consistent

if __name__ == "__main__":
    tf_bias = {"15m": "long", "1h": "long", "4h": "long"}
    print("✅ Bias consistent:", is_bias_consistent(tf_bias, symbol="TEST/LOG"))

    mixed_bias = {"15m": "long", "1h": "short"}
    print("❌ Bias inconsistent:", is_bias_consistent(mixed_bias, symbol="TEST/LOG"))
