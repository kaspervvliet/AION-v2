# 📄 Bestand: mute_controller.py
# Beheert mute-status — nu robuust: elke strategie krijgt altijd mute-status

import os
import datetime
from dateutil.parser import isoparse

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from supabase import create_client

def get_supabase():
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY") or os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    if not url or not key:
        raise EnvironmentError("SUPABASE_URL en SUPABASE_KEY (of SERVICE_ROLE_KEY) zijn vereist")
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

def activate_strategy(strategy_name: str):
    supabase = get_supabase()
    result = supabase.table("strategy_mute_state").upsert({
        "strategy": strategy_name,
        "is_muted": False,
        "mute_until": None,
        "updated_at": datetime.datetime.utcnow().isoformat()
    }).execute()
    return result

def is_strategy_muted(strategy_name: str) -> bool:
    supabase = get_supabase()
    rows = supabase.table("strategy_mute_state").select("is_muted, mute_until").eq("strategy", strategy_name).limit(1).execute()
    if not rows.data:
        return False
    row = rows.data[0]
    mute_until = row.get("mute_until")
    if row.get("is_muted") and mute_until:
        now = datetime.datetime.now(datetime.timezone.utc)
        return isoparse(mute_until) > now
    return False
