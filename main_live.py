
### main_live.py ###

from aion_core.kernel import context
from aion_core.kernel import kernel
from aion_core.kernel import equity_tracker
from aion_core.kernel import reflection
from aion_core import config
import time

print("🟢 AION LIVE MODE STARTED")

def run():
    if not config.LIVE_MODE:
        print("[LIVE] ❌ LIVE_MODE is uitgeschakeld via .env")
        return

    while True:
        candle = context.fetch_latest_candle("SOL/USDT")
        setup = context.analyse_market(candle)
        decision = kernel.evaluate(setup)

        if decision.status == "GO":
            outcome = context.simulate_trade(setup)
            kernel.observe_trade(setup, outcome, decision.status, decision.confidence, decision.reason)

        time.sleep(60 * 15)  # 15 minuten wachten

if __name__ == "__main__":
    run()
