"""
📄 Bestand: config.py
🔍 Doel: [AUTO-GEGENEREERD: controleer doel handmatig]
🧩 Gebruikt door: onbekend
📦 Behoort tot: aion_core
🧠 Laatst geüpdatet: 2025-04-25
"""

import logging
logger = logging.getLogger(__name__)

### aion_core/config.py – veilige config via omgevingsvariabelen ###

import os

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

AION_TELEGRAM_BOT = os.getenv("AION_TELEGRAM_BOT")
AION_TELEGRAM_CHAT = os.getenv("AION_TELEGRAM_CHAT")

LIVE_MODE = os.getenv("AION_LIVE", "False") == "True"

# Optioneel: fallback of debug logging
if not SUPABASE_URL:
    logger.info("[CONFIG] ⚠️ SUPABASE_URL ontbreekt in environment.")
if not AION_TELEGRAM_BOT:
    logger.info("[CONFIG] ⚠️ Telegram bot-token ontbreekt in environment.")
