"""
📄 Bestand: web_entry.py
🔍 Doel: FastAPI runner voor AION met KernelDecision integratie
🧩 Gebruikt door: Render deployment / cloud
📦 Behoort tot: root
🧠 Werkt nu met KernelDecision object
"""

import logging
from threading import Thread
from fastapi import FastAPI

from aion_core.context.context import AIONContext
from aion_core.kernel.kernel import kernel
from aion_core.context.context import analyse_market

logger = logging.getLogger(__name__)
app = FastAPI()

@app.get("/ping")
def ping():
    return {"status": "AION live"}

def live_loop():
    import time
    logger.info("🧠 AION live loop gestart...")
    ctx = AIONContext(symbol="SOL/USDT", timeframe="15m")

    while True:
        try:
            candle = ctx.fetch_latest_candle()
            if candle:
                setup = analyse_market(candle)
                decision = kernel.evaluate(setup)

                logger.info(f"Status: {decision.status}, Confidence: {decision.confidence}, Reason: {decision.reason}")

                if decision.status == "GO":
                    logger.info("🚀 GO - Trade activatie mogelijk")
                elif decision.status == "SKIP":
                    logger.info("⚠️ SKIP - Geen entry door HTF bias")
                else:
                    logger.info("🔎 CAUTION - Setup twijfelachtig")
            else:
                logger.warning("[LIVE_LOOP] Geen candle opgehaald.")
        except Exception as e:
            logger.warning(f"[LIVE_LOOP ERROR] {e}")

        time.sleep(15)

if __name__ != "__main__":
    Thread(target=live_loop, daemon=True).start()
