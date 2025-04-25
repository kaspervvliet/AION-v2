"""
📄 Bestand: context.py
🔍 Doel: Beheert symbol/timeframe context en analyse
🧩 Gebruikt door: kernel, strategieën, web_entry
📦 Behoort tot: aion_core/context
🧠 Verwacht implementatie van: analyse_market, fetch_latest_candle, get_latest_price
"""

from aion_core.utils.safe_io import read_json_file
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
            if latest and isinstance(latest, list) and len(latest) == 6:
                return latest
            else:
                from aion_core.utils.logger import logger
                logger.warning(f"[fetch_latest_candle] Ongeldig candleformaat: {latest}")
                return None
        except Exception as e:
            from aion_core.utils.logger import logger
            logger.warning(f"[fetch_latest_candle] Fout bij ophalen: {e}")
            return None

    def push_to_supabase(self):
        """Dummy-implementatie voor Supabase sync (placeholder)."""
        pass

def analyse_market(candle):
    """
    Analyseert een enkele candle en retourneert een SMC-achtige setup.
    :param candle: List [timestamp, open, high, low, close, volume]
    :return: dict met entry setup parameters
    """
    if not candle or len(candle) != 6:
        raise ValueError("Ongeldige candle-input voor analyse")

    _, o, h, l, c, v = candle

    direction = "LONG" if c > o else "SHORT"
    body = abs(c - o)
    wick = (h - l) - body

    setup = {
        "direction": direction,
        "body_size": round(body, 4),
        "wick_size": round(wick, 4),
        "entry_zone": (l, h) if direction == "LONG" else (h, l),
        "risk_reward": 2.0,
        "confidence": 0.65 if wick < body else 0.45,
        "structure": "impulse" if body > wick else "choppy",
        "source": "analyse_market"
    }
    return setup
