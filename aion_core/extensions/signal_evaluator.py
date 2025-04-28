
"""
📄 Bestand: signal_evaluator.py
🔍 Doel: Evalueren en valideren van gegenereerde trading signals
🧩 Gebruikt door: toekomstige strategieengine
📦 Behoort tot: aion_core/extensions
🧠 Verwacht implementatie van: supabase_logger
"""

import logging
from aion_core.database.supabase_logger import insert_via_edge, update_signal_status

logger = logging.getLogger(__name__)

def validate_signal(signal: dict) -> bool:
    """Evalueer of een signal valide is."""
    try:
        confidence = signal.get("confidence", 0)
        rr = signal.get("rr", 0)

        # Validation criteria
        if confidence >= 0.6 and rr >= 1.2:
            return True
        return False

    except Exception as e:
        logger.error(f"Fout tijdens signal validatie: {e}")
        return False

def evaluate_pending_signals(signals: list) -> None:
    """Filter en update status van pending signals."""
    for signal in signals:
        signal_id = signal.get("id")

        if not signal_id:
            logger.warning("Signal mist ID. Overslaan...")
            continue

        if validate_signal(signal):
            update_signal_status(signal_id, "validated")
            logger.info(f"✅ Signal {signal_id} gevalideerd.")
        else:
            update_signal_status(signal_id, "rejected")
            logger.info(f"❌ Signal {signal_id} afgewezen.")
