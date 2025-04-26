
"""
📄 Bestand: rsi_sweep/strategy.py
🔍 Aangepast: Structure Awareness toegevoegd vóór context validatie en dynamic risk.
"""

from aion_core.utils.context_validator import validate_entry_context
from aion_core.utils.risk_manager import calculate_sl, calculate_tp
from aion_core.knowledge.structure_awareness import should_block_entry
from aion_modules.rsi_sweep.entry_helpers import detect_rsi_sweep, find_fvg, enter_position
from aion_core.utils.logger import log  # Zorg dat deze bestaat voor nette logging

def strategy_main(market_data):
    entry_price = market_data.get("close")  # Stel entry price gelijk aan laatste sluitprijs
    market_structure = {
        "last_swing_low": market_data.get("last_swing_low"),
        "last_swing_high": market_data.get("last_swing_high")
    }

    # 🔵 Stap 1: Structure Awareness Check vóór alles
    if should_block_entry(market_data):
        log("Entry geblokkeerd: structureel risico gedetecteerd.", level="warning")
        return

    # 🔵 Stap 2: Sweep + FVG validatie
    sweep_check = detect_rsi_sweep(market_data)
    fvg_check = find_fvg(market_data)

    context_data = {
        "sweep_confirmed": sweep_check,
        "valid_fvg_found": fvg_check
    }

    if validate_entry_context(context_data):
        sl = calculate_sl(entry_price, market_structure, direction="long")
        tp = calculate_tp(entry_price, sl, risk_reward_ratio=2.0, direction="long")
        enter_position(market_data, sl=sl, tp=tp)
    else:
        log("Entry niet genomen: sweep/FVG validatie gefaald.", level="info")
