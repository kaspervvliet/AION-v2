"""
📄 Bestand: analyse_bos_choc.py
🔍 Doel: Detecteren van Break of Structure (BOS) en Change of Character (CHoCH) op lage timeframes
🧩 Gebruikt door: analyse_market()
📦 Behoort tot: AION V2 Core uitbreidingen
🧠 Verwacht input: lijst van recente candles
"""

def analyse_bos_choc(candles, direction='bullish', lookback=20):
    """
    Detecteert BOS/CHoCH gebaseerd op recentste candles.

    Args:
        candles (list): Candlelist [[timestamp, open, high, low, close, volume], ...]
        direction (str): Verwachte hoofdrichting ('bullish' of 'bearish')
        lookback (int): Aantal candles om terug te kijken

    Returns:
        dict: {'bos': bool, 'choc': bool}
    """
    if len(candles) < lookback:
        return {'bos': False, 'choc': False}

    recent = candles[-lookback:]

    highs = [float(c[2]) for c in recent]  # high prijzen
    lows = [float(c[3]) for c in recent]   # low prijzen

    highest_high = max(highs)
    lowest_low = min(lows)

    current_close = float(recent[-1][4])

    bos = False
    choc = False

    if direction == 'bullish':
        if current_close > highest_high:
            bos = True
        if current_close < lowest_low:
            choc = True

    elif direction == 'bearish':
        if current_close < lowest_low:
            bos = True
        if current_close > highest_high:
            choc = True

    return {'bos': bos, 'choc': choc}