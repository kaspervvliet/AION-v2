
## Bestand: aion_core/knowledge/structure_awareness.py

"""
📄 Bestand: aion_core/knowledge/structure_awareness.py
🔍 Doel: Detecteren van breaker blocks, shifts in market structure (BOS/CHoCH) en entry blokkeren bij structurele risico's.
🧩 Gebruikt door: Alle strategie-modules
📦 Behoort tot: aion_core/knowledge
🧠 Verwacht implementatie van: marktdata analyse
"""

def detect_breaker_blocks(market_data: dict) -> bool:
    """
    Detecteert breaker block situaties (oude support wordt weerstand, of andersom).
    """
    previous_support = market_data.get("previous_support")
    current_price = market_data.get("close")

    if previous_support and current_price < previous_support:
        return True  # Onder support gebroken ➔ weerstand

    return False


def detect_bos_shifts(market_data: dict) -> bool:
    """
    Detecteert Break of Structure (BOS) of Change of Character (CHoCH).
    """
    last_high = market_data.get("last_high")
    last_low = market_data.get("last_low")
    current_price = market_data.get("close")

    if last_high and current_price > last_high:
        return True  # Bullish BOS
    if last_low and current_price < last_low:
        return True  # Bearish BOS

    return False


def should_block_entry(market_data: dict) -> bool:
    """
    Bepaalt of een entry moet worden geblokkeerd vanwege structurele risico's.
    """
    if detect_breaker_blocks(market_data):
        return True
    if detect_bos_shifts(market_data):
        return True

    return False
