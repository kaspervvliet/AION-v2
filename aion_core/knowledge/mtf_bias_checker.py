"""
📄 Bestand: mtf_bias_checker.py
🔍 Doel: Bepalen of higher timeframe (HTF) en lower timeframe (LTF) biases aligned zijn
🧩 Gebruikt door: alle strategie modules
📦 Behoort tot: aion_core/
🧠 Verwacht implementatie van: candle data per timeframe
"""

def determine_bias(candles):
    """Bepaal bias (bullish, bearish, neutraal) op basis van simpele swing analysis."""
    if len(candles) < 2:
        return "neutral"

    recent_close = candles[-1][4]
    previous_close = candles[-2][4]

    if recent_close > previous_close:
        return "bullish"
    elif recent_close < previous_close:
        return "bearish"
    else:
        return "neutral"

def is_bias_aligned(htf_candles, ltf_candles):
    """Controleer of biases aligned zijn."""
    htf_bias = determine_bias(htf_candles)
    ltf_bias = determine_bias(ltf_candles)

    if htf_bias == ltf_bias and htf_bias in ["bullish", "bearish"]:
        return True
    return False