"""
📄 Bestand: engine.py
🔍 Doel: Backtest engine die signalen genereert uit dataframe
🧩 Gebruikt door: main_backtest.py, strategy_executor
📦 Behoort tot: aion_core/backtest/
🧠 Verwacht implementatie van: StrategyInterface, logger
"""

from aion_core.utils.logger import logger


def run_engine(df, strategy, context_meta: dict = None) -> list:
    """
    Simuleert strategie door de dataframe van boven naar beneden te verwerken
    """
    if df is None or df.empty:
        logger.warning("⚠️ Lege dataframe ontvangen door engine.")
        return []

    results = []
    context_meta = context_meta or {}

    for i in range(50, len(df)):
        candles = df.iloc[i - 50:i].to_dict("records")

        context = {
            "symbol": context_meta.get("symbol", "unknown"),
            "timeframe": context_meta.get("timeframe", "15m"),
            "candles": candles
        }

        try:
            signal = strategy.generate_signal(context)
            if signal:
                results.append(signal)
        except Exception as e:
            logger.error(f"❌ Fout bij strategie-evaluatie op index {i}: {e}")

    logger.info(f"✅ Engine klaar. {len(results)} signalen gegenereerd.")
    return results
