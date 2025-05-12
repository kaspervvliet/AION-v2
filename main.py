from aion_core.config import is_muted
"""
📄 Bestand: main.py
🔍 Doel: Dev/test entrypoint voor AION componenten
🧩 Gebruikt door: ontwikkelaars
📦 Behoort tot: cli/ (verplaatsbaar)
🧠 Verwacht implementatie van: losse module-aanroepen
"""

import logging

from aion_core.kernel.context_manager import create_context
from aion_core.utils.logtools import log_step

logger = logging.getLogger("AION")

def main():
    if is_muted():
        logger.info("Script staat in mute-mode. Afgebroken.")
        return

    logger.info("[DEV] Start main testscript")

    with log_step("Voorbeeld testblock"):
        from pandas import DataFrame
        df = DataFrame({"bias": ["long"], "fvg_hit": [True]})
        ctx = create_context(df, "1H")
        logger.info(f"Context: {ctx}")

if __name__ == "__main__":
    main()
