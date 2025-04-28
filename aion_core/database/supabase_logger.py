
"""
📄 Bestand: supabase_logger.py (verbeterd)
🔍 Doel: Communicatie met Supabase edge functions en REST API
🧩 Gebruikt door: context_updater, signal_generator, signal_evaluator, signal_executor
📦 Behoort tot: aion_core/database
🧠 Verbeterd: fetch_validated_signals zonder Authorization header
"""

import os
import requests
import logging
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY")
SUPABASE_EDGE_FUNCTION = os.getenv("SUPABASE_EDGE_FUNCTION", "aion_logger")

logger = logging.getLogger(__name__)

def insert_via_edge(table: str, payload: dict) -> bool:
    try:
        url = f"{SUPABASE_URL}/functions/v1/{SUPABASE_EDGE_FUNCTION}"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {SUPABASE_API_KEY}",
        }
        body = {
            "table": table,
            "payload": payload,
        }
        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status()
        logger.info(f"✅ Insert gelukt naar tabel '{table}'.")
        return True
    except Exception as e:
        logger.error(f"❌ Insert via Edge Function mislukt: {e}")
        logger.error(f"❌ Response inhoud: {getattr(e, 'response', 'geen response')}")
        return False

def fetch_validated_signals() -> list:
    """Ophalen van gevalideerde signals uit Supabase zonder foutieve Authorization header."""
    try:
        url = f"{SUPABASE_URL}/rest/v1/signals?status=eq.validated"
        headers = {
            "apikey": SUPABASE_API_KEY,
            "Content-Type": "application/json",
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        logger.info(f"✅ {len(data)} gevalideerde signals opgehaald.")
        return data
    except Exception as e:
        logger.error(f"❌ Fout bij ophalen van gevalideerde signals: {e}")
        return []

def update_signal_status(signal_id: str, update_data: dict) -> bool:
    """Update een signal met nieuwe status of executie-informatie."""
    try:
        url = f"{SUPABASE_URL}/rest/v1/signals?id=eq.{signal_id}"
        headers = {
            "apikey": SUPABASE_API_KEY,
            "Content-Type": "application/json",
            "Prefer": "return=representation"
        }
        response = requests.patch(url, headers=headers, json=update_data)
        response.raise_for_status()
        logger.info(f"✅ Signal {signal_id} succesvol geüpdatet.")
        return True
    except Exception as e:
        logger.error(f"❌ Fout bij updaten van signal {signal_id}: {e}")
        return False
