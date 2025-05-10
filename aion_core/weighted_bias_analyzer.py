"""
📄 Bestand: weighted_bias_analyzer.py
🔍 Doel: Bepaalt gecombineerde bias op basis van HTF-gewichten
🧩 Gebruikt door: kernel, strategieën, reflectie
📦 Behoort tot: aion_core/
🧠 Verwacht implementatie van: logger
"""

from aion_core.utils.logger import logger


def calculate_weighted_bias(bias_inputs: dict, weights: dict = None) -> str:
    """
    bias_inputs: {"4h": "bullish", "1d": "bearish"}
    weights: {"4h": 0.6, "1d": 0.4}
    """
    if not bias_inputs:
        logger.warning("⚠️ Geen biases meegegeven aan weighted_bias_analyzer")
        return "neutral"

    weights = weights or {k: 1 for k in bias_inputs}
    total = sum(weights.values())

    if total == 0:
        logger.warning("⚠️ Ongeldige bias-gewichten (totaal = 0)")
        return "neutral"

    score = 0
    for tf, bias in bias_inputs.items():
        w = weights.get(tf, 1)
        if bias == "bullish":
            score += w
        elif bias == "bearish":
            score -= w
        # "neutral" = 0

    norm_score = score / total

    if norm_score > 0.25:
        return "bullish"
    elif norm_score < -0.25:
        return "bearish"
    else:
        logger.info("ℹ️ Bias-score neutraal")
        return "neutral"
