
"""
📄 Bestand: keep_alive.py
🔍 Doel: Houdt de Render service actief door periodiek self-pings te sturen.
🧩 Gebruikt door: main_live.py, streamlit_main.py
📦 Behoort tot: aion_core/utils
🧠 Verwacht implementatie van: threading, requests, .env configuratie
"""

import threading
import time
import requests
import os

def start_keep_alive():
    def keep_alive():
        url = os.getenv("KEEP_ALIVE_URL")
        if not url:
            print("[KEEP-ALIVE] ❌ Geen KEEP_ALIVE_URL gevonden in .env — pingfunctie wordt overgeslagen.")
            return

        print(f"[KEEP-ALIVE] 🔁 Self-ping gestart naar {url}")
        while True:
            try:
                response = requests.get(url, timeout=10)
                print(f"[KEEP-ALIVE] ✅ Ping gestuurd → Status: {response.status_code}")
            except Exception as e:
                print(f"[KEEP-ALIVE] ⚠️ Fout bij ping: {e}")
            time.sleep(180)  # ping elke 3 minuten

    threading.Thread(target=keep_alive, daemon=True).start()
