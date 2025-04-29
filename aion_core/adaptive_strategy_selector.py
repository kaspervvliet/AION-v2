"""
📄 Bestand: adaptive_strategy_selector.py
🔍 Doel: Dynamisch selecteren van een strategie op basis van marktomstandigheden
🧩 Gebruikt door: main_live.py, main_backtest.py, future Adaptive Engine
📦 Behoort tot: aion_core/
🧠 Verwacht implementatie van: strategy_pool_initializer, context data (ATR, ADX, volatility spikes)
"""

from aion_core.strategy_pool_initializer import select_strategy_by_type

def detect_market_regime(context: dict) -> str:
    atr = context.get('atr', 0)
    adx = context.get('adx', 0)
    in_range = context.get('in_range_market', False)
    volatility_spike = context.get('volatility_spike', False)

    if volatility_spike:
        return "breakout"
    elif atr < 0.5 and in_range:
        return "mean_revert"
    elif adx > 25:
        return "trend_follow"
    else:
        return "mean_revert"

def select_adaptive_strategy(context: dict):
    regime = detect_market_regime(context)
    strategy = select_strategy_by_type(regime)
    return strategy
