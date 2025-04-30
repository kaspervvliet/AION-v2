# 📄 Bestand: supabase_reader.py
# Ophalen van recente strategielogs uit Supabase (nu lazy geladen)

import os
from supabase import create_client

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

def get_supabase():
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY") or os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    if not url or not key:
        raise EnvironmentError("SUPABASE_URL en SUPABASE_KEY (of SERVICE_ROLE_KEY) zijn vereist")
    return create_client(url, key)

def get_recent_logs(strategy_name: str, limit: int = 10):
    supabase = get_supabase()
    response = (
        supabase.table("strategy_logs")
        .select("strategy, bias, entry_type, sl_hit, tp_hit, timestamp")
        .eq("strategy", strategy_name)
        .order("timestamp", desc=True)
        .limit(limit)
        .execute()
    )
    return response.data
