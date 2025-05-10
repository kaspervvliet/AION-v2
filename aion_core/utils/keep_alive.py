"""
📄 Bestand: keep_alive.py
🔍 Doel: Houdt de Render service actief via self-ping
🧩 Gebruikt door: streamlit_main.py, web_entry.py
📦 Behoort tot: aion_core/utils
🧠 Verwacht implementatie van: threading, logging, KEEP_ALIVE_URL
"""

import threading
import time
import requests
import os
import logging
from config import is_muted

logger = logging.getLogger("AION")

def start_keep_alive() -> None:
    """
    Start een achtergrondthread die periodiek een ping stuurt naar een KEEP_ALIVE_URL.
    Wordt automatisch gestopt als de env-waarde ontbreekt of mute-mode actief is.
    """
    def keep_alive():
        url = os.getenv("KEEP_ALIVE_URL")
        if not url:
            logger.warning("❌ KEEP_ALIVE_URL ontbreekt — keep-alive gestopt.")
            return

        if is_muted():
            logger.info("🔇 Keep-alive staat in mute-mode.")
            return

        logger.info(f"🔁 Keep-alive gestart — ping naar {url}")
        while True:
            try:
                response = requests.get(url, timeout=10)
                logger.info(f"✅ Ping → {url} (status={response.status_code})")
            except Exception as e:
                logger.error(f"❌ Pingfout: {e}")
            time.sleep(60)

    thread = threading.Thread(target=keep_alive, daemon=True)
    thread.start()

if __name__ == "__main__":
    start_keep_alive()
    time.sleep(120)  # Houd main-thread tijdelijk in leven
