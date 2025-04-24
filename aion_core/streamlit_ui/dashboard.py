
import streamlit as st
import pandas as pd
import plotly.express as px
from aion_core.supabase_client import select
from aion_core.kernel import trade_explainer

st.set_page_config(page_title="AION Dashboard", layout="wide")
st.title("🧠 AION StrategicKernel – Live Insights")

# Tabs
log_tab, reflect_tab, explain_tab, heatmap_tab = st.tabs(["📈 Equity Log", "🧠 Reflecties", "🔍 Uitleg", "🔥 Heatmap"])

with log_tab:
    st.subheader("📊 Equity Log (laatste 100 entries)")
    equity_logs = select("equity_log", limit=100)
    if equity_logs:
        st.dataframe(equity_logs[::-1])
    else:
        st.warning("Geen equity data gevonden.")

with reflect_tab:
    st.subheader("🔁 GPT Reflecties (laatste 100)")
    reflections = select("reflections", limit=100)
    if reflections:
        for r in reflections[::-1]:
            with st.expander(f"🧠 Reflectie @ {r['timestamp']} – Run {r['run_id']}"):
                st.markdown(f"**Setup:** `{r['setup']}`")
                st.markdown(f"**Decision:** `{r['decision']} ({r['confidence']:.2f})` → _{r['reason']}_")
                st.markdown(f"**Outcome:** `{r['outcome']}`")
                st.markdown(f"**Feedback:**\n\n> {r.get('gpt_feedback') or '⚠️ Nog geen GPT feedback.'}")
    else:
        st.info("Nog geen reflectie logs gevonden.")

with explain_tab:
    st.subheader("🧠 Laatste Beslissing Uitleg (demo)")
    dummy_setup = {"bias": "bullish", "has_bos": True, "has_fvg": True, "rsi": 28}
    explanation = trade_explainer.explain_decision(dummy_setup, "GO", 0.76, "bias + BOS + FVG")
    st.markdown("```\n" + explanation + "\n```")

with heatmap_tab:
    st.subheader("🔥 RR Heatmap + Filters + Equitycurve")
    df = pd.DataFrame(select("equity_log", limit=1000))
    if not df.empty:
        df = df[df["rr"].notnull()]

        # Filters
        biases = sorted(df["bias"].dropna().unique())
        fvg_vals = sorted(df["has_fvg"].dropna().unique())
        rsi_min, rsi_max = int(df["rsi"].min()), int(df["rsi"].max())

        col1, col2, col3 = st.columns(3)
        with col1:
            bias_filter = st.selectbox("📊 Bias filter", options=["ALL"] + list(biases))
        with col2:
            fvg_filter = st.selectbox("📥 Has FVG", options=["ALL"] + list(map(str, fvg_vals)))
        with col3:
            rsi_range = st.slider("📉 RSI-range", rsi_min, rsi_max, (rsi_min, rsi_max))

        if bias_filter != "ALL":
            df = df[df["bias"] == bias_filter]
        if fvg_filter != "ALL":
            df = df[df["has_fvg"].astype(str) == fvg_filter]
        df = df[df["rsi"].between(*rsi_range)]

        st.markdown("### 🔥 RR Heatmap: Bias × FVG")
        heat = df.copy()
        heat["has_fvg"] = heat["has_fvg"].astype(str)
        pivot = heat.pivot_table(values="rr", index="bias", columns="has_fvg", aggfunc="mean")
        fig = px.imshow(pivot, text_auto=True, color_continuous_scale="RdBu", aspect="auto")
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("### 📈 Equity over tijd (cumulatief RR)")
        df_sorted = df.sort_values("timestamp")
        df_sorted["cumulative_rr"] = df_sorted["rr"].cumsum()
        line = px.line(df_sorted, x="timestamp", y="cumulative_rr", title="📉 Equitycurve")
        st.plotly_chart(line, use_container_width=True)
    else:
        st.warning("Niet genoeg equity data voor heatmap.")
