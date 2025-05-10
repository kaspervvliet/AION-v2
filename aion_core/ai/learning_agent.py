"""
📄 Bestand: learning_agent.py
🔍 Doel: Past strategy bias aan op basis van win/loss resultaat
🧩 Gebruikt door: morph_engine (AI tuning)
📦 Behoort tot: aion_core/ai/
🧠 Verwacht implementatie van: load_morph_state(), write_json_file()
"""

from aion_core.helpers.morph_state_loader import load_morph_state
from aion_core.utils.safe_io import write_json_file
import logging
from typing import Literal

logger = logging.getLogger("AION")

MAX_LOG_LEN = 20

def evaluate_outcome(strategy_name: str, result: Literal["win", "loss"]) -> None:
    """
    Verhoogt of verlaagt morph confidence op basis van resultaat.
    """
    state = load_morph_state()
    current = state.get("min_confidence_go", 0.7)
    boost = state.get("boost_on_win", 0.02)
    penalty = state.get("penalty_on_loss", 0.03)

    if result == "win":
        new_value = min(state["max"], current + boost)
        reason = f"Win boost (+{boost})"
    else:
        new_value = max(state["min"], current - penalty)
        reason = f"Loss penalty (-{penalty})"

    state["min_confidence_go"] = round(new_value, 4)
    logger.info(f"🧠 Nieuwe confidence threshold: {new_value} ({reason})")

    state["mutation_log"].append({
        "strategy": strategy_name,
        "result": result,
        "new_threshold": new_value,
        "reason": reason
    })

    # Truncate log
    state["mutation_log"] = state["mutation_log"][-MAX_LOG_LEN:]
    write_json_file("morph_state.json", state)

if __name__ == "__main__":
    evaluate_outcome("test-strategy", "win")
    evaluate_outcome("test-strategy", "loss")
