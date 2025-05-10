from aion_core.config import is_muted
"""
📄 Bestand: dashboard.py
🔍 Doel: Streamlit-dashboard met equity/reflectie
🧩 Gebruikt door: web_entry.py
📦 Behoort tot: aion_core/ui/
🧠 Verwacht implementatie van: supabase_client.fetch_equity(), fetch_reflection()
"""

import streamlit as st
import logging

from aion_core.database.supabase_reader import fetch_equity, fetch_reflection

logger = logging.getLogger("AION")

def render_dashboard():
    st.title("📊 AION Performance Dashboard")

    if is_muted():
        st.warning("Dashboard staat in mute-mode (AION_MUTE=True)")
        return

    try:
        equity_data = fetch_equity("SOL/USDT")
        if not equity_data:
            st.info("Geen equitydata gevonden.")
            logger.info("Equity response leeg.")
        else:
            st.subheader("Equity Progressie")
            st.line_chart([e["equity"] for e in equity_data])

        reflection_data = fetch_reflection("SOL/USDT")
        if not reflection_data:
            st.info("Geen reflectiedata beschikbaar.")
            logger.info("Reflectie response leeg.")
        else:
            st.subheader("AI Reflectie")
            for r in reflection_data:
                st.markdown(f"**{r['timestamp']}** — {r['prompt']}")

    except Exception as e:
        logger.error(f"Fout bij laden dashboard: {e}")
        st.error("Er ging iets mis bij het laden van de data.")

if __name__ == "__main__":
    render_dashboard()
