
from aion_core.knowledge.concepts import concepts

def explain_decision(setup: dict, decision: str, confidence: float, reason: str) -> str:
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
            uitleg += f"\n🔹 *{concept['naam'].capitalize()}* — {concept['definitie']}"

    return uitleg
