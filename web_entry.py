"""
📄 Bestand: web_entry.py
🔍 Doel: Streamlit web dashboard starter voor AION Trading Suite
🧩 Gebruikt door: ontwikkelaars en Render hosting
📦 Behoort tot: root runners
🧠 Verwacht implementatie van: streamlit_main
"""

import streamlit as st
import logging

st.set_page_config(page_title="AION Dashboard", page_icon="📊", layout="wide")

from aion_core.config import is_muted
from aion_core.streamlit_ui.dashboard import render_dashboard as run_dashboard
from aion_core.utils.keep_alive import start_keep_alive
from aion_core.utils.status_handler import run_status_check

logger = logging.getLogger("AION")

def main():
    if is_muted():
        logger.info("🔇 AION mute-mode actief — dashboard wordt niet geladen.")
        st.warning("🔇 AION staat in mute-mode. Dashboard wordt niet gestart.")
        return

    logger.info("📊 Streamlit dashboard wordt gestart")

    try:
        run_status_check()
        start_keep_alive()
        run_dashboard()
    except Exception as e:
        logger.error(f"❌ Fout bij opstarten dashboard: {e}")
        st.error("Er ging iets mis bij het starten van de applicatie.")

if __name__ == "__main__":
    main()