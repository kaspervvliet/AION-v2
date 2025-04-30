
"""
📄 Bestand: supabase_logger.py
🔍 Doel: Logging en ophalen van signalen, biases, en resultaten via Supabase
🧩 Gebruikt door: kernel, signal_engine, debug
📦 Behoort tot: aion_core/database
🧠 Verwacht implementatie van: log_signal(), get_last_bias_state()
"""

import os
import requests
import logging

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_BIAS_TABLE = "bias_log"
HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}
logger = logging.getLogger(__name__)

def log_bias_state(symbol: str, timeframe: str, bias: str):
    data = {
        "symbol": symbol,
        "timeframe": timeframe,
        "bias": bias
    }
    res = requests.post(
        f"{SUPABASE_URL}/rest/v1/{SUPABASE_BIAS_TABLE}",
        headers=HEADERS,
        json=data
    )
    if res.status_code != 201:
        logger.warning(f"[SUPABASE] Bias log mislukt: {res.text}")

def get_last_bias_state(symbol: str, timeframe: str):
    url = f"{SUPABASE_URL}/rest/v1/{SUPABASE_BIAS_TABLE}?symbol=eq.{symbol}&timeframe=eq.{timeframe}&order=timestamp.desc&limit=1"
    res = requests.get(url, headers=HEADERS)
    if res.status_code == 200:
        data = res.json()
        if data:
            return data[0].get("bias")
        else:
            logger.info("[SUPABASE] Geen bias state gevonden.")
    else:
        logger.warning(f"[SUPABASE] Fout bij ophalen bias: {res.text}")
    return None
