
"""
📄 Bestand: status_handler.py
🔍 Doel: Superlichte health-check endpoint voor uptime monitoring
🧩 Gebruikt door: UptimeRobot, Render Health Check
📦 Behoort tot: aion_core/utils/
🧠 Altijd 200 OK response bij ?status=ping
"""

import streamlit as st

def run_status_check():
    query_params = st.experimental_get_query_params()
    if query_params.get("status") == ["ping"]:
        st.write("✅ OK - AION V2 is live")
        st.stop()
