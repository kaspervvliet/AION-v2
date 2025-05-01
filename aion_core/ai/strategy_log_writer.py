# 📄 Bestand: strategy_log_writer.py
# Insert dummy logs in de Supabase strategy_logs tabel (voor testdoeleinden)

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
    key = os.getenv("SUPABASE_KEY") or os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    if not url or not key:
        raise EnvironmentError("SUPABASE_URL en SUPABASE_KEY (of SERVICE_ROLE_KEY) zijn vereist")
    return create_client(url, key)

def insert_strategy_log(strategy_name: str, bias='bullish', entry_type='FVG', sl_hit=False, tp_hit=True):
    supabase = get_supabase()
    result = supabase.table("strategy_logs").insert({
        "strategy": strategy_name,
        "bias": bias,
        "entry_type": entry_type,
        "sl_hit": sl_hit,
        "tp_hit": tp_hit,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }).execute()
    return result
