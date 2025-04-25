"""
📄 Bestand: safe_io.py
🔍 Doel: Beheert veilige file I/O voor Render-compatibiliteit
🧩 Gebruikt door: core modules, strategie-helpers
📦 Behoort tot: aion_core/utils/
"""

import os
import json
from aion_core.utils.logger import logger

AION_ENV = os.getenv("AION_ENV", "dev")  # render / dev / test

class UnsafeWriteError(Exception):
    pass

def safe_open(path, mode):
    if "w" in mode or "a" in mode:
        if AION_ENV == "render":
            raise UnsafeWriteError(f"Write operation blocked on Render: {path}")
    return open(path, mode, encoding="utf-8")

def read_json_file(path):
    try:
        with safe_open(path, "r") as f:
            return json.load(f)
    except Exception as e:
        logger.warning(f"[safe_io] Fout bij lezen JSON: {e}")
        return {}

def write_json_file(path, data):
    if AION_ENV == "render":
        raise UnsafeWriteError(f"Attempt to write JSON file on Render: {path}")
    with safe_open(path, "w") as f:
        json.dump(data, f, indent=2)

# Compatibiliteit met oudere imports
safe_load_json = read_json_file
