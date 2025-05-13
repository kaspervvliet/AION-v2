"""
📄 Bestand: breakout_snipe.py
🔍 Doel: Detecteert breakout entry via CHoCH + sweep + bias
🧩 Gebruikt door: strategy_pool_initializer, adaptive_selector
📦 Behoort tot: aion_modules/strategies/
🧠 Verwacht implementatie van: StrategyInterface, concepts, htf_bias_checker, risk_manager
"""

from aion_core.abstract import StrategyInterface
from aion_core.knowledge.concepts import detect_choc, detect_sweep
from aion_core.knowledge.htf_bias_checker import get_htf_bias
from aion_core.utils.risk_manager import calculate_rr
import time
from aion_core.utils.logger import logger


class BreakoutSnipeStrategy(StrategyInterface):
    def generate_signal(self, context):
        tf = context.get("timeframe")
        symbol = context.get("symbol")
        candles = context.get("candles")
        if not candles or len(candles) < 20:
            return self.log("⚠️ Onvoldoende candles", context)

        # 1. Sweep check
        if not detect_sweep(candles):
            return self.log("❌ Geen sweep gedetecteerd", context)

        # 2. CHoCH/Breakout check
        structure = context.get("structure")
        if not structure or not detect_choc(structure):
            return self.log("❌ Geen CHoCH-breakout", context)

        # 3. HTF bias bevestiging
        bias = get_htf_bias(symbol)
        if not bias or bias not in ["bullish", "bearish"]:
            return self.log("⚠️ Geen duidelijke HTF-bias", context)

        # 4. Trade richting
        direction = "long" if bias == "bullish" else "short"

        # 5. Entry parameters
        entry = candles[-1]["close"]
        stop = candles[-1]["low"] if direction == "long" else candles[-1]["high"]
        tp = calculate_rr(entry, stop, rr=2.0, direction=direction)

        return {
            "symbol": symbol,
            "timeframe": tf,
            "entry": entry,
            "stop": stop,
            "tp": tp,
            "direction": direction,
            "strategy": self.__class__.__name__,
        }
