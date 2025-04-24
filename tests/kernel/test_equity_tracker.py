
import unittest
from aion_core.kernel import equity_tracker

class TestEquityTracker(unittest.TestCase):

    def test_track_equity_runs(self):
        setup = {
            "bias": "bullish",
            "has_bos": True,
            "has_fvg": True,
            "rsi": 25
        }
        outcome = {
            "tp_hit": True,
            "sl_hit": False,
            "rr": 2.5
        }

        try:
            equity_tracker.track_equity("test-run-id", setup, outcome)
        except Exception as e:
            self.fail(f"track_equity raised an exception: {e}")

if __name__ == "__main__":
    unittest.main()
