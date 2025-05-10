"""
📄 Bestand: strategy_tester.py
🔍 Doel: Voert backtest uit en reflecteert op strategie-uitvoer
🧩 Gebruikt door: test_backtest.py, dev-tools
📦 Behoort tot: aion_core/eval/
🧠 Verwacht implementatie van: generate_signal(), RR, reflectie
"""

import logging
from typing import Any
from aion_core.database.supabase_writer import upload_backtest_results
from aion_core.eval.reflection import generate_reflection_prompt
from aion_core.modules.base_strategy import BaseStrategy

logger = logging.getLogger("AION")

def run_backtest(strategy: BaseStrategy, df, symbol="SOL/USDT") -> None:
    """Voert backtest uit over 1 candle op opgegeven strategie."""
    try:
        context = df.iloc[-1].to_dict()
        signal = strategy.generate_signal(context)

        if not all(k in signal for k in ["entry", "sl", "tp"]):
            logger.warning("❌ Backtest: SL/TP/Entry ontbreken — skipping.")
            return

        rr = strategy.calculate_rr(signal["entry"], signal["sl"], signal["tp"])

        if rr < 0.5:
            logger.info(f"⛔ R:R ongunstig: {rr:.2f} — skipping")
            return

        prompt = generate_reflection_prompt({
            "context": context,
            "setup": signal,
            "result": {"rr": rr, "success": rr >= 1.5}
        })

        payload = {
            "symbol": symbol,
            "entry": signal["entry"],
            "sl": signal["sl"],
            "tp": signal["tp"],
            "rr": rr,
            "reflection": prompt
        }

        upload_backtest_results(payload)
        logger.info("✅ Backtestresultaat opgeslagen in Supabase")

    except Exception as e:
        logger.error(f"❌ Backtest fout: {e}")

if __name__ == "__main__":
    class DummyStrategy(BaseStrategy):
        def generate_signal(self, market_context: dict[str, Any]) -> dict:
            return {"entry": 160.0, "sl": 158.0, "tp": 166.0}

    import pandas as pd
    df = pd.DataFrame({"bias": ["long"], "sweep": [False], "fvg": [True]})
    run_backtest(DummyStrategy(), df)
