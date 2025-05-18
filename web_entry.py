
"""
📄 Bestand: web_entry.py
🔍 Doel: Start de Streamlit-dashboard en optioneel de live loop
🧩 Gebruikt door: Render
📦 Behoort tot: root
🧠 Verwacht implementatie van: render_dashboard(), main_live.main()
"""

import threading
from main_live import main as run_live_loop
from aion_core.streamlit_ui.dashboard import render_dashboard as run_dashboard

# Start de live loop in achtergrondthread
threading.Thread(target=run_live_loop, daemon=True).start()

# Start Streamlit-dashboard
run_dashboard()
