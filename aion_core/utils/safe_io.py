"""
📄 Bestand: safe_io.py
🔍 Doel: Beheert veilige file I/O voor Render-compatibiliteit
🧩 Gebruikt door: core modules, strategie-helpers
📦 Behoort tot: aion_core/utils/
"""

import os
import json
from typing import Any
from aion_core.utils.logger import logger

AION_ENV = os.getenv("AION_ENV", "dev")  # render / dev / test

class UnsafeWriteError(Exception):
    pass

def safe_open(path: str, mode: str):
    if "w" in mode or "a" in mode:
        if AION_ENV == "render":
            raise UnsafeWriteError(f"Write operation blocked on Render: {path}")
    return open(path, mode, encoding="utf-8")

def read_json_file(path: str) -> dict[str, Any]:
    try:
        with safe_open(path, "r") as f:
            return json.load(f)
    except Exception as e:
        logger.warning(f"[safe_io] ❌ Fout bij lezen JSON {path}: {e}")
        return {}

def write_json_file(path: str, data: dict[str, Any]) -> None:
    if AION_ENV == "render":
        raise UnsafeWriteError(f"Attempt to write JSON file on Render: {path}")
    with safe_open(path, "w") as f:
        json.dump(data, f, indent=2)

if __name__ == "__main__":
    test_path = "test_config.json"
    try:
        write_json_file(test_path, {"env": "test"})
        cfg = read_json_file(test_path)
        print("✅ JSON inlezen gelukt:", cfg)
    except UnsafeWriteError as e:
        print(f"⛔ Render block: {e}")
