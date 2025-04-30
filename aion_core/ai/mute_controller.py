# 📄 Bestand: mute_controller.py
# Leest en schrijft mute-status naar Supabase (nu lazy geladen, werkt met .env)

import os
import datetime

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from supabase import create_client

def get_supabase():
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    if not url or not key:
        raise EnvironmentError("SUPABASE_URL en SUPABASE_KEY zijn vereist")
    return create_client(url, key)

def mute_strategy(strategy_name: str, hours: int = 4):
    supabase = get_supabase()
    until = datetime.datetime.utcnow() + datetime.timedelta(hours=hours)
    result = supabase.table("strategy_mute_state").upsert({
        "strategy": strategy_name,
        "is_muted": True,
        "mute_until": until.isoformat(),
        "updated_at": datetime.datetime.utcnow().isoformat()
    }).execute()
    return result

def is_strategy_muted(strategy_name: str) -> bool:
    supabase = get_supabase()
    row = supabase.table("strategy_mute_state").select("is_muted, mute_until").eq("strategy", strategy_name).single().execute()
    if not row.data:
        return False
    mute_until = row.data.get("mute_until")
    if row.data.get("is_muted") and mute_until:
        return datetime.datetime.fromisoformat(mute_until) > datetime.datetime.utcnow()
    return False
