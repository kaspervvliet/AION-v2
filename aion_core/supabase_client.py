"""
📄 Bestand: supabase_client.py
🔍 Doel: Interface tussen AION V2 en Supabase database
🧩 Gebruikt door: context.py, strategieën, logger
📦 Behoort tot: aion_core/
"""

import os
import requests
import json

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

# === CONTEXT ===
def get_context_from_supabase(symbol, timeframe):
    response = requests.get(
        f"{SUPABASE_URL}/rest/v1/context?symbol=eq.{symbol}&timeframe=eq.{timeframe}",
        headers=HEADERS
    )
    if response.status_code == 200 and response.json():
        return response.json()[0]
    return {}

def push_context_to_supabase(payload):
    response = requests.post(
        f"{SUPABASE_URL}/rest/v1/context",
        headers=HEADERS,
        data=json.dumps(payload)
    )
    return response.status_code == 201

# === LOGGING ===
def log_signal_to_supabase(strategy_name, message, level="INFO"):
    log_payload = {
        "strategy": strategy_name,
        "message": message,
        "level": level
    }
    response = requests.post(
        f"{SUPABASE_URL}/rest/v1/logs",
        headers=HEADERS,
        data=json.dumps(log_payload)
    )
    return response.status_code == 201

# === CONFIG ===
def fetch_config_from_supabase(strategy_name):
    response = requests.get(
        f"{SUPABASE_URL}/rest/v1/configs?strategy=eq.{strategy_name}",
        headers=HEADERS
    )
    if response.status_code == 200 and response.json():
        return response.json()[0]
    return {}