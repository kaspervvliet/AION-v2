"""
📄 Bestand: supabase_client.py
🔍 Doel: Initialiseert de Supabase client voor alle DB interacties
🧩 Gebruikt door: supabase_reader, supabase_writer
📦 Behoort tot: aion_core/database/
🧠 Verwacht implementatie van: client-init via .env
"""

import os
import logging
from supabase import create_client, Client

logger = logging.getLogger("AION")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client | None = None

if not SUPABASE_URL or not SUPABASE_KEY:
    logger.warning("⚠️ SUPABASE config ontbreekt — verbinding niet opgezet.")
else:
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        logger.info("🔌 Supabase client aangemaakt")
    except Exception as e:
        logger.error(f"❌ Fout bij Supabase client init: {e}")

if __name__ == "__main__":
    if supabase:
        res = supabase.table("aion_logs").select("id").limit(1).execute()
        print("✅ Verbonden met Supabase:", res.status_code)
    else:
        print("❌ Geen actieve Supabase-client. Check env.")
