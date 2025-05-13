"""
📄 Bestand: status_handler.py
🔍 Doel: Superlichte health-check endpoint voor uptime monitoring
🧩 Gebruikt door: UptimeRobot, Render Health Check
📦 Behoort tot: aion_core/utils/
🧠 Altijd 200 OK response bij ?status=ping
"""

import streamlit as st

def run_status_check() -> None:
    query_params = st.query_params
    if query_params.get("status") == ["ping"]:
        st.write("✅ OK - AION V2 is live")
        st.stop()  # Stop verdere verwerking om latency te beperken

if __name__ == "__main__":
    # Alleen handmatige test in Streamlit mogelijk
    run_status_check()
