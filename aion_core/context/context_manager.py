
"""
📄 Bestand: context_manager.py
🔍 Doel: Beheer van contextstructuur, updates en validatie
🧩 Gebruikt door: main_live, adaptive_strategy_selector
📦 Behoort tot: aion_core/context/
🧠 Vervangt: context.py, context_updater.py, context_validator.py
"""

from datetime import datetime

class ContextManager:
    def __init__(self):
        self.context = {
            "bias_1h": None,
            "bias_4h": None,
            "bias_1d": None,
            "structure": None,
            "sweep_detected": False,
            "rsi_divergence": False,
            "volume_spike": False,
            "atr": None,
            "adx": None,
            "last_updated": None
        }

    def update(self, updates: dict):
        for key, value in updates.items():
            if key in self.context:
                self.context[key] = value
        self.context["last_updated"] = datetime.utcnow().isoformat()

    def validate(self) -> bool:
        required_keys = ["bias_1h", "bias_4h", "bias_1d", "structure"]
        for key in required_keys:
            if self.context.get(key) is None:
                print(f"[Context Validation] Missing value for {key}")
                return False
        return True

    def get_context(self):
        return self.context

    def reset(self):
        for key in self.context:
            self.context[key] = None
        self.context["sweep_detected"] = False
        self.context["rsi_divergence"] = False
        self.context["volume_spike"] = False

# Voorbeeld gebruik
if __name__ == "__main__":
    cm = ContextManager()
    cm.update({"bias_1h": "bullish", "structure": "consolidation"})
    if cm.validate():
        print(cm.get_context())
