"""
📄 Bestand: analyse_market.py
🔍 Doel: Marktsetup analyseren inclusief BOS/CHoCH checks
🧩 Gebruikt door: kernel.py
📦 Behoort tot: AION Core
🧠 Verwacht candles, bias, confidence als input
"""

from aion_modules.analyse_bos_choc import analyse_bos_choc
import logging

logger = logging.getLogger("AION")

def analyse_market(setup):
    """
    Verwerkt setup info + BOS/CHoCH analyse.

    Args:
        setup (dict): Setup dict met o.a. candles, bias, confidence

    Returns:
        dict: analyse resultaten
    """
    candles = setup.get("candles", [])
    bias = setup.get("bias", "bullish")
    confidence = setup.get("confidence", 0)

    bos_choc = analyse_bos_choc(candles, direction=bias)

    # Logging voor AION Growth Insights
    logger.info(f"[MARKET] BOS gedetecteerd: {bos_choc['bos']}")
    logger.info(f"[MARKET] CHoCH gedetecteerd: {bos_choc['choc']}")

    return {
        "bias": bias,
        "confidence": confidence,
        "bos": bos_choc["bos"],
        "choc": bos_choc["choc"]
    }