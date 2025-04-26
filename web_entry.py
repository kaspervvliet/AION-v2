'''
📄 Bestand: web_entry.py
🔍 Doel: Hoofdingang AION server - live trading loop beheren
🧩 Gebruikt door: Render Web Service (uvicorn)
📦 Behoort tot: AION V2
🧠 Verwacht implementatie van: evaluate() uit aion_core.kernel.kernel
'''

import asyncio
import time
import logging
from fastapi import FastAPI
from aion_core.kernel.kernel import evaluate  # ✅ Correcte import nu

# Initieer FastAPI app
app = FastAPI()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AION")

# Mock: setup ophalen (later dynamisch maken)
def fetch_setup():
    return {
        "symbol": "SOLUSDT",
        "bias": "bullish",
        "structure": "valid",
        "confidence": 0.85
    }

# Live trading loop
async def live_loop():
    logger.info("[AION] Live loop gestart.")
    while True:
        setup = fetch_setup()
        logger.info(f"[AION] Setup ontvangen: {setup}")

        decision = evaluate(setup)  # ✅ Direct gebruik van evaluate()

        if decision.status:
            logger.info(f"[SIGNAL] Trade GO! Confidence: {decision.confidence:.2f} - Reason: {decision.reason}")
        else:
            logger.info(f"[SIGNAL] Geen trade. Reden: {decision.reason}")

        await asyncio.sleep(15)  # Wacht 15 sec voor volgende check

# Root endpoint
@app.get("/")
async def root():
    return {"message": "AION V2 server actief."}

# Background task
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(live_loop())