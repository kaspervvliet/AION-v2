"""
📄 Bestand: context_manager.py
🔍 Doel: Maakt contextdict per timeframe voor evaluatie
🧩 Gebruikt door: backtest, strategie-evaluatie
📦 Behoort tot: aion_core/backtest/
🧠 Verwacht implementatie van: context per tf met bias, sweep, fvg etc.
"""

import logging
import pandas as pd
from typing import Dict, Any

logger = logging.getLogger("AION")

def create_context(df: pd.DataFrame, timeframe: str) -> Dict[str, Any]:
    """
    Genereert contextdict met relevante informatie per timeframe.
    Verwacht kolommen zoals 'bias', 'sweep', 'fvg_hit', etc.
    """
    if df.empty or not isinstance(df, pd.DataFrame):
        logger.warning(f"Lege of ongeldige DataFrame ontvangen voor {timeframe}.")
        return {}

    try:
        latest = df.iloc[-1].to_dict()
        logger.debug(f"Context voor {timeframe}: {latest}")
        return latest
    except Exception as e:
        logger.error(f"Fout bij aanmaken context voor {timeframe}: {e}")
        return {}

if __name__ == "__main__":
    # Dummy test
    df = pd.DataFrame({
        "bias": ["long"],
        "sweep": [True],
        "fvg_hit": [False],
    })
    ctx = create_context(df, "1H")
    print(ctx)
