"""
📄 Bestand: volatility_analyzer.py
🔍 Doel: Meet recente volatiliteit als input voor entryfilter
🧩 Gebruikt door: strategieën, kernel, bias tools
📦 Behoort tot: aion_core/indicators/
🧠 Verwacht implementatie van: logger
"""

from aion_core.utils.logger import logger


def compute_volatility(candles: list, period: int = 14) -> float:
    if not candles or len(candles) < period:
        logger.warning("⚠️ Onvoldoende candles voor volatiliteitsanalyse")
        return 0.0

    highs = [c["high"] for c in candles[-period:]]
    lows = [c["low"] for c in candles[-period:]]

    ranges = [h - l for h, l in zip(highs, lows)]
    mean_range = sum(ranges) / len(ranges)

    if mean_range < 0.0001:
        logger.info("ℹ️ Zeer lage volatiliteit gemeten")
    return round(mean_range, 6)
