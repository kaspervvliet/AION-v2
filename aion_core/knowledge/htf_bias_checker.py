
"""
📄 Bestand: htf_bias_checker.py
🔍 Doel: Detecteert HTF-bias (1h/4h/daily) obv MA20 vs MA50
🧩 Gebruikt door: kernel, bias_logger
📦 Behoort tot: aion_core/knowledge
🧠 Logt bias via Supabase
"""

from aion_core.database.supabase_logger import log_bias_state

def infer_timeframe(candle_history):
    if len(candle_history) < 2:
        return "unknown"
    delta = candle_history[1]["timestamp"] - candle_history[0]["timestamp"]
    if delta == 900:
        return "15m"
    elif delta == 3600:
        return "1h"
    elif delta == 14400:
        return "4h"
    elif delta == 86400:
        return "1d"
    return "unknown"

def detect_htf_bias(candle_history, symbol, timestamp):
    closes = [c["close"] for c in candle_history]

    if len(closes) < 50:
        return None

    ma20 = sum(closes[-20:]) / 20
    ma50 = sum(closes[-50:]) / 50

    if ma20 > ma50:
        bias = "bullish"
    elif ma20 < ma50:
        bias = "bearish"
    else:
        bias = "neutral"

    timeframe = infer_timeframe(candle_history)
    log_bias_state(symbol=symbol, timeframe=timeframe, bias=bias, timestamp=timestamp)
    return bias
