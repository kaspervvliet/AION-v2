
## Bestand: aion_core/utils/context_validator.py

"""
📄 Bestand: aion_core/utils/context_validator.py
🔍 Doel: Valideert of Sweep en FVG aanwezig zijn voordat een entry wordt gemaakt.
🧩 Gebruikt door: Alle strategie-modules
📦 Behoort tot: aion_core/utils
🧠 Verwacht implementatie van: logging functie
"""

from aion_core.utils.logger import log  # Zorg dat je deze logfunctie hebt

def validate_entry_context(context_data: dict) -> bool:
    """
    Controleert of zowel sweep als FVG aanwezig zijn.

    Args:
        context_data (dict): Dictionary met keys 'sweep_confirmed' en 'valid_fvg_found'.

    Returns:
        bool: True als context valide is, False als niet.
    """
    sweep = context_data.get("sweep_confirmed", False)
    fvg = context_data.get("valid_fvg_found", False)

    if not sweep and not fvg:
        log("Entry skipped: No sweep confirmation and no valid FVG.", level="warning")
        return False
    if not sweep:
        log("Entry skipped: Missing sweep confirmation.", level="warning")
        return False
    if not fvg:
        log("Entry skipped: Missing valid FVG.", level="warning")
        return False

    return True
