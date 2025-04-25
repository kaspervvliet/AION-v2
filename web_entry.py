from aion_core.context.context import AIONContext

from fastapi import FastAPI
from threading import Thread
from aion_core import context
from aion_core.kernel import kernel

app = FastAPI()

@app.get("/ping")
def ping():
    return {"status": "AION is alive"}

def live_loop():
    import time
    print("🧠 AION live loop gestart...")
    while True:
        try:
    candle = ctx.fetch_latest_candle()
except Exception as e:
    print(f"[ERROR] Kon geen candle ophalen: {e}")
    candle = None
            candle = ctx = AIONContext(symbol="SOL/USDT", timeframe="15m")
candle = ctx.fetch_latest_candle()
            setup = context.analyse_market(candle)
            decision = kernel.evaluate(setup)

            if decision.status == "GO":
                outcome = context.simulate_trade(setup)
                kernel.observe_trade(setup, outcome, decision.status, decision.confidence, decision.reason)
        except Exception as e:
            print("[LIVE LOOP ERROR]", str(e))

        time.sleep(60 * 15)

# Start live loop zodra API draait
Thread(target=live_loop, daemon=True).start()
