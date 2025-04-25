"""
📄 Bestand: context.py
🔍 Doel: Contextmanagement voor symbol, timeframe, candles
🧩 Gebruikt door: kernel, strategieën, web_entry
📦 Behoort tot: aion_core/context
🧠 Werkt met dict-based candles + Supabase logging
"""

from aion_core.utils.safe_io import read_json_file
from aion_core.utils.kraken import get_ohlc_latest
from aion_core.utils.logger import logger
from aion_core.supabase_client import log_signal

class AIONContext:
    def __init__(self, symbol: str, timeframe: str):
        self.symbol = symbol
        self.timeframe = timeframe
        self.candle_data = []

    def update_candles(self, new_candles):
        self.candle_data = new_candles
        self.push_to_supabase()

    def get_latest_price(self):
        return self.candle_data[-1]['close'] if self.candle_data else None

    def fetch_latest_candle(self):
        try:
            latest = get_ohlc_latest(self.symbol, self.timeframe)
            if latest and isinstance(latest, dict) and 'close' in latest:
                return latest
            else:
                logger.warning(f"[fetch_latest_candle] Ongeldig candleformaat: {latest}")
                return None
        except Exception as e:
            logger.warning(f"[fetch_latest_candle] Fout bij ophalen: {e}")
            return None

    def push_to_supabase(self):
        if not self.candle_data:
            return
        last = self.candle_data[-1]
        try:
            log_signal({
                "symbol": self.symbol,
                "timeframe": self.timeframe,
                "timestamp": int(last["time"]),
                "price": float(last["close"]),
                "note": "auto-push candle"
            })
        except Exception as e:
            logger.warning(f"[Supabase push] Mislukt: {e}")

def analyse_market(candle):
    """
    Analyseert een enkele candle en retourneert een setup dict.
    :param candle: dict met keys zoals open, high, low, close, volume
    :return: dict met setup-informatie
    """
    if not candle or not all (k in candle for k in ["open", "high", "low", "close"]):
        raise ValueError("Ongeldige candle-input voor analyse")

    o = candle['open']
    h = candle['high']
    l = candle['low']
    c = candle['close']

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
        "source": "analyse_market",
        "symbol": candle.get("symbol", "UNKNOWN"),
        "timeframe": candle.get("timeframe", "15m"),
        "timestamp": int(candle.get("time", 0))
    }
    return setup
