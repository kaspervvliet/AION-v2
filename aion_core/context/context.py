
from aion_core.utils.kraken import get_ohlc_data

def fetch_candles_from_kraken(interval: str = "15", pair: str = "SOLUSDT"):
    """
    Haalt OHLC-data op van Kraken API voor een bepaalde interval en trading pair.
    """
    candles = get_ohlc_data(interval=interval, pair=pair)
    return candles

def fetch_latest_candle(interval: str = "15", pair: str = "SOLUSDT"):
    """
    Retourneert de meest recente candle uit de opgehaalde set.
    """
    candles = fetch_candles_from_kraken(interval=interval, pair=pair)
    return candles[-1] if candles else None
