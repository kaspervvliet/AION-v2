
## Bestand: aion_core/utils/risk_manager.py

"""
📄 Bestand: aion_core/utils/risk_manager.py
🔍 Doel: Dynamisch Stop Loss en Take Profit berekenen op basis van marktstructuur.
🧩 Gebruikt door: Alle strategie-modules
📦 Behoort tot: aion_core/utils
🧠 Verwacht implementatie van: marktstructuur analyse
"""

def calculate_sl(entry_price: float, market_structure: dict, direction: str) -> float:
    """
    Bepaal dynamische Stop Loss.

    Args:
        entry_price (float): De prijs waarop de positie wordt geopend.
        market_structure (dict): Structuurdata met laatste swing high en low.
        direction (str): 'long' of 'short'.

    Returns:
        float: Stop Loss prijs.
    """
    if direction == "long":
        sl = market_structure.get("last_swing_low", entry_price * 0.99)
    else:
        sl = market_structure.get("last_swing_high", entry_price * 1.01)

    return sl


def calculate_tp(entry_price: float, sl_price: float, risk_reward_ratio: float = 2.0, direction: str = "long") -> float:
    """
    Bepaal dynamische Take Profit op basis van gewenst risico/return verhouding.

    Args:
        entry_price (float): De prijs waarop de positie wordt geopend.
        sl_price (float): Berekende Stop Loss prijs.
        risk_reward_ratio (float, optional): RR-verhouding. Standaard 2.0.
        direction (str, optional): 'long' of 'short'.

    Returns:
        float: Take Profit prijs.
    """
    risk = abs(entry_price - sl_price)

    if direction == "long":
        tp = entry_price + (risk * risk_reward_ratio)
    else:
        tp = entry_price - (risk * risk_reward_ratio)

    return tp
