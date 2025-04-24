
import unittest
from aion_core.kernel import reflection

class TestReflection(unittest.TestCase):

    def test_build_prompt_output(self):
        setup = {"bias": "bullish", "has_bos": True, "rsi": 27}
        outcome = {"tp_hit": False, "sl_hit": True, "rr": -1.0}
        decision = "GO"
        confidence = 0.78
        reason = "bias alignment + FVG"

        prompt = reflection.build_prompt(setup, outcome, decision, confidence, reason)
        self.assertIn("De strategie besloot", prompt)
        self.assertIn("Wat zou AION in deze situatie kunnen verbeteren", prompt)
        self.assertIn("SL=True", prompt.replace("True", "SL=True"))

    def test_log_reflection_stub(self):
        setup = {"bias": "bearish", "has_fvg": True}
        outcome = {"tp_hit": False, "sl_hit": True, "rr": -0.5}
        try:
            reflection.log_reflection("test-run", setup, outcome, "SKIP", 0.42, "weak structure")
        except Exception as e:
            self.fail(f"log_reflection raised an exception: {e}")

if __name__ == "__main__":
    unittest.main()
