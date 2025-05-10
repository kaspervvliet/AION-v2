"""
📄 Bestand: concepts.py
🔍 Doel: Bevat definities van SMC-concepten met uitleg
🧩 Gebruikt door: trade_explainer, reflection_engine
📦 Behoort tot: aion_core/knowledge/
🧠 Verwacht implementatie van: conceptbank als statische list
"""

from typing import List, Dict

concepts: List[Dict[str, str]] = [
    {
        "naam": "bias",
        "uitleg": "De verwachte richting van de markt, gebaseerd op hogere timeframe analyse."
    },
    {
        "naam": "fair value gap",
        "uitleg": "Een prijsgebied waar onevenwichtigheid is ontstaan tussen vraag en aanbod."
    },
    {
        "naam": "bos",
        "uitleg": "Break of Structure: duidt op een mogelijke voortzetting van trend."
    },
    {
        "naam": "choch",
        "uitleg": "Change of Character: indicatie voor potentiële trendomslag."
    },
    {
        "naam": "rsi",
        "uitleg": "Relative Strength Index: meet sterkte/snelheid van prijsbeweging."
    }
]

if __name__ == "__main__":
    for c in concepts:
        print(f"🔹 {c['naam']}: {c['uitleg']}")
