"""
📄 Bestand: main.py
🔍 Doel: AION standalone runner met kernel decision integratie
🧩 Gebruikt door: lokaal testen, debuggen
📦 Behoort tot: root
🧠 Werkt nu met KernelDecision object
"""

import logging
from aion_core.context.context import AIONContext
from aion_core.kernel.kernel import kernel
from aion_core.context.context import analyse_market

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    ctx = AIONContext(symbol="SOL/USDT", timeframe="15m")
    latest_candle = ctx.fetch_latest_candle()

    if latest_candle:
        setup = analyse_market(latest_candle)
        decision = kernel.evaluate(setup)

        logger.info("\n--- BESLISSING ---")
        logger.info(f"Status: {decision.status}")
        logger.info(f"Confidence: {decision.confidence}")
        logger.info(f"Reason: {decision.reason}")

        if decision.status == "GO":
            logger.info("🚀 Trade wordt geactiveerd!")
        elif decision.status == "SKIP":
            logger.info("⚠️ Setup geskipped wegens HTF mismatch")
        else:
            logger.info("🔎 Setup onder voorbehoud (CAUTION)")
    else:
        logger.warning("[MAIN] Geen candle opgehaald — skipping analyse.")
