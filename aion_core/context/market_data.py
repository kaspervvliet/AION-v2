"""
📄 Bestand: market_data.py
🔍 Doel: Genereert contextdict uit df voor strategie-evaluatie
🧩 Gebruikt door: backtest, kernel, context_builder
📦 Behoort tot: aion_core/context/
🧠 Verwacht implementatie van: pandas
"""

import pandas as pd
from aion_core.utils.logger import logger


def generate_context(df: pd.DataFrame, symbol: str, timeframe: str) -> dict:
    required = {"open", "high", "low", "close"}
    if not required.issubset(df.columns):
        logger.error(f"❌ Vereiste kolommen ontbreken: {required - set(df.columns)}")
        return {}

    if len(df) < 20:
        logger.warning("⚠️ Te weinig candles voor contextgeneratie")
        return {}

    context = {
        "symbol": symbol,
        "timeframe": timeframe,
        "candles": df.tail(50).to_dict(orient="records"),
    }

    if not context["candles"]:
        logger.warning("⚠️ Lege candles in context")
    return context
