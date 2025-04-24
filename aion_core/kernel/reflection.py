
### aion_core/kernel/reflection.py ###
# Reflectie-engine: logt setups, outcomes en GPT-analyse naar Supabase

import json
import datetime
from aion_core.supabase_client import insert  # bestaande insert functie gebruiken

def build_prompt(setup: dict, outcome: dict, decision: str, confidence: float, reason: str) -> str:
    return (
        f"""Gegeven de volgende trading setup:
{json.dumps(setup, indent=2)}


        De strategie besloot: {decision} met confidence {confidence:.2f} omdat: {reason}

        De uitkomst was: TP={outcome.get('tp_hit')}, SL={outcome.get('sl_hit')}, RR={outcome.get('rr')}


        Wat zou AION in deze situatie kunnen verbeteren of leren? Wees kritisch maar compact."""
    )

def log_reflection(run_id: str, setup: dict, outcome: dict, decision: str, confidence: float, reason: str):
    prompt = build_prompt(setup, outcome, decision, confidence, reason)
    reflection = {
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "run_id": run_id,
        "setup": setup,
        "outcome": outcome,
        "decision": decision,
        "confidence": confidence,
        "reason": reason,
        "gpt_feedback": None,  # Kan later gevuld worden met OpenAI-call
        "prompt": prompt
    }
    print("[REFLECTION] Log:", json.dumps(reflection, indent=2))
    insert("reflections", reflection)  # Standaard Supabase insert
