"""
📄 Bestand: supabase_client.py
🔍 Doel: Supabase-interface voor context, logging en opslag
🧩 Gebruikt door: context.py, backtests, signal loops
📦 Behoort tot: aion_core
🧠 Laatst geüpdatet: 2025-04-25
"""

import logging
import requests
from aion_core import config

logger = logging.getLogger(__name__)

SUPABASE_URL = config.SUPABASE_URL
SUPABASE_KEY = config.SUPABASE_KEY

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

def insert(table: str, data: dict):
    if not SUPABASE_URL:
        logger.warning("[SUPABASE] ❌ Geen SUPABASE_URL gedefinieerd")
        return
    url = f"{SUPABASE_URL}/rest/v1/{table}"
    try:
        response = requests.post(url, json=data, headers=headers)
        logger.info(f"[SUPABASE] Insert {table} ➝ {response.status_code}")
        if not response.ok:
            logger.error(f"[SUPABASE] ❌ Insert error: {response.text}")
    except Exception as e:
        logger.exception(f"[SUPABASE] ❌ Insert failed: {e}")

def select(table: str, limit: int = 10):
    if not SUPABASE_URL:
        logger.warning("[SUPABASE] ❌ Geen SUPABASE_URL gedefinieerd")
        return []

    url = f"{SUPABASE_URL}/rest/v1/{table}?limit={limit}&order=timestamp.desc"
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        logger.error(f"[SUPABASE] ❌ Fout bij ophalen: {response.status_code} → {response.text}")
    except Exception as e:
        logger.exception(f"[SUPABASE] ❌ Select error: {e}")
    return []

def get_context_from_supabase(symbol: str, timeframe: str):
    rows = select("context", limit=5)
    for row in rows:
        if row.get("symbol") == symbol and row.get("timeframe") == timeframe:
            return row
    return {}

def push_context_to_supabase(context_data: dict):
    if not isinstance(context_data, dict):
        logger.warning("[SUPABASE] ❌ push_context: geen dict meegegeven")
        return
    insert("context", context_data)

__all__ = [
    "insert",
    "select",
    "get_context_from_supabase",
    "push_context_to_supabase"
]