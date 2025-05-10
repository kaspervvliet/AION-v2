"""
📄 Bestand: morph_state_loader.py
🔍 Doel: Valideert en laadt morph_state.json veilig
🧩 Gebruikt door: morph_engine (experimenteel)
📦 Behoort tot: aion_core/helpers/
🧠 Verwacht implementatie van: load_morph_state()
"""

import json
import logging
from typing import Any
from pathlib import Path

logger = logging.getLogger("AION")

DEFAULT_STATE = {
    "min_confidence_go": 0.7,
    "boost_on_win": 0.02,
    "penalty_on_loss": 0.03,
    "min": 0.5,
    "max": 0.95,
    "bias_weight": 1.0,
    "rsi_weight": 1.0,
    "mutation_log": []
}

ALLOWED_KEYS = set(DEFAULT_STATE.keys())

def load_morph_state(path: str = "morph_state.json") -> dict[str, Any]:
    """Laadt en valideert morph_state-bestand."""
    f = Path(path)
    if not f.exists():
        logger.warning("⚠️ morph_state.json niet gevonden — standaardwaarden gebruikt.")
        return DEFAULT_STATE.copy()

    try:
        data = json.loads(f.read_text())
        unknown_keys = set(data.keys()) - ALLOWED_KEYS
        if unknown_keys:
            logger.warning(f"⚠️ Onbekende velden in morph_state.json: {unknown_keys}")

        # Truncate mutation_log indien nodig
        if isinstance(data.get("mutation_log"), list) and len(data["mutation_log"]) > 20:
            data["mutation_log"] = data["mutation_log"][-20:]
            logger.info("✂️ mutation_log ingekort tot laatste 20 entries")

        return {**DEFAULT_STATE, **data}

    except Exception as e:
        logger.error(f"❌ Fout bij laden morph_state.json: {e}")
        return DEFAULT_STATE.copy()

if __name__ == "__main__":
    state = load_morph_state()
    print(state)
