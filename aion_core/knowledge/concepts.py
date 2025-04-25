"""
📄 Bestand: concepts.py
🔍 Doel: [AUTO-GEGENEREERD: controleer doel handmatig]
🧩 Gebruikt door: onbekend
📦 Behoort tot: aion_core
🧠 Laatst geüpdatet: 2025-04-25
"""


### aion_core/knowledge/concepts.py ###

concepts = [
    {"naam": "candle", "categorie": "prijsactie", "definitie": "Een candle geeft de open/high/low/close van een tijdseenheid weer.", "gebruik_in_strategie": True, "relevantie_per_tijdframe": ["15m", "1H", "4H"], "log_in_dashboard": False},
    {"naam": "sweep", "categorie": "prijsactie", "definitie": "Doorschieten van een high/low om liquiditeit op te halen.", "gebruik_in_strategie": True, "relevantie_per_tijdframe": ["15m", "1H"], "log_in_dashboard": True},
    {"naam": "choch", "categorie": "market structure", "definitie": "Change of Character — een structurele omslag.", "gebruik_in_strategie": True, "relevantie_per_tijdframe": ["15m", "1H"], "log_in_dashboard": True},
    {"naam": "bos", "categorie": "market structure", "definitie": "Break of Structure — bevestigt richting.", "gebruik_in_strategie": True, "relevantie_per_tijdframe": ["15m", "1H"], "log_in_dashboard": True},
    {"naam": "internal structure", "categorie": "market structure", "definitie": "Substructuur binnen grotere swing highs/lows.", "gebruik_in_strategie": False, "relevantie_per_tijdframe": ["15m"], "log_in_dashboard": False},
    {"naam": "bias", "categorie": "contextueel", "definitie": "Verwachte richting op basis van hogere tijdframes.", "gebruik_in_strategie": True, "relevantie_per_tijdframe": ["1H", "4H", "1D"], "log_in_dashboard": True},
    {"naam": "orderblock", "categorie": "smart money", "definitie": "Laatste bullish/bearish candle voor een impuls.", "gebruik_in_strategie": True, "relevantie_per_tijdframe": ["1H", "4H"], "log_in_dashboard": True},
    {"naam": "mitigation", "categorie": "smart money", "definitie": "Herbezoek van orderblock of FVG voor nieuwe richting.", "gebruik_in_strategie": True, "relevantie_per_tijdframe": ["15m", "1H"], "log_in_dashboard": False},
    {"naam": "breaker block", "categorie": "smart money", "definitie": "Falen van OB dat verandert in een setup trigger.", "gebruik_in_strategie": False, "relevantie_per_tijdframe": ["1H"], "log_in_dashboard": False},
    {"naam": "rsi", "categorie": "indicator", "definitie": "Relative Strength Index — meet momentum.", "gebruik_in_strategie": True, "relevantie_per_tijdframe": ["15m"], "log_in_dashboard": True},
    {"naam": "divergence", "categorie": "indicator", "definitie": "RSI/MACD divergeert van prijs, duidt mogelijk reversal.", "gebruik_in_strategie": False, "relevantie_per_tijdframe": ["15m", "1H"], "log_in_dashboard": False},
    {"naam": "fair value gap", "categorie": "inefficiëntie", "definitie": "Een zone zonder trade tussen 2 candles, vaak gevuld.", "gebruik_in_strategie": True, "relevantie_per_tijdframe": ["15m", "1H"], "log_in_dashboard": True},
    {"naam": "imbalance", "categorie": "inefficiëntie", "definitie": "Structurele onbalans in orderflow, vaak in FVG.", "gebruik_in_strategie": True, "relevantie_per_tijdframe": ["1H", "4H"], "log_in_dashboard": False},
    {"naam": "rr", "categorie": "risk management", "definitie": "Risk-to-reward ratio.", "gebruik_in_strategie": True, "relevantie_per_tijdframe": ["alle"], "log_in_dashboard": True},
    {"naam": "tp/sl", "categorie": "risk management", "definitie": "Take profit en stop loss.", "gebruik_in_strategie": True, "relevantie_per_tijdframe": ["alle"], "log_in_dashboard": True},
    {"naam": "confluence", "categorie": "strategie", "definitie": "Wanneer meerdere signalen samenvallen voor validatie.", "gebruik_in_strategie": True, "relevantie_per_tijdframe": ["alle"], "log_in_dashboard": True},
    {"naam": "confirmation", "categorie": "strategie", "definitie": "Extra structuur of signaal dat een setup valideert.", "gebruik_in_strategie": True, "relevantie_per_tijdframe": ["15m", "1H"], "log_in_dashboard": True},
    {"naam": "invalidatie", "categorie": "strategie", "definitie": "Wanneer een setup ongeldig wordt (bv. sweep in verkeerde richting).", "gebruik_in_strategie": True, "relevantie_per_tijdframe": ["15m"], "log_in_dashboard": False}
]
