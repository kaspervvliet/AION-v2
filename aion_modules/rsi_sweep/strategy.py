
"""
📄 Bestand: rsi_sweep/strategy.py
🔍 Aangepast: Validate context vóór entries.
"""

from aion_core.utils.context_validator import validate_entry_context
from aion_modules.rsi_sweep.entry_helpers import detect_rsi_sweep, find_fvg, enter_position

def strategy_main(market_data):
    sweep_check = detect_rsi_sweep(market_data)
    fvg_check = find_fvg(market_data)

    context_data = {
        "sweep_confirmed": sweep_check,
        "valid_fvg_found": fvg_check
    }

    if validate_entry_context(context_data):
        enter_position(market_data)
    else:
        pass  # Geen entry
