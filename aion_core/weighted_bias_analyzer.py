"""
📄 Bestand: weighted_bias_analyzer.py
🔍 Doel: Multi-Timeframe Bias bepalen via gewogen analyse (1D, 4H, 1H)
🧩 Gebruikt door: strategieën
📦 Behoort tot: aion_core/
🧠 Verwacht implementatie van: candle data per timeframe
"""

def determine_bias(candles):
    """Bepaal bias (bullish, bearish, neutral) van candles."""
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

def calculate_weighted_bias(daily_candles, fourh_candles, oneh_candles, threshold=0.5):
    """Combineer biases van meerdere timeframes tot één master bias."""
    weights = {
        "1D": 0.5,
        "4H": 0.3,
        "1H": 0.2
    }

    biases = {
        "1D": determine_bias(daily_candles),
        "4H": determine_bias(fourh_candles),
        "1H": determine_bias(oneh_candles)
    }

    score = 0

    for tf, bias in biases.items():
        if bias == "bullish":
            score += weights[tf]
        elif bias == "bearish":
            score -= weights[tf]

    if score >= threshold:
        return "bullish"
    elif score <= -threshold:
        return "bearish"
    else:
        return "neutral"