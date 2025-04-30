
"""
📄 Bestand: keep_alive.py
🔍 Doel: Houdt de Render service actief door periodiek self-pings te sturen met logging.
🧩 Gebruikt door: streamlit_main.py, web_entry.py
📦 Behoort tot: aion_core/utils
🧠 Logt naar: /tmp/keepalive.log
"""

import threading
import time
import requests
import os
import traceback

def start_keep_alive():
    def keep_alive():
        url = os.getenv("KEEP_ALIVE_URL")
        if not url:
            with open("/tmp/keepalive.log", "a") as f:
                f.write("[KEEP-ALIVE] ❌ Geen KEEP_ALIVE_URL gevonden\n")
            return

        with open("/tmp/keepalive.log", "a") as f:
            f.write(f"[KEEP-ALIVE] 🔁 Self-ping gestart naar {url}\n")

        while True:
            try:
                response = requests.get(url, timeout=10)
                with open("/tmp/keepalive.log", "a") as f:
                    f.write(f"[{time.ctime()}] ✅ Ping gestuurd → Status: {response.status_code}\n")
            except Exception:
                with open("/tmp/keepalive.log", "a") as f:
                    f.write(f"[{time.ctime()}] ⚠️ Fout bij ping:\n{traceback.format_exc()}\n")
            time.sleep(180)

    threading.Thread(target=keep_alive, daemon=True).start()
