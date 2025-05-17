
""" 
📄 Bestand: supabase_logger.py
🔍 Doel: Supabase logging van context-, bias- en signaldata
🧩 Gebruikt door: strategy_executor, context_engine, web_entry
📦 Behoort tot: aion_core.database
🧠 Verwacht implementatie van: supabase Python client (v2)
"""

logger = logging.getLogger("AION")
import os
import datetime
import logging
from supabase import create_client, Client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    logger.warning("⚠️ SUPABASE_URL of SUPABASE_KEY ontbreekt — Supabase client gedeactiveerd")
    supabase: Client = None
else:
    logger.info(f"✅ SUPABASE_URL = {SUPABASE_URL}")
    logger.info(f"✅ SUPABASE_KEY = {SUPABASE_KEY[:8]}...(truncated)")
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def log_context_data(data: dict):
    if not supabase:
        logger.warning("❌ Geen Supabase client actief – context niet gelogd")
        return
    try:
        response = supabase.table("context").insert(data).execute()
        logger.info(f"✅ Context gelogd: {response}")
    except Exception as e:
        logger.error(f"❌ Fout bij upload_context: {e}")
