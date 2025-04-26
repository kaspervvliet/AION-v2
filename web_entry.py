
"""
📄 Bestand: web_entry.py
🔍 Aangepast: Keep Alive mechanisme toegevoegd voor Streamlit UI.
"""

from aion_core.utils.keep_alive import start_keep_alive
import streamlit as st

def main():
    start_keep_alive()  # ✅ Houd de server wakker

    st.title("AION V2 Dashboard")
    st.write("Welkom bij de tradingtool!")
    # [Hier meer Streamlit pagina's]

if __name__ == "__main__":
    main()
