from fastapi import FastAPI
from threading import Thread
from aion_core.context import AIONContext
from aion_core.kernel import kernel
from aion_modules.rsi_sweep.strategy import analyse_market

app = FastAPI()

@app.get("/ping")
def ping():
    return {"status": "AION is alive"}

def live_loop():
    import time
    print("🧠 AION live loop gestart...")

    context = AIONContext.from_supabase("SOL/USDT", "15m")
    context.fetch_candles_from_kraken("1h")  # HTF bias
    context.fetch_candles_from_kraken("15m")  # LTF entries

    while True:
        try:
            candle = context.get_latest_price()
            if candle is None:
                print("[LOOP] ⚠️ Geen candle beschikbaar — skipping analyse.")
                continue

            setup = analyse_market(candle, context)
            decision = kernel.evaluate(setup)

            if decision.status == "GO":
                outcome = context.simulate_trade(setup)
                kernel.observe_trade(setup, outcome, decision.status, decision.confidence, decision.reason)
                context.push_to_supabase()
        except Exception as e:
            print("[LIVE LOOP ERROR]", str(e))

        time.sleep(60 * 15)

# Start live loop zodra API draait
Thread(target=live_loop, daemon=True).start()
