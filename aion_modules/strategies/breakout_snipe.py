"""
📄 Bestand: breakout_snipe.py
🔍 Doel: Trade early breakouts met kleine risico's
🧩 Gebruikt door: Adaptive Engine
📦 Behoort tot: aion_modules/strategies/
🧠 Verwacht implementatie van: Volatility spike detectie
"""

def get_metadata():
    return {
        "name": "Breakout Snipe",
        "description": "Snipes explosieve breakouts bij hoge volatility readings.",
        "type": "breakout",
        "timeframes": ["15m", "1h"]
    }

def generate_signal(context):
    if context.get('volatility_spike') and context.get('price_breakout_detected'):
        return {
            "action": "buy",
            "confidence": 0.9,
            "sl_pct": 0.02,
            "tp_pct": 0.04
        }
    return None
