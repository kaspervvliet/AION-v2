"""
📄 Bestand: logtools.py
🔍 Doel: Logging contextmanager voor procesblokken
🧩 Gebruikt door: strategie-logica, setup-evaluatie
📦 Behoort tot: aion_core/utils/
🧠 Verwacht implementatie van: log_step()
"""

import logging
import time
from contextlib import contextmanager
from typing import Generator

logger = logging.getLogger("AION")

@contextmanager
def log_step(label: str) -> Generator[None, None, None]:
    """
    Logging context die starttijd + emoji toont voor stap.
    """
    logger.info(f"🟡 {label} gestart...")
    t0 = time.time()
    try:
        yield
        t1 = time.time()
        logger.info(f"✅ {label} voltooid ({t1 - t0:.2f}s)")
    except Exception as e:
        logger.error(f"❌ {label} gefaald: {e}")
        raise

if __name__ == "__main__":
    with log_step("Voorbeeldstap"):
        time.sleep(1.2)
