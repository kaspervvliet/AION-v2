"""
📄 Bestand: memory.py
🔍 Doel: [AUTO-GEGENEREERD: controleer doel handmatig]
🧩 Gebruikt door: onbekend
📦 Behoort tot: aion_core
🧠 Laatst geüpdatet: 2025-04-25
"""

import logging
logger = logging.getLogger(__name__)
import datetime

def log_setup(setup: dict, confidence: float, status: str):
    logger.info(f"[MEMORY] Setup logged @ {datetime.datetime.now().isoformat()} → {status} ({confidence})")
    # Supabase insert can be added here

def log_outcome(setup: dict, outcome: dict):
    logger.info(f"[MEMORY] Outcome: TP={outcome.get('tp_hit')}, SL={outcome.get('sl_hit')}, RR={outcome.get('rr')}")
    # Supabase insert can be added here
