"""
📄 Bestand: htf_context.py
🔍 Doel: Maakt high-timeframe context aan uit dataframe
🧩 Gebruikt door: kernel, bias modules, strategieën
📦 Behoort tot: aion_core/context/
🧠 Verwacht implementatie van: pandas, logger
"""

import pandas as pd
from aion_core.utils.logger import logger


def build_htf_context(df: pd.DataFrame, symbol: str) -> dict:
    context = {"symbol": symbol}

    if "bias" in df.columns:
        context["bias"] = df["bias"].iloc[-1]
    else:
        logger.warning("⚠️ Bias-kolom ontbreekt in HTF-data")

    if "fvg" in df.columns:
        context["fvg"] = df["fvg"].iloc[-1]
    else:
        logger.warning("⚠️ FVG-kolom ontbreekt in HTF-data")

    if "sweep" in df.columns:
        context["sweep"] = df["sweep"].iloc[-1]
    else:
        logger.warning("⚠️ Sweep-kolom ontbreekt in HTF-data")

    return context
