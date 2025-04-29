
"""
📄 Bestand: supabase_performance_helper.py
🔍 Doel: Upload van uitgevoerde trades naar Supabase (equity_log + signal update)
🧩 Gebruikt door: PerformanceTracker, main_live, backtest
📦 Behoort tot: aion_core/extensions
🧠 Verwacht implementatie van: supabase_writer module
"""

from aion_core.extensions.supabase_writer import upload_record, update_record
from datetime import datetime

def upload_trade_to_equity_log(trade: dict):
    """
    Verwacht:
    {
        "timestamp": iso-format str,
        "symbol": "SOL/USDT",
        "rr": float,
        "result": "win" / "loss",
        "balance": float (optioneel)
    }
    """
    try:
        upload_record("equity_log", trade)
    except Exception as e:
        print(f"[Supabase Performance Helper ERROR] Equity log upload faalde: {e}")

def update_signal_outcome(signal_id: str, updates: dict):
    """
    Update een bestaande signal entry met resultaatinfo
    updates = {
        "result": "win",
        "duration": 84,
        "execution_price": 87.3,
        "execution_time": 174582XXXX
    }
    """
    try:
        update_record("signals", "id", signal_id, updates)
    except Exception as e:
        print(f"[Supabase Performance Helper ERROR] Signal update faalde: {e}")
