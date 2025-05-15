
"""
📄 Bestand: context_engine.py
🔍 Doel: Centrale contextuele detecties voor SMC (BOS, CHoCH, FVG, etc.)
🧩 Gebruikt door: strategieën, executor, reflectie
📦 Behoort tot: aion_core/context/
🧠 Verwacht implementatie van: detect_market_structure
"""

from typing import List, Dict
from aion_core.context.market_structure import detect_market_structure

def detect_bos(candles: List[Dict], direction: str = "bullish") -> bool:
    """
    Detecteert Break of Structure (BOS) op basis van directionele voorkeur.
    """
    structure = detect_market_structure(candles)
    if direction == "bullish":
        return structure.get("bos_up", False)
    elif direction == "bearish":
        return structure.get("bos_down", False)
    return False

def detect_choch(candles: List[Dict]) -> bool:
    """
    Detecteert Change of Character (CHoCH) in prijsstructuur.
    """
    structure = detect_market_structure(candles)
    return structure.get("choc", False)
