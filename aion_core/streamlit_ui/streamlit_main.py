"""
📄 Bestand: streamlit_main.py
🔍 Doel: Start Streamlit dashboard en interne keep-alive self-ping.
🧩 Gebruikt door: Render deployment
📦 Behoort tot: aion_core/
🧠 Verwacht implementatie van: streamlit, keep_alive
"""

import streamlit as st
from aion_core.utils.keep_alive import start_keep_alive
from aion_core.utils.status_handler import run_status_check

# Status-check eerste
run_status_check()

# Start self-pinger
start_keep_alive()

# Echte dashboard imports
from aion_core.streamlit_ui import dashboard

# Streamlit interface starten
st.title("AION V2 Dashboard")
dashboard.show_dashboard()
