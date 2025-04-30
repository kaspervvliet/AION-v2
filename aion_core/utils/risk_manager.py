
"""
📄 Bestand: risk_manager.py
🔍 Doel: Berekeningen van SL/TP, Risk/Reward en adaptieve risk levels
🧩 Gebruikt door: signal_engine, kernel, strategieën
📦 Behoort tot: aion_core/utils
🧠 Verwacht implementatie van: calculate_rr(), adjust_risk_level()
"""

def adjust_risk_level(drawdown_pct: float) -> float:
    """
    Past de risk per trade aan op basis van drawdown percentage.
    - >15% drawdown: reduceer naar 0.5%
    - >25% drawdown: naar 0.25%
    - <10% drawdown: herstel naar 1%
    """
    if drawdown_pct >= 25:
        return 0.0025  # 0.25%
    elif drawdown_pct >= 15:
        return 0.005   # 0.5%
    else:
        return 0.01    # 1%
