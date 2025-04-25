"""
📄 Bestand: test_trade_explainer.py
🔍 Doel: [AUTO-GEGENEREERD: controleer doel handmatig]
🧩 Gebruikt door: onbekend
📦 Behoort tot: tests
🧠 Laatst geüpdatet: 2025-04-25
"""


import unittest
from aion_core.kernel import trade_explainer

class TestTradeExplainer(unittest.TestCase):

    def test_explainer_output_contains_core_fields(self):
        setup = {
            "bias": "bearish",
            "has_bos": False,
            "has_fvg": True,
            "rsi": 33
        }
        explanation = trade_explainer.explain_decision(setup, "CAUTION", 0.62, "weak confluence")
        self.assertIn("⚠️ Beslissing: CAUTION", explanation)
        self.assertIn("📌 Reden: weak confluence", explanation)
        self.assertIn("📉 RSI: 33", explanation)

if __name__ == "__main__":
    unittest.main()
