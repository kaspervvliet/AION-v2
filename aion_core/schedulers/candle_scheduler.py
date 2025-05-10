"""
📄 Bestand: aion_core/schedulers/candle_scheduler.py
🔍 Doel: Detecteren van nieuwe hogere timeframe candles en triggeren van HTF bias detectie.
🧩 Gebruikt door: morph_engine, signal_engine
📦 Behoort tot: aion_core/schedulers/
🧠 Verwacht implementatie van: check_and_update_bias()
"""

from datetime import datetime, timedelta
from typing import List, Dict
from aion_core.knowledge.htf_bias_checker import detect_htf_bias
from aion_core.utils.logger import log

_last_htf_bias_update = {
    "1h": None,
    "4h": None,
    "1d": None
}

def check_and_update_bias(candle_history: List[Dict], symbol: str, timeframe: str = "1h") -> None:
    """
    Controleert of een nieuwe hogere timeframe candle is gesloten en update bias.
    """
    now = datetime.utcnow()

    if timeframe == "1h":
        candle_interval = timedelta(hours=1)
    elif timeframe == "4h":
        candle_interval = timedelta(hours=4)
    elif timeframe == "1d":
        candle_interval = timedelta(days=1)
    else:
        log(f"❌ Ongeldig timeframe voor bias update: {timeframe}", level="error")
        return

    last_update = _last_htf_bias_update.get(timeframe)
    if last_update is None or now - last_update >= candle_interval:
        log(f"⏱️ HTF candle gesloten — bias wordt opnieuw berekend voor {timeframe}")
        detect_htf_bias(candle_history, symbol, timeframe)
        _last_htf_bias_update[timeframe] = now

if __name__ == "__main__":
    test_history = [{"close": 160, "timestamp": "2024-05-01T12:00:00Z"}]
    check_and_update_bias(test_history, "SOL/USDT", "1h")
