"""
📄 Bestand: rsi_sweep.py
🔍 Doel: RSI sweep based mean-reversion strategie
🧩 Gebruikt door: Adaptive Engine, Signal Generator
📦 Behoort tot: aion_modules/strategies/
🧠 Verwacht implementatie van: RSI, Sweep detection, Risk/Reward calc
"""

def get_metadata():
    return {
        "name": "RSI Sweep",
        "description": "Speurt naar sweep setups onder RSI 30 om mean-reversion trades te plaatsen.",
        "type": "mean_revert",
        "timeframes": ["15m", "1h"]
    }

def generate_signal(context):
    # Vereist keys: context['rsi'], context['price_sweeps']
    if context.get('rsi', 100) < 30 and context.get('price_sweeps', False):
        return {
            "action": "buy",
            "confidence": 0.8,
            "sl_pct": 0.01,
            "tp_pct": 0.02
        }
    return None
