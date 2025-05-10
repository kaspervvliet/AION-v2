"""
📄 Bestand: web_entry.py
🔍 Doel: Streamlit web dashboard starter voor AION Trading Suite
🧩 Gebruikt door: ontwikkelaars en Render hosting
📦 Behoort tot: root runners
🧠 Verwacht implementatie van: streamlit_main
"""

import streamlit as st
import logging
from config import is_muted
from aion_core.streamlit_ui.streamlit_main import run_dashboard
from aion_core.utils.keep_alive import start_keep_alive
from aion_core.utils.status_handler import run_status_check

logger = logging.getLogger("AION")

def main():
    if is_muted():
        st.warning("🔇 AION staat in mute-mode. Dashboard wordt niet gestart.")
        return

    logger.info("📊 Streamlit dashboard wordt gestart")
    run_status_check()
    st.set_page_config(page_title="AION Dashboard", page_icon="📊", layout="wide")
    start_keep_alive()
    run_dashboard()

if __name__ == "__main__":
    main()
