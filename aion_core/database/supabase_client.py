"""
📄 Bestand: supabase_client.py
🔍 Doel: Initialiseert de Supabase client voor alle DB interacties
🧩 Gebruikt door: supabase_reader, supabase_writer
📦 Behoort tot: aion_core/database/
🧠 Verwacht implementatie van: client-init via omgeving (Render)
"""

import os
import logging
from supabase import create_client, Client

logger = logging.getLogger("AION")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    logger.warning("⚠️ SUPABASE_URL of SUPABASE_KEY ontbreekt — Supabase client gedeactiveerd")
    supabase = None
else:
    try:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        logger.info("🔌 Supabase client aangemaakt")
    except Exception as e:
        logger.error(f"❌ Supabase connectie mislukt: {e}")
        supabase = None

if __name__ == "__main__":
    if supabase:
        try:
            res = supabase.table("aion_logs").select("id").limit(1).execute()
            print("✅ Verbonden met Supabase:", res.status_code)
        except Exception as e:
            print("❌ Supabase testquery gefaald:", e)
    else:
        print("⚠️ Supabase client niet actief — test overgeslagen.")
