"""
📄 Bestand: strategy.py
🔍 Doel: Trading strategie gebaseerd op RSI-sweeps + Weighted MTF Bias validatie
🧩 Gebruikt door: backtest engine, live trading modules
📦 Behoort tot: aion_modules/rsi_sweep/
🧠 Verwacht implementatie van: candle data input + weighted bias control
"""

from aion_core.weighted_bias_analyzer import calculate_weighted_bias

class Strategy:
    def __init__(self):
        pass

    def is_entry(self, window, daily_candles=None, fourh_candles=None, oneh_candles=None):
        """
        Bepaal of er een entry mogelijkheid is.

        Args:
            window (list): Laatste 20 candles (15M timeframe)
            daily_candles (list): 1D timeframe candles
            fourh_candles (list): 4H timeframe candles
            oneh_candles (list): 1H timeframe candles

        Returns:
            bool: True als er een entry mogelijkheid is
        """
        if daily_candles is None or fourh_candles is None or oneh_candles is None:
            return False

        overall_bias = calculate_weighted_bias(daily_candles, fourh_candles, oneh_candles)

        if overall_bias != "bullish":
            return False

        closes = [candle[4] for candle in window]

        if len(closes) < 2:
            return False

        if closes[-1] > closes[-2]:
            return True

        return False