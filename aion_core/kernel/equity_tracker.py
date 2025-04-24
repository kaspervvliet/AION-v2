
### aion_core/kernel/equity_tracker.py ###
# Equity logica per setup: RR, TP/SL, confluence, bias enz.

import datetime
from aion_core.supabase_client import insert  # bestaand Supabase script gebruiken

def track_equity(run_id: str, setup: dict, outcome: dict):
    equity_log = {
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "run_id": run_id,
        "rr": outcome.get("rr"),
        "tp_hit": outcome.get("tp_hit"),
        "sl_hit": outcome.get("sl_hit"),
        "bias": setup.get("bias"),
        "has_bos": setup.get("has_bos"),
        "has_fvg": setup.get("has_fvg"),
        "rsi": setup.get("rsi"),
        "context_snapshot": setup,
    }
    print("[EQUITY] Log:", equity_log)
    insert("equity_log", equity_log)
