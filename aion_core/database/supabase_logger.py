"""
📄 Bestand: supabase_logger.py
🔍 Doel: Insert data naar Supabase Edge Function zonder bestaande flow te breken
🧩 Gebruikt door: logging_engine, andere modules
📦 Behoort tot: aion_core/database
🧠 Verwacht implementatie van: .env + requests
"""

import os
import requests
import logging
from dotenv import load_dotenv

# Probeer omgevingsvariabelen te laden (lokaal)
load_dotenv()

# Configureer logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ophalen Supabase configuratie
SUPABASE_EDGE_FUNCTION_URL = os.getenv("SUPABASE_EDGE_FUNCTION_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

if not SUPABASE_EDGE_FUNCTION_URL or not SUPABASE_SERVICE_ROLE_KEY:
    logger.warning("⚠️ SUPABASE_EDGE_FUNCTION_URL of SUPABASE_SERVICE_ROLE_KEY niet gevonden in .env of Render environment!")

def insert_via_edge(table: str, payload: dict) -> dict:
    """Insert data naar Supabase Edge Function."""
    if not SUPABASE_EDGE_FUNCTION_URL or not SUPABASE_SERVICE_ROLE_KEY:
        logger.error("❌ Verplichte Supabase configuratie ontbreekt.")
        return {}

    if not table or not payload:
        logger.error("❌ Ongeldige input: table of payload ontbreekt.")
        return {}

    headers = {
        "Authorization": f"Bearer {SUPABASE_SERVICE_ROLE_KEY}",
        "Content-Type": "application/json"
    }
    body = {
        "table": table,
        "payload": payload
    }

    try:
        response = requests.post(SUPABASE_EDGE_FUNCTION_URL, headers=headers, json=body, timeout=10)
        response.raise_for_status()
        logger.info(f"✅ Insert gelukt naar tabel '{table}'.")
        return response.json()
    except requests.RequestException as e:
        logger.error(f"❌ Insert via Edge Function mislukt: {e}")
        return {}

# Geen __main__ testblok, want bedoeld voor productiegebruik
