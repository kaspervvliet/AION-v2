"""
📄 Bestand: test_morph_engine.py
🔍 Doel: [AUTO-GEGENEREERD: controleer doel handmatig]
🧩 Gebruikt door: onbekend
📦 Behoort tot: tests
🧠 Laatst geüpdatet: 2025-04-25
"""


import unittest
import os
import json
from aion_core.kernel import morph_engine

STATE_PATH = "morph_state.json"

class TestMorphEngine(unittest.TestCase):

    def setUp(self):
        self.initial_state = {
            "min_confidence_go": 0.7,
            "boost_on_win": 0.02,
            "penalty_on_loss": 0.03,
            "bias_weight": 1.0,
            "rsi_weight": 1.0,
            "min": 0.5,
            "max": 0.95,
            "mutation_log": []
        }
        with open(STATE_PATH, "w") as f:
            json.dump(self.initial_state, f)

    def test_adjust_upwards_on_tp(self):
        morph_engine.adjust_threshold({"tp_hit": True, "sl_hit": False})
        state = morph_engine.load_state()
        self.assertGreater(state["min_confidence_go"], 0.7)

    def test_adjust_downwards_on_sl(self):
        morph_engine.adjust_threshold({"tp_hit": False, "sl_hit": True})
        state = morph_engine.load_state()
        self.assertLess(state["min_confidence_go"], 0.7)

    def test_boundaries_respected(self):
        self.initial_state["min_confidence_go"] = 0.5
        with open(STATE_PATH, "w") as f:
            json.dump(self.initial_state, f)
        morph_engine.adjust_threshold({"tp_hit": False, "sl_hit": True})
        state = morph_engine.load_state()
        self.assertEqual(state["min_confidence_go"], 0.5)

        self.initial_state["min_confidence_go"] = 0.95
        with open(STATE_PATH, "w") as f:
            json.dump(self.initial_state, f)
        morph_engine.adjust_threshold({"tp_hit": True, "sl_hit": False})
        state = morph_engine.load_state()
        self.assertEqual(state["min_confidence_go"], 0.95)

    def test_mutate(self):
        morph_engine.mutate()
        state = morph_engine.load_state()
        self.assertGreater(state["bias_weight"], 1.0)
        self.assertIn("mutation_log", state)
        self.assertTrue(len(state["mutation_log"]) > 0)

    def tearDown(self):
        if os.path.exists(STATE_PATH):
            os.remove(STATE_PATH)

if __name__ == "__main__":
    unittest.main()
