from aion_core.context.context_engine import detect_bos, detect_choch
"""
📄 Bestand: mean_revert_chopbox.py
🔍 Doel: Rangebound entry gebaseerd op Sweep + BOS + FVG
🧩 Gebruikt door: strategy_pool_initializer, adaptive_selector
📦 Behoort tot: aion_modules/strategies/
🧠 Verwacht implementatie van: StrategyInterface, concepts, risk_manager
"""

from aion_core.abstract import StrategyInterface
from aion_core.knowledge.concepts import detect_sweep, detect_bos, detect_fvg
from aion_core.utils.risk_manager import calculate_rr
import time
from aion_core.utils.logger import logger


class MeanRevertChopboxStrategy(StrategyInterface):
    def generate_signal(self, context):
        tf = context.get("timeframe")
        symbol = context.get("symbol")
        candles = context.get("candles")

        if not candles or len(candles) < 30:
            return self.log("⚠️ Onvoldoende candles", context)

        # 1. Sweep validatie
        if not detect_sweep(candles):
            return self.log("❌ Geen sweep", context)

        # 2. BOS validatie
        structure = context.get("structure")
        if not structure or not detect_bos(structure):
            return self.log("❌ Geen BOS gedetecteerd", context)

        # 3. FVG check in tegenovergestelde richting
        direction = "short" if candles[-1]["close"] > candles[-1]["open"] else "long"
        if not detect_fvg(candles, direction=direction):
            return self.log(f"❌ Geen FVG in {direction}-richting", context)

        # 4. Entry setup
        entry = candles[-1]["close"]
        stop = candles[-1]["high"] if direction == "short" else candles[-1]["low"]
        tp = calculate_rr(entry, stop, rr=1.5, direction=direction)

        return {
            "symbol": symbol,
            "timeframe": tf,
            "entry": entry,
            "stop": stop,
            "tp": tp,
            "direction": direction,
            "strategy": self.__class__.__name__,
        }
