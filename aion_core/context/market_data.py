from aion_core.indicators.kraken import fetch_ohlc

def get_candles(pair: str, interval: str = "15", limit: int = 150) -> list[dict]:
    raw = fetch_ohlc(pair, interval)
    if not raw or len(raw) < limit:
        raise ValueError(f"Niet genoeg candles opgehaald voor {pair} op {interval}m (gevonden: {len(raw)})")
    return raw[-limit:]

def get_htf_ltf_candles(pair: str) -> dict:
    return {
        "htf": get_candles(pair, interval="240", limit=200),  # 4H
        "mtf": get_candles(pair, interval="60", limit=200),   # 1H
        "ltf": get_candles(pair, interval="15", limit=200),   # 15m
    }