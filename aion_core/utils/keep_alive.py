
## Nieuw bestand: aion_core/utils/keep_alive.py

"""
📄 Bestand: aion_core/utils/keep_alive.py
🔍 Doel: Houdt de Render instance actief door elke 13 minuten een self-ping te doen.
🧩 Gebruikt door: main_live.py (of web_entry.py)
📦 Behoort tot: aion_core/utils
🧠 Verwacht implementatie van: threading, requests
"""

import threading
import time
import requests

def start_keep_alive():
    def keep_alive():
        url = "https://aion-v2-t5qp.onrender.com"  # Hardcoded URL
        while True:
            try:
                print(f"[KEEP-ALIVE] Ping naar {url}")
                requests.get(url, timeout=10)
            except Exception as e:
                print(f"[KEEP-ALIVE] Fout bij ping: {e}")
            time.sleep(13 * 60)  # 13 minuten

    t = threading.Thread(target=keep_alive, daemon=True)
    t.start()
