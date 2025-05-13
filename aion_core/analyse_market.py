"""
📄 Bestand: analyse_market.py
🔍 Doel: Marktstructuur analyseren (BOS/CHoCH) via wrapper
🧩 Gebruikt door: main.py
📦 Behoort tot: /
🧠 Verwacht implementatie van: analyse_bos_choc.detect_market_structure
"""

import logging
from analyse_bos_choc import detect_market_structure

logger = logging.getLogger("AION")

def analyse_market(df, bias=None):
    if df is None or df.empty:
        logger.warning("Lege dataframe ontvangen in analyse_market().")
        return {}

    result = detect_market_structure(df)
    if not result:
        logger.info("Geen marktstructuur gedetecteerd.")
    return result

if __name__ == "__main__":
    import pandas as pd
    # Dummy test
    data = pd.DataFrame({"high": [1, 2, 3], "low": [0.5, 1, 1.5], "close": [0.8, 1.8, 2.5]})
    print(analyse_market(data))