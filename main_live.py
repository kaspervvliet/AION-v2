from aion_core.context.context import AIONContext
from aion_core.context.market_data import get_htf_ltf_candles

def live_loop():
    pair = "SOL/USDT"
    candles = get_htf_ltf_candles(pair)
    ltf = candles["ltf"]
    latest_candle = ltf[-1]

    print("🔁 Laatste 15m candle (live loop):", latest_candle)