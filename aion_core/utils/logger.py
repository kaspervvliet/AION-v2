"""
📄 Bestand: logger.py
🔍 Doel: Centraal logging object voor alle modules
🧩 Gebruikt door: safe_io, kraken, context, strategieën
📦 Behoort tot: aion_core/utils/
"""

import logging

logger = logging.getLogger("AION")
logger.setLevel(logging.INFO)

if not logger.handlers:
    console = logging.StreamHandler()
    formatter = logging.Formatter("[%(levelname)s] %(message)s")
    console.setFormatter(formatter)
    logger.addHandler(console)
