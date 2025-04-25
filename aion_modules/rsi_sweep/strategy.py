"""
import logging
logger = logging.getLogger(__name__)
📄 Bestand: strategy.py
🔍 Doel: RSI Sweep strategie module
🧩 Gebruikt door: loader.py, backtest, UI
📦 Behoort tot: aion_modules/rsi_sweep/
"""

from aion_core.base_strategy import BaseStrategy
from aion_core.kernel import kernel

class Strategy(BaseStrategy):
    def is_entry(self, candle_data):
        """
        Dummy-logica:
        - Check of RSI onder 30 (simulatie)
        - Check of laatste candle sweeping low heeft
        """
        if not candle_data or len(candle_data[-1]) < 5:
            return False

        close = candle_data[-1][4]  # close
        low = candle_data[-1][3]    # low

        setup = {
            "has_bos": True,
            "has_fvg": True,
            "bias": "bullish",
            "rsi": 28
        }
        decision = kernel.evaluate(setup)
        logger.info(f"[KERNEL] Decision: {decision.status} | Confidence: {decision.confidence} | Reason: {decision.reason}")

        if decision.status == "GO":
            return True

        return False

    def get_metadata(self):
        return {
            "name": "RSI Sweep",
            "version": "1.0",
            "author": "Mariëlle",
            "inputs": ["RSI", "Liquidity sweep"],
            "output": ["is_entry", "alerts"]
        }

# ✅ Externe analyse functie
def analyse_market(candle, context):
    setup = {
        "has_bos": True,
        "has_fvg": True,
        "bias": "bullish",
        "rsi": 28  # Deze waarde zou normaal berekend worden
    }
    return setup
