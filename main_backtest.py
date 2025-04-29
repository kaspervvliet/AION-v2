
"""
📄 Bestand: main_backtest.py
🔍 Doel: Uitvoeren van een backtest run met AION strategieën op historische candles
🧩 Gebruikt door: ontwikkelaars
📦 Behoort tot: losse backtest runners
🧠 Verwacht implementatie van: ContextManager, SignalManager, execute_signal
"""

import logging
from aion_core.backtest.engine import BacktestEngine
from aion_modules.strategies.rsi_sweep import Strategy as DefaultStrategy
from aion_core.utils.safe_io import safe_read_json
from aion_core.performance.performance_tracker import PerformanceTracker

# Logging configureren
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_mock_candles():
    """Genereer eenvoudige mock candles voor testdoeleinden."""
    candles = []
    open_price = 100
    for i in range(250):
        high = open_price * 1.01
        low = open_price * 0.99
        close = open_price * (1 + (0.002 if i % 8 == 0 else -0.002))
        volume = 100 + i
        candles.append([i, open_price, high, low, close, volume])
        open_price = close
    return candles

def main():
    logger.info("[BACKTEST] Initialiseren van backtest...")

    # Laad candles
    candles = load_mock_candles()

    # Initialiseer BacktestEngine
    strategy = DefaultStrategy
    engine = BacktestEngine(strategy_class=strategy, candles=candles, starting_balance=1000)

    # Initialiseer Performance Tracker
    tracker = PerformanceTracker()

    # Run de backtest
    engine.run()

    # Log resultaten
    logger.info("\n--- Backtest Resultaten ---")
    logger.info(f"Aantal trades: {len(engine.trades)}")
    logger.info(f"Eindbalans: {engine.balance:.2f} USD")

    # Log individuele trades
    for trade in engine.trades:
        signal = {
            "strategy_name": "RSI_Sweep",
            "action": "buy",  # Simplificatie
            "symbol": "SOL/USDT",
            "id": f"backtest-{trade['entry_time']}"
        }
        result = {
            "outcome": trade['result'],
            "rr_achieved": trade['rr'],
            "price": trade['entry_price'],
            "execution_time": trade['entry_time'],
            "duration": 60,
            "balance": trade.get('balance', 1000)
        }
        tracker.log_trade(signal, result)

if __name__ == "__main__":
    main()
