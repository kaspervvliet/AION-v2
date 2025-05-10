"""
📄 Bestand: run_backtest.py
🔍 Doel: Backtest-runner met contextuele setup en visualisatie
🧩 Gebruikt door: Devs tijdens test van strategieën
📦 Behoort tot: /
🧠 Verwacht implementatie van: strategy_executor, create_context, PerformanceTracker
"""

from aion_core.kernel.strategy_executor import run_strategy_on_market
from aion_core.backtest.context_manager import create_context
from aion_core.performance.performance_tracker import PerformanceTracker
from aion_core.kernel.adaptive_strategy_selector import select_best_strategy
from aion_core.utils.logger import logger

import streamlit as st

# Streamlit entry
st.set_page_config(page_title="🧪 AION Backtest Runner", layout="wide")

st.title("📊 AION Strategy Backtester")

symbol = st.text_input("Trading pair", value="SOL/USDT")
timeframe = st.selectbox("Timeframe", options=["15m", "1h", "4h", "1d"], index=0)
limit = st.slider("Candles to load", min_value=100, max_value=1000, step=100, value=500)

if st.button("🚀 Run Backtest"):
    st.info(f"⏳ Loading context for {symbol} @ {timeframe}...")
    context = create_context(symbol=symbol, timeframe=timeframe, limit=limit)

    best_strategy = select_best_strategy(context)
    st.success(f"✅ Strategy selected: `{best_strategy.__class__.__name__}`")

    logger.info("▶️ Running backtest...")
    results = run_strategy_on_market(strategy=best_strategy, context=context)

    if not results:
        st.warning("⚠️ Geen resultaten gegenereerd.")
    else:
        tracker = PerformanceTracker()
        tracker.load_results(results)

        st.subheader("📈 Performance overview")
        st.metric("Total Trades", tracker.total_trades)
        st.metric("Win Rate", f"{tracker.win_rate:.2f}%")
        st.metric("Avg RR", f"{tracker.avg_rr:.2f}")

        fig = tracker.plot_equity_curve()
        st.plotly_chart(fig, use_container_width=True)
