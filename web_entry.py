
"""
📄 Bestand: web_entry.py
🔍 Doel: Start de Streamlit-dashboard en de live loop persistent
🧩 Gebruikt door: Render
📦 Behoort tot: root
🧠 Verwacht implementatie van: render_dashboard(), main_live.main()
"""

import threading
import logging
from main_live import main as run_live_loop
from aion_core.streamlit_ui.dashboard import render_dashboard as run_dashboard

logger = logging.getLogger("AION")

def start_live_loop():
    logger.info("🧠 Start live loop vanuit web_entry...")
    run_live_loop()

# Start de live loop (niet-daemon zodat Render hem niet afsluit)
threading.Thread(target=start_live_loop).start()

# Start Streamlit-dashboard
run_dashboard()
