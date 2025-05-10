"""
📄 Bestand: signal_engine.py
🔍 Doel: Genereert beslissingen en logs voor inkomende signalen
🧩 Gebruikt door: strategy_executor, supabase_writer, reflectie
📦 Behoort tot: aion_core/kernel/
🧠 Verwacht implementatie van: logger, validatie op signalen
"""

from aion_core.utils.logger import logger


def evaluate_signals(signal_batch: list) -> list:
    """
    Evalueer een batch signalen, valideer en label ze
    """
    results = []

    if not signal_batch:
        logger.warning("⚠️ Geen signalen ontvangen voor evaluatie.")
        return results

    for signal in signal_batch:
        if not all(k in signal for k in ["entry", "stop", "tp", "direction"]):
            logger.warning(f"❌ Incompleet signaal: {signal}")
            results.append({"status": "rejected", "reason": "incomplete", "signal": signal})
            continue

        rr = abs((signal["tp"] - signal["entry"]) / (signal["entry"] - signal["stop"])) if signal["entry"] != signal["stop"] else 0
        if rr < 1.0:
            logger.info(f"❌ RR te laag ({rr:.2f}) — signaal geweigerd")
            results.append({"status": "rejected", "reason": f"rr={rr:.2f}", "signal": signal})
        else:
            logger.info(f"✅ Signaal geaccepteerd ({signal['direction'].upper()} | RR={rr:.2f})")
            results.append({"status": "accepted", "rr": rr, "signal": signal})

    return results
