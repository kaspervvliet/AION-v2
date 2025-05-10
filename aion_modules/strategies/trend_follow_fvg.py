"""
📄 Bestand: trend_follow_fvg.py
🔍 Doel: Detecteert trendcontinuatie via FVG + bias
🧩 Gebruikt door: strategy_pool_initializer, adaptive_selector
📦 Behoort tot: aion_modules/strategies/
🧠 Verwacht implementatie van: StrategyInterface, concepts, htf_bias_checker, risk_manager
"""

from aion_core.abstract import StrategyInterface
from aion_core.knowledge.concepts import detect_fvg
from aion_core.knowledge.htf_bias_checker import get_htf_bias
from aion_core.utils.risk_manager import calculate_rr
from aion_core.utils.logger import logger


class TrendFollowFVGStrategy(StrategyInterface):
    def generate_signal(self, context):
        tf = context.get("timeframe")
        symbol = context.get("symbol")
        candles = context.get("candles")
        if not candles or len(candles) < 20:
            return self.log("⚠️ Onvoldoende candles", context)

        # 1. Bias check
        bias = get_htf_bias(symbol)
        if not bias or bias not in ["bullish", "bearish"]:
            return self.log("⚠️ Geen duidelijke HTF-bias", context)

        direction = "long" if bias == "bullish" else "short"

        # 2. FVG validatie
        if not detect_fvg(candles, direction=direction):
            return self.log(f"❌ Geen FVG in {direction}-richting", context)

        # 3. Entry-setup
        entry = candles[-1]["close"]
        stop = candles[-1]["low"] if direction == "long" else candles[-1]["high"]
        tp = calculate_rr(entry, stop, rr=1.8, direction=direction)

        return {
            "symbol": symbol,
            "timeframe": tf,
            "entry": entry,
            "stop": stop,
            "tp": tp,
            "direction": direction,
            "strategy": self.__class__.__name__,
        }
