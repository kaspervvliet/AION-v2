"""
📄 Bestand: confidence_model.py
🔍 Doel: Genereert confidence-score op basis van SMC-input
🧩 Gebruikt door: reflectie, evaluatie-engine
📦 Behoort tot: aion_core/kernel/
🧠 Verwacht implementatie van: logica voor inputscores
"""

import logging
from typing import Dict

logger = logging.getLogger("AION")

def get_confidence_score(factors: Dict[str, bool]) -> int:
    """
    Berekent een confidence score op basis van boolean input.
    Elke True telt als +1.
    """
    if not factors:
        logger.warning("Lege input voor confidence score.")
        return 0

    score = sum(1 for v in factors.values() if v)
    logger.info(f"Confidence score: {score} (factors: {factors})")
    return score

if __name__ == "__main__":
    # Dummy tests
    print(get_confidence_score({"bias": True, "fvg": True, "choch": False}))
    print(get_confidence_score({"bias": False, "breaker": False}))
    print(get_confidence_score({}))
