"""
📄 Bestand: trade_explainer.py
🔍 Doel: Genereert tekstuele uitleg over een tradingbesluit op basis van SMC-principes
🧩 Gebruikt door: evaluator, dashboard
📦 Behoort tot: aion_core/kernel/
🧠 Verwacht implementatie van: explain_decision()
"""

import logging
from typing import Dict
from aion_core.knowledge.concepts import concepts

logger = logging.getLogger("AION")

def explain_decision(setup: Dict, decision: str, confidence: float, reason: str) -> str:
    bias = setup.get("bias")
    rsi = setup.get("rsi")
    fvg = setup.get("has_fvg")
    bos = setup.get("has_bos")
    choch = setup.get("has_choch")

    uitleg = f"Beslissing: {decision} ({confidence:.2f})\n"
    uitleg += f"Reden: {reason}\n"

    concept_keys = []
    if bias: concept_keys.append("bias")
    if fvg: concept_keys.append("fair value gap")
    if bos: concept_keys.append("bos")
    if choch: concept_keys.append("choch")
    if rsi is not None: concept_keys.append("rsi")

    for key in concept_keys:
        concept = next((c for c in concepts if c["naam"] == key), None)
        if concept:
            uitleg += f"\n🔹 *{concept['naam'].capitalize()}* — {concept['uitleg']}"
        else:
            logger.warning(f"Concept '{key}' niet gevonden in kennisbank")

    return uitleg

if __name__ == "__main__":
    fake_setup = {"bias": "long", "rsi": 42, "has_bos": True, "has_choch": False, "has_fvg": True}
    result = explain_decision(fake_setup, "LONG", 3.2, "bias + fvg + bos")
    print(result)
