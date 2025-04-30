from aion_core.utils import safe_io
from aion_core.performance.performance_tracker import PerformanceTracker
"""
📄 Bestand: run_backtest.py
🔍 Doel: Simpele runner om AION strategieën te backtesten met metrics, equity curve, drawdown en Kraken data support
🧩 Gebruikt door: ontwikkelaars
📦 Behoort tot: losse scripts / backtest tools
"""

import logging
import csv
import matplotlib.pyplot as plt
from aion_modules.rsi_sweep.strategy import Strategy
from aion_core.backtest.engine import BacktestEngine

# Setup logging
logging.basicConfig(level=logging.INFO)

def load_kraken_candles(filepath):
    """Laad historische candles vanuit een Kraken CSV bestand."""
    candles = []
    # replaced
# with open(filepath, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # sla header over
        for row in reader:
            timestamp = int(float(row[0]))
            open_price = float(row[1])
            high = float(row[2])
            low = float(row[3])
            close = float(row[4])
            volume = float(row[5])
            candles.append([timestamp, open_price, high, low, close, volume])
    return candles

# Kies welke candles je wilt gebruiken:
USE_KRAKEN_DATA = False  # Zet op True als je echte data wilt testen

if USE_KRAKEN_DATA:
    candles = load_kraken_candles('/path/to/your/kraken_candles.csv')
else:
    # Mock candles aanmaken
    candles = []
    open_price = 100
    for i in range(200):
        high = open_price * 1.01
        low = open_price * 0.99
        close = open_price * (1 + (0.002 if i % 10 == 0 else -0.002))
        volume = 100 + i
        candles.append([i, open_price, high, low, close, volume])
        open_price = close

# Strategie + Engine initialiseren
strategy = Strategy
engine = BacktestEngine(strategy_class=strategy, candles=candles, starting_balance=1000)

tracker = PerformanceTracker()

# Backtest draaien
engine.run()

# Resultaten tonen
print("\n--- Backtest Resultaten ---")
print(f"Aantal trades: {len(engine.trades)}")
print(f"Eindbalans: {engine.balance:.2f}")

if engine.trades:
    win_trades = [t for t in engine.trades if t['result'] == 'win']
    loss_trades = [t for t in engine.trades if t['result'] == 'loss']
    winrate = len(win_trades) / len(engine.trades) * 100
    avg_win = sum(t['exit_price'] - t['entry_price'] for t in win_trades) / len(win_trades) if win_trades else 0
    avg_loss = sum(t['exit_price'] - t['entry_price'] for t in loss_trades) / len(loss_trades) if loss_trades else 0
    expectancy = ((winrate/100) * avg_win) + ((1 - (winrate/100)) * avg_loss)

    print(f"Winrate: {winrate:.2f}%")
    print(f"Gemiddelde winst per winnende trade: {avg_win:.4f}")
    print(f"Gemiddelde verlies per verliezende trade: {avg_loss:.4f}")
    print(f"Expectancy per trade: {expectancy:.4f}")

    # Equity curve plotten + Drawdown analyse
    balance = 1000
    balance_over_time = [balance]
    peak = balance
    drawdowns = []

    for trade in engine.trades:
        pnl = trade['exit_price'] - trade['entry_price']
        balance += pnl
        balance_over_time.append(balance)
        peak = max(peak, balance)
        drawdown = (peak - balance) / peak
        drawdowns.append(drawdown)

    max_drawdown = max(drawdowns) * 100 if drawdowns else 0
    print(f"Max Drawdown: {max_drawdown:.2f}%")

    plt.figure(figsize=(10, 5))
    plt.plot(balance_over_time, marker='o')
    plt.title("AION Backtest Equity Curve")
    plt.xlabel("Aantal Trades")
    plt.ylabel("Balans ($)")
    plt.grid(True)
    plt.show()
else:
    print("Geen trades gemaakt.")


# Performance samenvatting loggen
for trade in engine.trades:
    signal = {
        "strategy_name": "BacktestStrategy",
        "action": "buy",  # Simplificatie
        "sl_pct": 0.01,
        "tp_pct": 0.02,
        "symbol": "SOL/USDT",
        "id": f"backtest-{trade['entry_time']}"
    }
    result = {
        "outcome": trade['result'],
        "rr_achieved": trade['rr'],
        "price": trade['entry_price'],
        "execution_time": trade['entry_time'],
        "duration": 60,  # Simplificatie voor backtest
        "balance": trade.get('balance', 1000)
    }
    tracker.log_trade(signal, result)
