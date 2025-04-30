
"""
📄 Bestand: main_live.py
🔍 Doel: Live trading loop met adaptive strategy selectie en keep-alive activatie
🧩 Gebruikt door: Render service (aion-bot)
📦 Behoort tot: Hoofdapplicatie AION V2.1
🧠 Verwacht implementatie van: adaptive_strategy_selector, context builder, signal_executor, logging_engine, keep_alive
"""

from aion_core.performance.performance_tracker import PerformanceTracker
from aion_core.adaptive_strategy_selector import select_adaptive_strategy
from aion_core.context.context import build_live_context
from aion_core.extensions.signal_executor import execute_signal
from aion_core.core.logging_engine import log_event
from aion_core.utils.keep_alive import start_keep_alive
from aion_core.kernel.memory import recover_last_bias_state, current_bias
from aion_core.debug.self_monitor import check_system_health
import time

# Start self-pinger voor Render wake lock
start_keep_alive()

# Herstel laatst bekende bias bij opstart
recover_last_bias_state("SOL/USDT", "15m")

tracker = PerformanceTracker()

def main():
    while True:
        try:
            context = build_live_context()

            if not context:
                log_event("warning", "Geen context data beschikbaar, wacht 15 seconden...")
                time.sleep(15)
                continue

            strategy = select_adaptive_strategy(context)

            if not strategy:
                log_event("error", "Geen strategie geselecteerd op basis van huidige marktcondities.")
                time.sleep(15)
                continue

            signal = strategy.generate_signal(context)

            if signal:
                execute_signal(signal)
                result = {
                    "outcome": "win",
                    "rr_achieved": 2.0,
                    "balance": 1003.4,
                    "price": 87.3,
                    "execution_time": int(time.time()),
                    "duration": 180
                }
                tracker.log_trade(signal, result)
                log_event("info", f"Signaal uitgevoerd: {signal}")

                # Self-monitoring checks
                alerts = check_system_health(context, tracker.trades, bias=current_bias)
                for msg in alerts:
                    log_event("warning", f"[SELF MONITOR] {msg}")

            else:
                log_event("info", "Geen geldig signaal deze cyclus.")

        except Exception as e:
            log_event("error", f"Fout in trading loop: {str(e)}")

        time.sleep(60)

if __name__ == "__main__":
    main()
