"""
📄 Bestand: logger.py
🔍 Doel: Initialiseert globale AION-logger
🧩 Gebruikt door: alle modules
📦 Behoort tot: aion_core/utils/
🧠 Verwacht implementatie van: kleur, mute, debug-niveau
"""

import logging
import os
from config import is_muted

AION_LOGGER_NAME = "AION"

def init_logger() -> logging.Logger:
    if is_muted():
        logging.getLogger(AION_LOGGER_NAME).disabled = True
        return logging.getLogger(AION_LOGGER_NAME)

    logger = logging.getLogger(AION_LOGGER_NAME)
    logger.setLevel(logging.DEBUG if os.getenv("AION_MODE") == "DEV" else logging.INFO)

    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "[90m[%(asctime)s][0m %(levelname)s: [1m%(message)s[0m",
            datefmt="%H:%M:%S"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger

# Init standaard bij import
logger = init_logger()

if __name__ == "__main__":
    logger.info("Logger actief")
    logger.debug("Debug test")
