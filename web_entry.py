"""
📄 Bestand: web_entry.py
🔍 Doel: Webservice entrypoint + live trading loop
🧩 Gebruikt door: Render deployment
📦 Behoort tot: root
🧠 Werkt met dict-based candles
"""

import logging
from threading import Thread
from fastapi import FastAPI

from aion_core.context.context import AIONContext
from aion_core import context
from aion_core.kernel import kernel

logger = logging.getLogger(__name__)
app = FastAPI()

@app.get("/ping")
def ping():
    return {"status": "AION is alive"}

def live_loop():
    import time
    logger.info("🧠 AION live loop gestart...")
    ctx = AIONContext(symbol="SOL/USDT", timeframe="15m")

    while True:
        try:
            candle = ctx.fetch_latest_candle()

            if candle:
                setup = context.analyse_market(candle)
                decision = kernel.evaluate(setup)

                if decision.status == "GO":
                    outcome = context.simulate_trade(setup)
                    kernel.observe_trade(setup, outcome)
            else:
                logger.warning("[LIVE_LOOP] Geen candle opgehaald.")

        except Exception as e:
            logger.warning(f"[LIVE_LOOP ERROR] {e}")

        time.sleep(15)  # 15 seconden poll interval

# Start de live loop alleen als niet direct gestart
if __name__ != "__main__":
    Thread(target=live_loop, daemon=True).start()
