import datetime

def log_setup(setup: dict, confidence: float, status: str):
    print(f"[MEMORY] Setup logged @ {datetime.datetime.now().isoformat()} → {status} ({confidence})")
    # Supabase insert can be added here

def log_outcome(setup: dict, outcome: dict):
    print(f"[MEMORY] Outcome: TP={outcome.get('tp_hit')}, SL={outcome.get('sl_hit')}, RR={outcome.get('rr')}")
    # Supabase insert can be added here
