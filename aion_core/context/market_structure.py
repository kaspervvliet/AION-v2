"""
📄 Bestand: market_structure.py
🔍 Doel: Detecteert BOS/CHoCH structuurwijziging uit prijsdata
🧩 Gebruikt door: strategieën, kernel, analyse
📦 Behoort tot: aion_core/context/
🧠 Verwacht implementatie van: numpy
"""

import numpy as np
from aion_core.utils.logger import logger


def detect_market_structure(candles: list) -> dict:
    if not candles or len(candles) < 10:
        logger.warning("⚠️ Onvoldoende candles voor structuurdetectie.")
        return {}

    highs = np.array([c["high"] for c in candles])
    lows = np.array([c["low"] for c in candles])

    try:
        last_high = highs[-1]
        prev_high = highs[-5]
        last_low = lows[-1]
        prev_low = lows[-5]

        structure = {}

        if last_high > prev_high:
            structure["bos_up"] = True
        if last_low < prev_low:
            structure["bos_down"] = True

        if last_high < prev_high and last_low > prev_low:
            structure["choc"] = True

        return structure

    except Exception as e:
        logger.error(f"❌ Structuurdetectie mislukt: {e}")
        return {}
