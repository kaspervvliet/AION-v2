"""
📄 Bestand: kernel.py
🔍 Doel: Evalueren van setups inclusief bias filtering
🧩 Gebruikt door: web_entry.py
📦 Behoort tot: AION v2
🧠 Verwacht implementatie van: analyse_market output
"""

class Decision:
    def __init__(self, status, confidence, reason):
        self.status = status  # GO / SKIP / CAUTION
        self.confidence = confidence
        self.reason = reason

def evaluate(setup):
    if setup.get("structure") == "error":
        return Decision(status="CAUTION", confidence=0, reason="Setup error")

    if not setup.get("bias_filter_passed", True):
        return Decision(status="SKIP", confidence=setup.get("confidence", 0), reason="Niet in lijn met HTF bias")

    if setup.get("confidence", 0) > 0.5:
        return Decision(status="GO", confidence=setup.get("confidence", 0), reason="Sterke structuur")

    return Decision(status="CAUTION", confidence=setup.get("confidence", 0), reason="Zwakke structuur")