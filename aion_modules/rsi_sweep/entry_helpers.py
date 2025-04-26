
"""
📄 Bestand: rsi_sweep/entry_helpers.py
🔍 Aangepast: Trade result logging toegevoegd bij entry (dummy exitsimulatie voor nu).
"""

from aion_core.core.logging_engine import handle_trade_result_logging
from aion_core.utils.logger import log
import random  # Simuleert voor nu TP/SL hit (later vervangen door echte exit logica)

def detect_rsi_sweep(market_data):
    return market_data.get("rsi") < 30

def find_fvg(market_data):
    return market_data.get("fair_value_gap", False)

def enter_position(market_data, sl, tp):
    symbol = market_data.get("symbol", "UNKNOWN/UNKNOWN")
    entry_price = market_data.get("close")
    timestamp = market_data.get("timestamp")

    log(f"[ENTRY] Entry geplaatst! Entry Price: {entry_price}, SL: {sl}, TP: {tp}", level="info")

    # 🔵 Dummy exitsimulatie - random SL of TP geraakt (voor testdoeleinden)
    sl_hit = random.choice([True, False])
    tp_hit = not sl_hit
    exit_price = sl if sl_hit else tp

    # 🔵 Log trade result
    handle_trade_result_logging(symbol, entry_price, exit_price, sl_hit, tp_hit, timestamp)
