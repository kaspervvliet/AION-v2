
## Bestand: aion_core/indicators/volatility_analyzer.py

"""
📄 Bestand: aion_core/indicators/volatility_analyzer.py
🔍 Doel: Volatiliteit meten (ATR) en risk parameters aanpassen op basis van marktconditie.
🧩 Gebruikt door: Strategie-modules
📦 Behoort tot: aion_core/indicators
🧠 Verwacht implementatie van: ATR berekening
"""

def calculate_atr(candle_data: list, period: int = 14) -> float:
    """
    Bereken de Average True Range (ATR) over een periode.
    """
    if len(candle_data) < period + 1:
        return 0.0  # Niet genoeg data

    trs = []
    for i in range(1, period + 1):
        high = candle_data[-i]["high"]
        low = candle_data[-i]["low"]
        prev_close = candle_data[-i-1]["close"]

        tr = max(high - low, abs(high - prev_close), abs(low - prev_close))
        trs.append(tr)

    atr = sum(trs) / period
    return atr


def assess_volatility(atr_value: float, high_threshold: float, low_threshold: float) -> str:
    """
    Bepaal of de volatiliteit hoog, normaal of laag is.
    """
    if atr_value > high_threshold:
        return "high"
    if atr_value < low_threshold:
        return "low"
    return "normal"


def adjust_risk_parameters(base_sl: float, base_tp: float, volatility_label: str) -> tuple:
    """
    Pas SL en TP aan afhankelijk van volatiliteit.
    """
    if volatility_label == "high":
        return base_sl * 1.5, base_tp * 1.5  # Wijder SL/TP
    elif volatility_label == "low":
        return base_sl * 0.8, base_tp * 0.8  # Strakkere SL/TP
    else:
        return base_sl, base_tp
