"""
📄 Bestand: config.py
🔍 Doel: Laden en beheren van configuratie uit .env-bestand
🧩 Gebruikt door: alerts, supabase, logger, kernmodules
📦 Behoort tot: /
🧠 Verwacht implementatie van: os.environ, dotenv
"""

import os
import logging
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger("AION")

# Basisconfiguratie
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
MODE = os.getenv("AION_MODE", "DEV")
MUTE = os.getenv("AION_MUTE", "false").lower() == "true"

# Fallback-checks
missing = []
for var in ["SUPABASE_URL", "SUPABASE_KEY"]:
    if not os.getenv(var):
        missing.append(var)
if missing:
    logger.warning(f"Ontbrekende .env variabelen: {missing}")

def is_muted() -> bool:
    """Geeft aan of logging/output gemute moet worden."""
    return MUTE

def get_config() -> dict:
    """Retourneert alle relevante configuratie als dict."""
    return {
        "supabase_url": SUPABASE_URL,
        "supabase_key": SUPABASE_KEY,
        "telegram_token": TELEGRAM_TOKEN,
        "telegram_chat_id": TELEGRAM_CHAT_ID,
        "mode": MODE,
        "mute": MUTE
    }
