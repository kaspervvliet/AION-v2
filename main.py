"""
📄 Bestand: main.py
🔍 Doel: AION stand-alone runner
🧩 Gebruikt door: lokaal testen van live signal flow
📦 Behoort tot: root
🧠 Werkt met dict-based candles
"""

import logging
from aion_core.context.context import AIONContext
from aion_core import context
from aion_core.kernel import kernel
import config

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    if not config.LIVE_MODE:
        logger.info("[MAIN] ⚠️ LIVE_MODE is uit — draai als test.")

    ctx = AIONContext(symbol="SOL/USDT", timeframe="15m")
    candle = ctx.fetch_latest_candle()

    if candle:
        setup = context.analyse_market(candle)
        decision = kernel.evaluate(setup)

        logger.info("\n--- BESLISSING ---")
        logger.info("STATUS: %s", decision.status)
        logger.info("CONFIDENCE: %s", decision.confidence)
        logger.info("REASON: %s", decision.reason)

        if decision.status == "GO":
            outcome = context.simulate_trade(setup)
            kernel.observe_trade(setup, outcome)
    else:
        logger.warning("[MAIN] Geen candle opgehaald — skipping analyse.")
