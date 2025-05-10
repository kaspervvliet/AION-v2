"""
📄 Bestand: morph_engine.py
🔍 Doel: Past strategieparameters aan op basis van performance ('morphing')
🧩 Gebruikt door: strategy_executor, kernel
📦 Behoort tot: aion_core/kernel/
🧠 Verwacht implementatie van: logger
"""

from aion_core.utils.logger import logger


def morph_strategy(settings: dict, result: str) -> dict:
    """
    Wijzigt interne parameters (zoals RR) afhankelijk van trade-uitkomst
    """
    if not settings or "rr" not in settings:
        logger.warning("⚠️ Settings missen sleutel 'rr'")
        return settings

    old_rr = settings["rr"]

    if result == "win":
        settings["rr"] = round(min(old_rr + 0.2, 3.0), 2)
    elif result == "loss":
        settings["rr"] = round(max(old_rr - 0.2, 0.8), 2)
    else:
        logger.warning(f"⚠️ Ongeldige result: {result}")
        return settings

    logger.info(f"🧬 Morph: RR aangepast van {old_rr} naar {settings['rr']}")
    return settings
