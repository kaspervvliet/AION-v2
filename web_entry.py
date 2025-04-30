
"""
📄 Bestand: web_entry.py
🔍 Doel: Streamlit web dashboard starter voor AION Trading Suite
🧩 Gebruikt door: ontwikkelaars en Render hosting
📦 Behoort tot: root runners
🧠 Verwacht implementatie van: streamlit_main
"""

import streamlit as st
from aion_core.streamlit_ui.streamlit_main import run_dashboard
from aion_core.utils.keep_alive import start_keep_alive
from aion_core.utils.status_handler import run_status_check  # ✅ toegevoegd

def main():
    run_status_check()  # ⏱️ Check voor status endpoint
    st.set_page_config(page_title="AION Dashboard", page_icon="📊", layout="wide")
    start_keep_alive()  # ✅ activeert Render-safe self-ping
    run_dashboard()

if __name__ == "__main__":
    main()
