"""
📄 Bestand: structure_awareness.py
🔍 Doel: Analyseert of BOS/CHoCH aanwezig is in structuurobject
🧩 Gebruikt door: kernel, strategieën, analyse
📦 Behoort tot: aion_core/knowledge/
🧠 Verwacht implementatie van: logger
"""

from aion_core.utils.logger import logger


def detect_bos(structure: dict) -> bool:
    if not structure or not isinstance(structure, dict):
        logger.warning("⚠️ Geen geldige structuur ontvangen (detect_bos)")
        return False

    result = structure.get("bos_up") or structure.get("bos_down")
    if not result:
        logger.info("ℹ️ Geen BOS in structuur")
    return bool(result)


def detect_choc(structure: dict) -> bool:
    if not structure or not isinstance(structure, dict):
        logger.warning("⚠️ Geen geldige structuur ontvangen (detect_choc)")
        return False

    result = structure.get("choc")
    if not result:
        logger.info("ℹ️ Geen CHoCH in structuur")
    return bool(result)
