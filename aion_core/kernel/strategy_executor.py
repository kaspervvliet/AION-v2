"""
📄 Bestand: strategy_executor.py
🔍 Doel: Strategie-evaluatie uitvoeren (validate, signal, build)
🧩 Gebruikt door: kernel.py, backtest_engine, streamlit_ui
📦 Behoort tot: aion_core/kernel
🧠 Verwacht implementatie van: StrategyInterface + context
"""

from aion_core.strategy_pool_initializer import load_strategies
from aion_core.context.context_manager import AionContext
import pandas as pd

strategies = load_strategies()

def evaluate_all(df: pd.DataFrame, context: AionContext):
    results = []
    for strat in strategies:
        try:
            if not strat.validate_market(df):
                continue
            signal = strat.generate_signal(df, context)
            if signal is None:
                continue
            trade = strat.build_trade(signal, df)
            if trade:
                results.append({
                    "strategy": strat.name,
                    "trade": trade,
                    "signal": signal
                })
        except Exception as e:
            print(f"[{strat.name}] Strategiecrash: {e}")
    return results

if __name__ == "__main__":
    from aion_core.utils.kraken import get_recent_ohlc
    df = get_recent_ohlc("SOL/USDT", interval="15m")
    ctx = AionContext(df)
    trades = evaluate_all(df, ctx)
    print(trades)
