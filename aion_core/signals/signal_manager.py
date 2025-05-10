"""
📄 Bestand: signal_manager.py
🔍 Doel: Signaalgeneratie, evaluatie en voorbereiding op executie
🧩 Gebruikt door: main_live, backtest, adaptive_strategy_selector
📦 Behoort tot: aion_core/signals/
🧠 Vervangt: signal_generator.py, signal_evaluator.py
"""

from datetime import datetime
from typing import Any, Dict
import logging

logger = logging.getLogger("AION")

class SignalManager:
    def __init__(self):
        self.generated_signals = []

    def generate_signal(self, context: Dict[str, Any], strategy: Any) -> Dict[str, Any]:
        """
        Genereert een trading signaal vanuit de gegeven strategie.
        """
        signal = strategy.generate_signal(context)
        if signal:
            signal["created_at"] = datetime.utcnow().isoformat()
            self.generated_signals.append(signal)
            logger.info("📤 Nieuw signaal gegenereerd")
        else:
            logger.warning("⚠️ Geen signaal gegenereerd door strategie")
        return signal

    def evaluate_signal(self, signal: Dict[str, Any]) -> bool:
        """
        Evalueert of het signaal geldig en bruikbaar is.
        """
        if not signal:
            logger.warning("❌ Ongeldig of leeg signaal bij evaluatie")
            return False

        # Toekomstige checks: age, price drift, liquidity, mute-mode etc.
        return True

if __name__ == "__main__":
    class DummyStrategy:
        def generate_signal(self, ctx):
            return {"entry": 160, "sl": 155, "tp": 165}

    mgr = SignalManager()
    ctx = {"bias": "long", "fvg": True}
    sig = mgr.generate_signal(ctx, DummyStrategy())
    print("Gegenereerd:", sig)
    print("✅ Geldig:", mgr.evaluate_signal(sig))
