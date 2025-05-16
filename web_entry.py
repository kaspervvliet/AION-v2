"""
📄 Bestand: web_entry.py  
🔍 Doel: Start Streamlit-dashboard + parallel de AION live-logging  
🧩 Gebruikt door: main.py (Render web entrypoint)  
📦 Behoort tot: streamlit_ui  
🧠 Verwacht implementatie van: render_dashboard(), run()  
"""

import threading
from aion_core.streamlit_ui.dashboard import render_dashboard as run_dashboard
from main_live import run as run_main_live

def run_main_in_thread():
    try:
        print("🔁 Start main_live logging thread...")
        run_main_live()
    except Exception as e:
        print(f"❌ main_live crashed: {e}")

if __name__ == "__main__":
    threading.Thread(target=run_main_in_thread, daemon=True).start()
    run_dashboard()
