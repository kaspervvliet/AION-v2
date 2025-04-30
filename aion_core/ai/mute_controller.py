# 📄 Bestand: mute_controller.py
# Leest en schrijft mute-status naar Supabase

import os
import datetime
from supabase import create_client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def mute_strategy(strategy_name: str, hours: int = 4):
    until = datetime.datetime.utcnow() + datetime.timedelta(hours=hours)
    result = supabase.table("strategy_mute_state").upsert({
        "strategy": strategy_name,
        "is_muted": True,
        "mute_until": until.isoformat(),
        "updated_at": datetime.datetime.utcnow().isoformat()
    }).execute()
    return result

def is_strategy_muted(strategy_name: str) -> bool:
    row = supabase.table("strategy_mute_state").select("is_muted, mute_until").eq("strategy", strategy_name).single().execute()
    if not row.data:
        return False
    mute_until = row.data.get("mute_until")
    if row.data.get("is_muted") and mute_until:
        return datetime.datetime.fromisoformat(mute_until) > datetime.datetime.utcnow()
    return False
