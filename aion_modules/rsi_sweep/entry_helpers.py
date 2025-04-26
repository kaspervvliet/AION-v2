
"""
📄 Bestand: rsi_sweep/entry_helpers.py
🔍 Aangepast: SL en TP parameters toegevoegd aan entry.
"""

def detect_rsi_sweep(market_data):
    return market_data.get("rsi") < 30

def find_fvg(market_data):
    return market_data.get("fair_value_gap", False)

def enter_position(market_data, sl, tp):
    print(f"[ENTRY] Entry geplaatst! Entry Price: {market_data.get('close')}, SL: {sl}, TP: {tp}")
