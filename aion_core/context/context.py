"""
📄 Bestand: context.py
🔍 Doel: Beheert symbol/timeframe context en datastromen
🧩 Gebruikt door: kernel, strategieën, web_entry
📦 Behoort tot: aion_core/context
🧠 Verwacht implementatie van: fetch_latest_candle, get_latest_price, sync
"""

from aion_core.utils.safe_io import safe_load_json
from aion_core.utils.kraken import get_ohlc_latest

class AIONContext:
    def __init__(self, symbol: str, timeframe: str):
        self.symbol = symbol
        self.timeframe = timeframe
        self.candle_data = []

    def update_candles(self, new_candles):
        """Update candle data en sync met Supabase."""
        self.candle_data = new_candles
        self.push_to_supabase()

    def get_latest_price(self):
        """Geeft de laatste prijs van de huidige asset terug."""
        return self.candle_data[-1][4] if self.candle_data else None

    def fetch_latest_candle(self):
        """
        Haalt de laatste candle op voor de huidige symbol/timeframe.
        Retourneert 1 candle in [timestamp, open, high, low, close, volume]-formaat.
        """
        try:
            latest = get_ohlc_latest(self.symbol, self.timeframe)
            if latest and isinstance(latest, list) and len(latest[0]) == 6:
                return latest[0]
            else:
                raise ValueError(f"📛 Ongeldig candleformaat: {latest}")
        except Exception as e:
            from aion_core.utils.logger import logger
            logger.warning(f"[fetch_latest_candle] Fout bij ophalen: {e}")
            return None

    def push_to_supabase(self):
        """Dummy-implementatie voor Supabase sync (placeholder)."""
        pass
