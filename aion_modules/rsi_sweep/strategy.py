
"""
📄 Bestand: rsi_sweep/strategy.py
🔍 Aangepast: Event-driven context logging toegevoegd + adaptive risk management.
"""

from aion_core.utils.context_validator import validate_entry_context
from aion_core.utils.risk_manager import calculate_sl, calculate_tp
from aion_core.knowledge.structure_awareness import should_block_entry
from aion_core.indicators.volatility_analyzer import calculate_atr, assess_volatility, adjust_risk_parameters
from aion_core.core.logging_engine import handle_context_logging
from aion_modules.rsi_sweep.entry_helpers import detect_rsi_sweep, find_fvg, enter_position
from aion_core.utils.logger import log  # Zorg dat deze bestaat

def strategy_main(market_data, candle_history):
    entry_price = market_data.get("close")
    symbol = market_data.get("symbol", "UNKNOWN/UNKNOWN")
    market_structure = {
        "last_swing_low": market_data.get("last_swing_low"),
        "last_swing_high": market_data.get("last_swing_high")
    }
    timestamp = market_data.get("timestamp")

    # 🔵 Stap 1: Structure Awareness Check
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

    # 🔵 Stap 3: Context Logging
    handle_context_logging(symbol, sweep=sweep_check, fvg=fvg_check, timestamp=timestamp)

    if validate_entry_context(context_data):
        # 🔵 Stap 4: SL/TP berekenen
        sl = calculate_sl(entry_price, market_structure, direction="long")
        tp = calculate_tp(entry_price, sl, risk_reward_ratio=2.0, direction="long")

        # 🔵 Stap 5: Volatility Analyse
        atr = calculate_atr(candle_history, period=14)
        volatility_label = assess_volatility(atr, high_threshold=0.02, low_threshold=0.005)
        adjusted_sl, adjusted_tp = adjust_risk_parameters(sl, tp, volatility_label)

        log(f"Volatility assessment: {volatility_label}. SL/TP aangepast.", level="info")

        # 🔵 Stap 6: Entry openen met aangepaste risk
        enter_position(market_data, sl=adjusted_sl, tp=adjusted_tp)
    else:
        log("Entry niet genomen: sweep/FVG validatie gefaald.", level="info")
