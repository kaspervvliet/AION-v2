from aion_core.context.context_engine import detect_bos, detect_choch
"""
📄 Bestand: rsi_sweep.py
🔍 Doel: Strategie op basis van RSI-extreem gecombineerd met liquidity sweep
🧩 Gebruikt door: strategy_pool, backtest
📦 Behoort tot: aion_modules/strategies/
🧠 Verwacht implementatie van: StrategyInterface, concepts, indicators
"""

from aion_core.abstract import StrategyInterface
from aion_core.knowledge.concepts import detect_sweep
from aion_core.indicators.rsi import calculate_rsi
from aion_core.utils.logger import logger
from aion_core.utils.risk_manager import calculate_rr
import time


class RSISweepStrategy(StrategyInterface):
    def generate_signal(self, context):
        candles = context.get("candles")
        symbol = context.get("symbol")
        tf = context.get("timeframe")

        if not candles or len(candles) < 20:
            return self.log("⚠️ Onvoldoende candles", context)

        rsi = calculate_rsi(candles, period=14)
        if rsi is None or rsi[-1] < 0:
            return self.log("⚠️ RSI kon niet worden berekend", context)

        if rsi[-1] > 75:
            bias = "short"
        elif rsi[-1] < 25:
            bias = "long"
        else:
            return self.log("❌ RSI niet in extremen", context)

        if not detect_sweep(candles):
            return self.log("❌ Geen sweep gedetecteerd", context)

        entry = candles[-1]["close"]
        stop = candles[-1]["high"] if bias == "short" else candles[-1]["low"]
        tp = calculate_rr(entry, stop, rr=1.5, direction=bias)

        return {
            "symbol": symbol,
            "timeframe": tf,
            "entry": entry,
            "stop": stop,
            "tp": tp,
            "direction": bias,
            "strategy": self.__class__.__name__,
            "log_equity": {
                "timestamp": int(time.time()),
                "symbol": symbol,
                "rr": 1.5,
                "result": tp - entry if bias == "long" else entry - tp,
                "confidence": abs(rsi[-1] - 50) / 50,
                "balance": 1000,
                "exposure": 0.2
            },
            "reflection": {
                "timestamp": int(time.time()),
                "symbol": symbol,
                "setup": {
                    "entry": "sweep + rsi_extreme",
                    "bias": bias
                },
                "decision": "ja",
                "outcome": "N/A",
                "explanation": f"RSI={rsi[-1]:.2f}, sweep actief, entry={entry:.2f}"
            }
        }
