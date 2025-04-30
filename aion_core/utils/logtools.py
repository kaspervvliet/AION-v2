
"""
📄 Bestand: logtools.py
🔍 Doel: Contextmanager voor nette begin/einde logging
🧩 Gebruikt door: kernel, logging_engine, debug
📦 Behoort tot: aion_core/utils/
🧠 Gebruik: with log_context("label"):
"""

from contextlib import contextmanager
import logging
import time

logger = logging.getLogger(__name__)

@contextmanager
def log_context(name: str):
    start = time.strftime('%Y-%m-%d %H:%M:%S')
    logger.info(f"🔷 [{start}] START: {name}")
    try:
        yield
    finally:
        end = time.strftime('%Y-%m-%d %H:%M:%S')
        logger.info(f"🔶 [{end}] END: {name}")
