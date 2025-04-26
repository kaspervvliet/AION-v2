"""
📄 Bestand: strategy.py
🔍 Doel: Trading strategie gebaseerd op RSI-sweeps + MTF Bias validatie
🧩 Gebruikt door: backtest engine, live trading modules
📦 Behoort tot: aion_modules/rsi_sweep/
🧠 Verwacht implementatie van: candle data input + bias control
"""

from aion_core.mtf_bias_checker import is_bias_aligned

class Strategy:
    def __init__(self):
        pass

    def is_entry(self, window, htf_candles=None):
        """
        Bepaal of er een entry mogelijkheid is.

        Args:
            window (list): Laatste 20 candles (15M timeframe)
            htf_candles (list): Higher timeframe candles (1H timeframe)

        Returns:
            bool: True als er een entry mogelijkheid is
        """
        if htf_candles is None or not is_bias_aligned(htf_candles, window):
            return False

        closes = [candle[4] for candle in window]

        if len(closes) < 2:
            return False

        if closes[-1] > closes[-2]:
            return True

        return False