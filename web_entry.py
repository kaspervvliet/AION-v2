
from fastapi import FastAPI
import threading
from aion_core.kernel import context, kernel
import time

app = FastAPI()

@app.get("/ping")
def ping():
    return {"status": "AION live", "message": "StrategicKernel running."}

def live_loop():
    print("🟢 AION LIVE LOOP gestart op achtergrond thread.")
    while True:
        candle = context.fetch_latest_candle("SOL/USDT")
        setup = context.analyse_market(candle)
        decision = kernel.evaluate(setup)

        if decision.status == "GO":
            outcome = context.simulate_trade(setup)
            kernel.observe_trade(setup, outcome, decision.status, decision.confidence, decision.reason)

        time.sleep(60 * 15)  # 15 min

# Start bij opstarten
threading.Thread(target=live_loop, daemon=True).start()
