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
            print("[KEEP-ALIVE] Geen KEEP_ALIVE_URL gevonden in .env, stoppen...")
            return

        while True:
            try:
                print(f"[KEEP-ALIVE] Ping naar {url}")
                response = requests.get(url, timeout=10)
                if response.status_code != 200:
                    print(f"[KEEP-ALIVE] Waarschuwing: respons {response.status_code}")
            except Exception as e:
                print(f"[KEEP-ALIVE] Fout bij ping: {e}")
            time.sleep(13 * 60)  # elke 13 minuten pingen

    t = threading.Thread(target=keep_alive, daemon=True)
    t.start()
