
"""
📄 Bestand: signal_manager.py
🔍 Doel: Signaalgeneratie, evaluatie en voorbereiding op executie
🧩 Gebruikt door: main_live, backtest, adaptive_strategy_selector
📦 Behoort tot: aion_core/signals/
🧠 Vervangt: signal_generator.py, signal_evaluator.py
"""

from datetime import datetime

class SignalManager:
    def __init__(self):
        self.generated_signals = []

    def generate_signal(self, context: dict, strategy) -> dict:
        """
        Gebaseerd op de gegeven strategie en context genereer je een trading signaal.
        """
        signal = strategy.generate_signal(context)
        if signal:
            signal["created_at"] = datetime.utcnow().isoformat()
            self.generated_signals.append(signal)
        return signal

    def evaluate_signal(self, signal: dict) -> bool:
        """
        Evalueer of een signaal nog geldig is op basis van eenvoudige validatie.
        """
        if signal is None:
            return False

        # Placeholder voor complexere evaluatie logica
        required_keys = ["symbol", "setup_name", "expected_rr", "entry_price"]
        for key in required_keys:
            if key not in signal:
                print(f"[Signal Evaluation] Missing key: {key}")
                return False

        return True

    def get_all_signals(self):
        return self.generated_signals

    def reset(self):
        self.generated_signals = []

# Voorbeeld gebruik
if __name__ == "__main__":
    sm = SignalManager()

    # Mock strategy object met generate_signal functie
    class MockStrategy:
        def generate_signal(self, context):
            return {"symbol": "SOL/USDT", "setup_name": "RSI Sweep", "expected_rr": 2.5, "entry_price": 88.5}

    strategy = MockStrategy()
    context = {"structure": "consolidation", "sweep_detected": True}

    signal = sm.generate_signal(context, strategy)
    if sm.evaluate_signal(signal):
        print("Signaal geldig:", signal)
    else:
        print("Signaal ongeldig.")
