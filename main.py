"""
📄 Bestand: main.py
🔍 Doel: Startpunt van AION V2 (Streamlit UI)
🧩 Gebruikt door: eindgebruiker
📦 Behoort tot: projectroot
"""

import streamlit as st
from aion_core.loader import StrategyLoader
from aion_core.context import AIONContext

st.set_page_config(page_title="AION V2", layout="wide")
st.title("🤖 AION Smart Money Concepts V2")

loader = StrategyLoader()
available_strategies = loader.list_available_strategies()

selected_strategy = st.selectbox("Kies een strategie:", available_strategies)

if selected_strategy:
    module = loader.load_strategy(selected_strategy)
    StrategyClass = getattr(module, "Strategy", None)

    if StrategyClass:
        context = AIONContext(symbol="SOL/USDT", timeframe="15m")
        context.load_from_supabase()

        strategy = StrategyClass(config={}, context=context)

        st.markdown(f"### 🧠 Strategie: {strategy.get_metadata().get('name')}")
        st.markdown(f"Versie: `{strategy.get_metadata().get('version')}`")
        st.markdown("(Visualisaties volgen hier)")
    else:
        st.error("❌ Strategy class niet gevonden in module.")