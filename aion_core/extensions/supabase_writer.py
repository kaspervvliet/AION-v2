
"""
📄 Bestand: supabase_writer.py
🔍 Doel: Veilige en centrale helper voor Supabase insert en update operaties
🧩 Gebruikt door: alle modules die data uploaden (performance, signals, equity)
📦 Behoort tot: aion_core/extensions/
🧠 Verwacht implementatie van: retries, foutafhandeling, logging
"""

import os
import time
from supabase import create_client, Client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_API_KEY)

MAX_RETRIES = 3
RETRY_DELAY = 2  # seconden

def upload_record(table: str, data: dict):
    attempts = 0
    while attempts < MAX_RETRIES:
        try:
            response = supabase.table(table).insert([data]).execute()
            print(f"[Supabase] Insert naar {table} succesvol.")
            return response
        except Exception as e:
            print(f"[Supabase ERROR] Insert poging {attempts + 1} mislukt: {e}")
            time.sleep(RETRY_DELAY)
            attempts += 1

def update_record(table: str, match_field: str, match_value, updates: dict):
    attempts = 0
    while attempts < MAX_RETRIES:
        try:
            response = supabase.table(table).update(updates).eq(match_field, match_value).execute()
            print(f"[Supabase] Update van {table} succesvol.")
            return response
        except Exception as e:
            print(f"[Supabase ERROR] Update poging {attempts + 1} mislukt: {e}")
            time.sleep(RETRY_DELAY)
            attempts += 1
