"""
📄 Bestand: main.py
🔍 Doel: [AUTO-GEGENEREERD: controleer doel handmatig]
🧩 Gebruikt door: onbekend
📦 Behoort tot: main.py
🧠 Laatst geüpdatet: 2025-04-25
"""


"""
📄 Bestand: main.py
🔍 Doel: Start full module + UI interactie
🧩 Gebruikt door: interactief gebruik met streamlit of CLI
📦 Behoort tot: root
🧠 Verwacht implementatie van: context loader, UI-runner
"""

import logging
logger = logging.getLogger(__name__)
from aion_core.context.context import AIONContext

### main.py – handmatige test of analyse ###

from aion_core.kernel import context
from aion_core.kernel import kernel
from aion_core.kernel import reflection
from aion_core.kernel import equity_tracker
from aion_core import config

logger.info("🧪 AION MANUAL RUN")

if __name__ == "__main__":
    if not config.LIVE_MODE:
        logger.info("[MAIN] ⚠️ LIVE_MODE is uit — draai als test.")

    ctx = AIONContext(symbol="SOL/USDT", timeframe="15m")
    candle = ctx.fetch_latest_candle()
    setup = context.analyse_market(candle)
    decision = kernel.evaluate(setup)

    logger.info("\n--- BESLISSING ---")
    logger.info("STATUS: %s", decision.status)
    logger.info("CONFIDENCE: %s", decision.confidence)
    logger.info("REASON: %s", decision.reason)

    if decision.status == "GO":
        outcome = context.simulate_trade(setup)
        kernel.observe_trade(setup, outcome, decision.status, decision.confidence, decision.reason)
        logger.info("[MAIN] ✅ Trade gesimuleerd en gelogd.")
