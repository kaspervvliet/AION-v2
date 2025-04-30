
"""
📄 Bestand: self_monitor.py
🔍 Doel: Detecteren van interne anomalieën tijdens live trading
🧩 Gebruikt door: main_live, kernel
📦 Behoort tot: aion_core/debug
🧠 Detecteert o.a. bias mismatches, onrealistische RR, verliesreeksen
"""

from typing import List, Dict

def check_system_health(context: dict, trades: List[dict], bias: str) -> List[str]:
    alerts = []

    # Check 1: Laatste 10 trades allemaal verlies
    if len(trades) >= 10:
        last_10 = trades[-10:]
        losses = [t for t in last_10 if t.get("outcome") == "loss"]
        if len(losses) == 10:
            alerts.append("⚠️ 10 verliestrades op rij! Mogelijk marktconditie gewijzigd.")

    # Check 2: Abnormale R:R ratio
    for trade in trades[-5:]:
        rr = trade.get("rr_achieved", 0)
        if rr > 5.0:
            alerts.append(f"❗ Onrealistische RR gedetecteerd: {rr:.2f}")

    # Check 3: Bias mismatch met context
    structure = context.get("structure", {})
    if structure.get("trend") and bias and structure["trend"] != bias:
        alerts.append("⚠️ Bias mismatch met trendstructuur in context.")

    # Check 4: Zeer laag volume
    if context.get("volume") is not None and context["volume"] < 20:
        alerts.append("🔕 Laag volume: mogelijk illiquide markt.")

    return alerts
