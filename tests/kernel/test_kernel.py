
import unittest
from aion_core.kernel.kernel import kernel

class TestKernelEvaluate(unittest.TestCase):

    def test_go_decision(self):
        setup = {
            "has_bos": True,
            "has_fvg": True,
            "bias": "bullish",
            "rsi": 28
        }
        decision = kernel.evaluate(setup)
        self.assertEqual(decision.status, "GO")
        self.assertGreaterEqual(decision.confidence, 0.7)

    def test_caution_decision(self):
        setup = {
            "has_bos": False,
            "has_fvg": True,
            "bias": "bullish",
            "rsi": 32
        }
        decision = kernel.evaluate(setup)
        self.assertEqual(decision.status, "CAUTION")

    def test_skip_decision(self):
        setup = {
            "has_bos": False,
            "has_fvg": False,
            "bias": "neutral",
            "rsi": 55
        }
        decision = kernel.evaluate(setup)
        self.assertEqual(decision.status, "SKIP")
        self.assertLessEqual(decision.confidence, 0.5)

if __name__ == "__main__":
    unittest.main()
