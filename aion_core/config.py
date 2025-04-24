
### aion_core/config.py – veilige config via omgevingsvariabelen ###

import os

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

AION_TELEGRAM_BOT = os.getenv("AION_TELEGRAM_BOT")
AION_TELEGRAM_CHAT = os.getenv("AION_TELEGRAM_CHAT")

LIVE_MODE = os.getenv("AION_LIVE", "False") == "True"

# Optioneel: fallback of debug logging
if not SUPABASE_URL:
    print("[CONFIG] ⚠️ SUPABASE_URL ontbreekt in environment.")
if not AION_TELEGRAM_BOT:
    print("[CONFIG] ⚠️ Telegram bot-token ontbreekt in environment.")
