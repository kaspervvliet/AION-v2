
"""
📄 Bestand: aion_core/core/logging_engine.py
🔍 Doel: Event-driven logging handlers voor AION 2.0 naar Supabase.
🧩 Gebruikt door: Strategie-modules, main loop, bias updates
📦 Behoort tot: aion_core/core
🧠 Verwacht implementatie van: supabase_logger
"""

from aion_core.database.supabase_logger import (
    log_context,
    log_trade_result,
    log_htf_bias,
    log_equity_update,
    log_reflection
)

def handle_context_logging(symbol, sweep, fvg, timestamp):
    context_data = {
        "symbol": symbol,
        "sweep": sweep,
        "fvg": fvg,
        "timestamp": timestamp
    }
    log_context(context_data)

def handle_trade_result_logging(symbol, entry_price, exit_price, sl_hit, tp_hit, timestamp):
    trade_data = {
        "symbol": symbol,
        "entry_price": entry_price,
        "exit_price": exit_price,
        "stop_loss_hit": sl_hit,
        "take_profit_hit": tp_hit,
        "timestamp": timestamp
    }
    log_trade_result(trade_data)

def handle_bias_update_logging(symbol, htf_bias, timestamp):
    bias_data = {
        "symbol": symbol,
        "htf_bias": htf_bias,
        "timestamp": timestamp
    }
    log_htf_bias(bias_data)

def handle_equity_update_logging(balance, timestamp):
    equity_data = {
        "balance": balance,
        "timestamp": timestamp
    }
    log_equity_update(equity_data)

def handle_reflection_logging(reflection_text, timestamp):
    reflection_data = {
        "reflection": reflection_text,
        "timestamp": timestamp
    }
    log_reflection(reflection_data)
