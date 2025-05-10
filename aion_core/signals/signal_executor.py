"""
📄 Bestand: signal_executor.py
🔍 Doel: Simuleert en logt de uitvoering van signalen
🧩 Gebruikt door: strategy_executor, kernel, signal_engine
📦 Behoort tot: aion_core/extensions/
🧠 Verwacht implementatie van: supabase_writer, logger, time
"""

import time
from aion_core.utils.logger import logger
from aion_core.database.supabase_writer import insert_signal_execution


def execute_signals(signal_batch: list, strategy_name: str = "unknown"):
    if not signal_batch:
        logger.warning("⚠️ Geen signalen om uit te voeren.")
        return

    logger.info(f"▶️ Uitvoeren van {len(signal_batch)} signalen...")

    for i, signal in enumerate(signal_batch):
        signal_id = signal.get("id", f"no-id-{i}")
        logger.info(f"🔁 Simuleer uitvoering van signaal {signal_id}")

        # Simuleer wachttijd (bv. order-uitvoering)
        time.sleep(0.2)

        # Log naar Supabase
        result = insert_signal_execution({
            "signal_id": signal_id,
            "strategy": strategy_name,
            "executed_at": time.time()
        })

        if not result["success"]:
            logger.error(f"❌ Mislukt om signaal {signal_id} te loggen: {result['error']}")
        else:
            logger.info(f"✅ Signaal {signal_id} uitgevoerd en gelogd.")
