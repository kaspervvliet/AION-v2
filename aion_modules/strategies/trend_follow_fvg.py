"""
📄 Bestand: trend_follow_fvg.py
🔍 Doel: Trend-following strategie via Fair Value Gap + BOS detectie
🧩 Gebruikt door: Adaptive Engine
📦 Behoort tot: aion_modules/strategies/
🧠 Verwacht implementatie van: FVG, BOS, Trend strength
"""

def get_metadata():
    return {
        "name": "Trend Follow FVG",
        "description": "Volgt sterke trends na FVG en Break of Structure (BOS).",
        "type": "trend_follow",
        "timeframes": ["15m", "1h", "4h"]
    }

def generate_signal(context):
    if context.get('fvg_detected') and context.get('bos_confirmed'):
        return {
            "action": "buy",
            "confidence": 0.85,
            "sl_pct": 0.015,
            "tp_pct": 0.03
        }
    return None
