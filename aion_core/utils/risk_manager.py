"""
📄 Bestand: risk_manager.py
🔍 Doel: Schat risk per trade en berekent TP op basis van RR
🧩 Gebruikt door: alle strategieën met calculate_rr()
📦 Behoort tot: aion_core/utils/
🧠 Verwacht implementatie van: pure Python
"""

def calculate_rr(entry: float, stop: float, rr: float = 2.0, direction: str = "long") -> float:
    """
    Bereken take-profit niveau op basis van RR-ratio
    """
    if entry <= 0 or stop <= 0 or rr <= 0:
        raise ValueError("Entry, stop en RR moeten positief zijn")

    risk = abs(entry - stop)

    if direction == "long":
        return entry + risk * rr
    elif direction == "short":
        return entry - risk * rr
    else:
        raise ValueError("Direction moet 'long' of 'short' zijn")
