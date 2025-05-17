"""
📄 Bestand: web_entry.py  
🔍 Doel: Start Streamlit-dashboard + parallel de AION live-logging  
🧩 Gebruikt door: main.py (Render web entrypoint)  
📦 Behoort tot: streamlit_ui  
🧠 Verwacht implementatie van: render_dashboard(), run()  
"""

import threading
import threading
from main_live import main as run_live_loop
threading.Thread(target=run_live_loop, daemon=True).start()

from aion_core.streamlit_ui.dashboard import render_dashboard as run_dashboard
from aion_core.database.supabase_logger import log_context_data
from main_live import run as run_aion
from datetime import datetime

def run_main_in_thread():
    try:
        # ✅ Dummy entry voor verificatie
        run_aion()  # ✅ Start AION live runner
            "symbol": "TEST/LOG",
            "timestamp": int(datetime.utcnow().timestamp()),
            "sweep": False,
            "bos": False,
            "fvg": False,
            "open": 0,
            "high": 0,
            "low": 0,
            "close": 0,
            "volume": 0
        }])
    except Exception as e:
        print(f"❌ Logging thread faalde: {e}")

if __name__ == "__main__":
    threading.Thread(target=run_main_in_thread, daemon=True).start()
    run_dashboard()