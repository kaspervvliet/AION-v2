"""
📄 Bestand: market_structure.py
🔍 Doel: Verbeterde markt analyse inclusief HTF bias filtering
🧩 Gebruikt door: web_entry.py, kernel.py
📦 Behoort tot: AION v2
🧠 Verwacht implementatie van: Smart Money Concepts interpretatie
"""

def analyse_market(candle, bias="neutral"):
    setup = {
        "structure": "unknown",
        "confidence": 0,
        "bias_filter_passed": True,
    }

    try:
        if candle['close'] > candle['open']:
            setup["structure"] = "bullish"
        elif candle['close'] < candle['open']:
            setup["structure"] = "bearish"
        else:
            setup["structure"] = "neutral"

        setup["confidence"] = abs(float(candle['close']) - float(candle['open']))

        if bias == "bullish" and setup["structure"] != "bullish":
            setup["bias_filter_passed"] = False
        if bias == "bearish" and setup["structure"] != "bearish":
            setup["bias_filter_passed"] = False

    except Exception:
        setup["structure"] = "error"
        setup["confidence"] = 0
        setup["bias_filter_passed"] = False

    return setup