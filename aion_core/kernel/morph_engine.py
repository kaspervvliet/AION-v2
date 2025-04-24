### aion_core/kernel/morph_engine.py ###
# Doel: parameters automatisch aanpassen obv trade-uitkomsten
# Werkt met eenvoudig JSON-bestand als opslag: morph_state.json

import json
import os

STATE_PATH = "morph_state.json"

# Default instellingen (fallback)
def get_default_state():
    return {
        "min_confidence_go": 0.7,
        "boost_on_win": 0.02,
        "penalty_on_loss": 0.03,
        "min": 0.5,
        "max": 0.95
    }

def load_state():
    if not os.path.exists(STATE_PATH):
        return get_default_state()
    with open(STATE_PATH, "r") as f:
        return json.load(f)

def save_state(state: dict):
    with open(STATE_PATH, "w") as f:
        json.dump(state, f, indent=2)

def adjust_threshold(outcome: dict):
    state = load_state()
    delta = -state["penalty_on_loss"] if outcome.get("sl_hit") else state["boost_on_win"]
    updated = state["min_confidence_go"] + delta
    state["min_confidence_go"] = max(state["min"], min(state["max"], updated))
    save_state(state)
    print(f"[MORPH] Adjusted min_confidence_go to {state['min_confidence_go']:.2f}")

def get_threshold():
    return load_state()["min_confidence_go"]


def mutate():
    state = load_state()
    now = datetime.datetime.utcnow().isoformat()

    # Voorbeeldmutatie: bias krijgt meer gewicht na winst
    state["bias_weight"] = min(2.0, round(state.get("bias_weight", 1.0) + 0.05, 2))

    # Log mutatie
    log = state.get("mutation_log", [])
    log.append({
        "timestamp": now,
        "change": "bias_weight ↑",
        "new_value": state["bias_weight"]
    })
    state["mutation_log"] = log

    save_state(state)
    print(f"[MORPH] bias_weight gemuteerd → {state['bias_weight']:.2f}")
