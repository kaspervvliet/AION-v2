
from aion_core.config import is_muted, get_config
"""
📄 Bestand: main_live.py
🔍 Doel: Start continue live trading loop op basis van signal engine
🧩 Gebruikt door: Render deployment
📦 Behoort tot: root
🧠 Verwacht implementatie van: signal_engine, strategy_selector
"""

import logging
import time

from aion_core.kernel.signal_engine import run_signal_engine
from aion_core.kernel.adaptive_strategy_selector import select_best_strategy

logger = logging.getLogger("AION")

def main():
    if is_muted():
        logger.info("AION staat in mute-mode. Live loop wordt niet gestart.")
        return

    logger.info("🔁 Live AION loop wordt gestart...")

    try:
        config = get_config()
        strategy = select_best_strategy([])  # in prod: fetch stats from Supabase
        logger.info(f"📌 Geselecteerde strategie: {strategy.__class__.__name__}")

        while True:
            logger.info("⚙️ Nieuwe tick — strategie uitvoeren...")
            run_signal_engine(symbol="SOL/USDT", strategy=strategy)
            time.sleep(30)

    except Exception as e:
        logger.error(f"❌ Live engine crash: {e}")

if __name__ == "__main__":
    main()
