"""
📄 Bestand: memory.py
🔍 Doel: Houdt in-memory sessiestatus bij
🧩 Gebruikt door: kernel, strategieën, signal_engine
📦 Behoort tot: aion_core/utils/
🧠 Verwacht implementatie van: get_memory(), update_memory()
"""

import logging
from typing import Any

logger = logging.getLogger("AION")

MEMORY: dict[str, Any] = {}

def get_memory() -> dict:
    return MEMORY

def update_memory(key: str, value: Any) -> None:
    MEMORY[key] = value
    logger.debug(f"🧠 MEMORY update: {key} → {value}")

def clear_memory() -> None:
    MEMORY.clear()
    logger.info("🧠 MEMORY gewist")

if __name__ == "__main__":
    update_memory("mode", "live")
    print(get_memory())
    clear_memory()
