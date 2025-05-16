
from aion_core.config import is_muted
"""
📄 Bestand: logger.py
🔍 Doel: Initialiseert globale AION-logger
🧩 Gebruikt door: alle modules
📦 Behoort tot: aion_core/utils/
🧠 Verwacht implementatie van: kleur, mute, debug-niveau
"""

import logging
import os

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
            "\x1b[90m[%(asctime)s]\x1b[0m %(levelname)s: \x1b[1m%(message)s\x1b[0m",
            datefmt="%H:%M:%S"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger

# Init standaard bij import
logger = init_logger()

def log(msg: str, level: str = "info"):
    if level == "debug":
        logger.debug(msg)
    elif level == "warning":
        logger.warning(msg)
    elif level == "error":
        logger.error(msg)
    else:
        logger.info(msg)

if __name__ == "__main__":
    logger.info("Logger actief")
    logger.debug("Debug test")
