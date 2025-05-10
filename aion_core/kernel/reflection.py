"""
📄 Bestand: reflection.py
🔍 Doel: Genereert AI-reflectieprompt op basis van run-resultaat
🧩 Gebruikt door: strategy_tester.py
📦 Behoort tot: aion_core/eval/
🧠 Verwacht implementatie van: generate_reflection_prompt()
"""

import logging
from typing import Dict

logger = logging.getLogger("AION")

MAX_PROMPT_LENGTH = 3000  # safeguard in tokens/karakters

def generate_reflection_prompt(run_result: Dict) -> str:
    """
    Maakt een GPT-prompt voor reflectie op basis van testresultaat.
    """
    context = run_result.get("context", {})
    setup = run_result.get("setup", {})
    result = run_result.get("result", {})

    prompt = (
        f"Context:\n{context}\n\n"
        f"Setup:\n{setup}\n\n"
        f"Resultaat:\n{result}\n\n"
        "Analyseer deze setup volgens Smart Money Concepts. Geef feedback over entrylogica, RR, structuur en verbeterpunten."
    )

    if len(prompt) > MAX_PROMPT_LENGTH:
        logger.warning(f"Reflectieprompt te lang ({len(prompt)} tekens). Ingekort.")
        prompt = prompt[:MAX_PROMPT_LENGTH]

    logger.info(f"🧠 Prompt gegenereerd ({len(prompt)} tekens)")
    return prompt

if __name__ == "__main__":
    dummy = {
        "context": {"bias": "long", "fvg": True},
        "setup": {"entry": 158.5, "sl": 155.0, "tp": 165.0},
        "result": {"success": True, "rr": 2.1}
    }
    print(generate_reflection_prompt(dummy))
