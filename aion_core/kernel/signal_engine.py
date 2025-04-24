
from aion_core.kernel import trade_explainer
from aion_core.supabase_client import insert
from aion_core.kernel import reflection

def propose_trade(run_id: str, setup: dict, outcome: dict, decision: str, confidence: float, reason: str):
    rr = outcome.get("rr", 0)
    if decision != "GO" or rr < 1.5:
        print(f"[SIGNAL] Trade genegeerd: status={decision}, rr={rr}")
        return None

    explanation = trade_explainer.explain_decision(setup, decision, confidence, reason)

    signal = {
        "run_id": run_id,
        "setup": setup,
        "outcome": outcome,
        "confidence": confidence,
        "reason": reason,
        "rr": rr,
        "explanation": explanation,
        "timestamp": outcome.get("timestamp")
    }

    print("[SIGNAL] 💡 Voorstel gegenereerd:")
    print(explanation)

    insert("signals", signal)
    return signal
