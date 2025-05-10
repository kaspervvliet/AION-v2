"""
📄 Bestand: mtf_bias_checker.py
🔍 Doel: Checkt of bias consistent is over meerdere timeframes
🧩 Gebruikt door: pre-analyse, signal_engine
📦 Behoort tot: aion_core/knowledge/
🧠 Verwacht implementatie van: is_bias_consistent()
"""

from typing import Dict

def is_bias_consistent(biases: Dict[str, str]) -> bool:
    """
    Geeft True als alle biaswaarden identiek zijn over timeframes.
    """
    return len(set(biases.values())) == 1

if __name__ == "__main__":
    tf_bias = {"15m": "long", "1h": "long", "4h": "long"}
    print("✅ Bias consistent:", is_bias_consistent(tf_bias))

    mixed_bias = {"15m": "long", "1h": "short"}
    print("❌ Bias inconsistent:", is_bias_consistent(mixed_bias))
