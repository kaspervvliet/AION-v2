"""
📄 Bestand: telegram_alerts.py
🔍 Doel: Versturen van alerts naar Telegram via bot-API
🧩 Gebruikt door: signal_executor, reflectie-module, supabase_logger
📦 Behoort tot: /
🧠 Verwacht implementatie van: requests, config.get_config()
"""

import requests
from config import get_config
from aion_core.utils.logger import logger


def send_alert(message: str) -> bool:
    config = get_config()
    token = config.get("TELEGRAM_BOT_TOKEN")
    chat_id = config.get("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        logger.warning("⚠️ Telegramconfig ontbreekt — geen alert verzonden.")
        return False

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }

    try:
        response = requests.post(url, json=payload, timeout=5)
        if response.status_code != 200:
            logger.warning(f"⚠️ Telegram error: {response.text}")
            return False
        return True
    except Exception as e:
        logger.error(f"❌ Fout bij verzenden Telegram alert: {e}")
        return False
