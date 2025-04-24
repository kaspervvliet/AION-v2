"""
📄 Bestand: entry_helpers.py
🔍 Doel: Hulpfuncties voor RSI Sweep entrycondities
🧩 Gebruikt door: strategy.py binnen rsi_sweep module
📦 Behoort tot: aion_modules/rsi_sweep/
"""

def simulate_rsi(candles):
    """Simuleert een RSI waarde voor testdoeleinden."""
    if not candles or len(candles) < 5:
        return 50
    close = candles[-1][4]
    prev = candles[-5][4]
    delta = close - prev
    return 30 if delta < 0 else 60

def detect_sweep(candles):
    """Dummy sweepdetectie: check of laatste low lager is dan de 3 ervoor."""
    if len(candles) < 4:
        return False
    last_low = candles[-1][3]
    return all(last_low < candles[-i][3] for i in range(2, 5))