
"""
📄 Bestand: rsi_sweep/entry_helpers.py
🔍 Aangepast: Helper functies voor RSI sweep entries.
"""

def detect_rsi_sweep(market_data):
    # Dummy: detectie van sweep
    return market_data.get("rsi") < 30

def find_fvg(market_data):
    # Dummy: detectie van FVG
    return market_data.get("fair_value_gap", False)

def enter_position(market_data):
    print("[ENTRY] Entry geplaatst op basis van sweep + FVG.")
