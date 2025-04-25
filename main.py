from aion_core.context.context import AIONContext

### main.py – handmatige test of analyse ###

from aion_core.kernel import context
from aion_core.kernel import kernel
from aion_core.kernel import reflection
from aion_core.kernel import equity_tracker
from aion_core import config

print("🧪 AION MANUAL RUN")

if __name__ == "__main__":
    if not config.LIVE_MODE:
        print("[MAIN] ⚠️ LIVE_MODE is uit — draai als test.")

    candle = ctx = AIONContext(symbol="SOL/USDT", timeframe="15m")
candle = ctx.fetch_latest_candle()
    setup = context.analyse_market(candle)
    decision = kernel.evaluate(setup)

    print("\n--- BESLISSING ---")
    print("STATUS:", decision.status)
    print("CONFIDENCE:", decision.confidence)
    print("REASON:", decision.reason)

    if decision.status == "GO":
        outcome = context.simulate_trade(setup)
        kernel.observe_trade(setup, outcome, decision.status, decision.confidence, decision.reason)
        print("[MAIN] ✅ Trade gesimuleerd en gelogd.")
