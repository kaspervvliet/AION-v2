"""
📄 Bestand: mean_revert_chopbox.py
🔍 Doel: Mean-reversion trading in consolidatie (chopbox) markten
🧩 Gebruikt door: Adaptive Engine
📦 Behoort tot: aion_modules/strategies/
🧠 Verwacht implementatie van: Range detectie, Volatility filters
"""

def get_metadata():
    return {
        "name": "Mean Revert Chopbox",
        "description": "Trade tussen support en resistance binnen ranges.",
        "type": "mean_revert",
        "timeframes": ["15m", "1h"]
    }

def generate_signal(context):
    if context.get('in_range_market') and context.get('price_near_support'):
        return {
            "action": "buy",
            "confidence": 0.75,
            "sl_pct": 0.012,
            "tp_pct": 0.024
        }
    return None
