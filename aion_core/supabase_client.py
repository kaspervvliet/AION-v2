"""
📄 Bestand: supabase_client.py
🔍 Doel: [AUTO-GEGENEREERD: controleer doel handmatig]
🧩 Gebruikt door: onbekend
📦 Behoort tot: aion_core
🧠 Laatst geüpdatet: 2025-04-25
"""

import logging
logger = logging.getLogger(__name__)
import requests
from aion_core import config

SUPABASE_URL = config.SUPABASE_URL
SUPABASE_KEY = config.SUPABASE_KEY

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

def insert(table: str, data: dict):
    if not SUPABASE_URL:
        logger.info(f"[SUPABASE] ❌ Geen SUPABASE_URL gedefinieerd")
        return

    url = f"{SUPABASE_URL}/rest/v1/{table}"
    response = requests.post(url, json=data, headers=headers)
    logger.info(f"[SUPABASE] Insert {table} -> {response.status_code}")

def select(table: str, limit: int = 10):
    if not SUPABASE_URL:
        logger.info(f"[SUPABASE] ❌ Geen SUPABASE_URL gedefinieerd")
        return []

    url = f"{SUPABASE_URL}/rest/v1/{table}?limit={limit}&order=timestamp.desc"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    logger.info(f"[SUPABASE] ❌ Fout bij ophalen: {response.status_code}")
    return []

def get_context_from_supabase(symbol: str, timeframe: str):
    rows = select("context", limit=1)
    for row in rows:
        if row.get("symbol") == symbol and row.get("timeframe") == timeframe:
            return row
    return {}

def push_context_to_supabase(context_data: dict):
    insert("context", context_data)

__all__ = [
    "insert",
    "select",
    "get_context_from_supabase",
    "push_context_to_supabase"
]
