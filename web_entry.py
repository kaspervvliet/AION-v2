
"""
📄 Bestand: web_entry.py
🔍 Doel: Streamlit web dashboard starter voor AION Trading Suite
🧩 Gebruikt door: ontwikkelaars en Render hosting
📦 Behoort tot: root runners
🧠 Verwacht implementatie van: streamlit_main
"""

import streamlit as st
from aion_core.streamlit_ui.streamlit_main import run_dashboard

def main():
    st.set_page_config(page_title="AION Dashboard", page_icon="📊", layout="wide")
    run_dashboard()

if __name__ == "__main__":
    main()
