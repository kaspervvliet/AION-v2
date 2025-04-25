"""
📄 Bestand: web_entry.py
🔍 Doel: Webservice entrypoint voor live loop (uvicorn)
🧩 Gebruikt door: render deployment
📦 Behoort tot: root
🧠 Verwacht implementatie van: ctx initialisatie, fetch, alert push
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
            setup = context.analyse_market(candle)
            decision = kernel.evaluate(setup)

            if decision.status == "GO":
                outcome = context.simulate_trade(setup)
                kernel.observe_trade(setup, outcome)

        except Exception as e:
            logger.warning(f"[ERROR] Live loop fout: {e}")

        time.sleep(15)

# Start de live loop bij opstart via thread
if __name__ != "__main__":
    Thread(target=live_loop, daemon=True).start()
