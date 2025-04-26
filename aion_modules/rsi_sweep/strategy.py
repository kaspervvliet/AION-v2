"""
📄 Bestand: strategy.py
🔍 Doel: RSI Sweep strategie module (geupgrade met echte BOS/CHoCH analyse)
🧩 Gebruikt door: loader.py, backtest, UI
📦 Behoort tot: aion_modules/rsi_sweep/
"""

import logging
from aion_core.base_strategy import BaseStrategy
from aion_core.kernel import kernel
from aion_modules.analyse_bos_choc import analyse_bos_choc

logger = logging.getLogger("AION")

class Strategy(BaseStrategy):
    def is_entry(self, candle_data):
        """
        Logica:
        - Echte analyse van BOS/CHoCH over recente candles
        - Simuleert voorlopig FVG en RSI waarden
        """
        if not candle_data or len(candle_data[-1]) < 5:
            return False

        bos_choc = analyse_bos_choc(candle_data, direction='bullish')

        setup = {
            "has_bos": bos_choc['bos'],
            "has_fvg": True,  # FVG wordt later toegevoegd
            "bias": "bullish",
            "rsi": 28  # Placeholder waarde
        }

        decision = kernel.evaluate(setup)
        logger.info(f"[KERNEL] Decision: {decision.status} | Confidence: {decision.confidence} | Reason: {decision.reason}")

        return decision.status == "GO"

    def get_metadata(self):
        return {
            "name": "RSI Sweep",
            "version": "1.1",
            "author": "Mariëlle",
            "inputs": ["RSI", "Liquidity sweep", "BOS/CHoCH"],
            "output": ["is_entry", "alerts"]
        }