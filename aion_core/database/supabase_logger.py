
""" 
📄 Bestand: supabase_logger.py
🔍 Doel: Supabase logging van context-, bias- en signaldata
🧩 Gebruikt door: strategy_executor, context_engine, web_entry
📦 Behoort tot: aion_core.database
🧠 Verwacht implementatie van: supabase Python client (v2)
"""

import os
import datetime
from supabase import create_client, Client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("⚠️ SUPABASE_URL of SUPABASE_KEY ontbreekt — Supabase client gedeactiveerd")
    supabase: Client = None
else:
    print(f"✅ SUPABASE_URL = {SUPABASE_URL}")
    print(f"✅ SUPABASE_KEY = {SUPABASE_KEY[:8]}...(truncated)")
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def log_context_data(data: dict):
    if not supabase:
        print("❌ Geen Supabase client actief – context niet gelogd")
        return
    try:
        response = supabase.table("context").insert(data).execute()
        print(f"✅ Context gelogd: {response}")
    except Exception as e:
        print(f"❌ Fout bij upload_context: {e}")
