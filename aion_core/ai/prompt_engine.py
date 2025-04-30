import json
from typing import List, Dict

def generate_strategy_prompt(logs: List[Dict], strategy_name: str) -> str:
    if not logs:
        return f"Er zijn geen recente logs gevonden voor strategy '{strategy_name}'."

    json_logs = json.dumps(logs, indent=2, ensure_ascii=False)
    return f"""
Je bent een slimme trading-analist.

Analyseer de recente prestaties van strategy '{strategy_name}'.

Hier zijn de laatste {len(logs)} logs:
{json_logs}

Vraag:
- Wat valt op?
- Waarom zijn bepaalde trades mislukt?
- Welke signalen werkten wél?
- Wat zou je veranderen aan deze strategy?

Antwoord helder, gestructureerd en actiegericht.
"""
