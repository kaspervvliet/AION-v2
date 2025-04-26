
"""
📄 Bestand: aion_core/schedulers/candle_scheduler.py
🔍 Doel: Detecteren van nieuwe hogere timeframe candles en triggeren van HTF bias detectie.
"""

from datetime import datetime, timedelta
from aion_core.knowledge.htf_bias_checker import detect_htf_bias
from aion_core.utils.logger import log

_last_htf_bias_update = {
    "1h": None,
    "4h": None,
    "1d": None
}

def check_and_update_bias(candle_history, symbol, timeframe="1h"):
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
        log(f"Ongeldig timeframe voor bias update: {timeframe}", level="error")
        return

    last_update = _last_htf_bias_update.get(timeframe)

    if last_update is None or now - last_update >= candle_interval:
        # Nieuwe candle! ➔ Bias detecteren en loggen
        timestamp = now.isoformat()
        detect_htf_bias(candle_history, symbol, timestamp)
        _last_htf_bias_update[timeframe] = now
        log(f"HTF Bias herberekend voor timeframe {timeframe}.", level="info")
