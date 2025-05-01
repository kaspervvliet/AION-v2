# 📄 Bestand: aion_ai_agent.py
# Orchestrator met GPT-evaluatie én automatische mute/activate logging

import datetime
import os
from aion_core.ai.supabase_reader import get_recent_logs
from aion_core.ai.prompt_engine import generate_strategy_prompt
from aion_core.ai.llm_bridge import ask_llm
from aion_core.ai.feedback_analyzer import extract_actions
from aion_core.ai.mute_controller import mute_strategy, activate_strategy
from supabase import create_client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY") or os.getenv("SUPABASE_SERVICE_ROLE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def store_feedback(strategy_name: str, gpt_feedback: str, mute: bool):
    now = datetime.datetime.utcnow().isoformat()
    result = supabase.table("strategy_feedback").insert({
        "strategy": strategy_name,
        "timestamp": now,
        "feedback_text": gpt_feedback,
        "mute_recommendation": mute,
        "source": "GPT-4"
    }).execute()
    return result

def evaluate_strategy(strategy_name: str, use_local_llm=False, llm_func=None):
    logs = get_recent_logs(strategy_name)
    prompt = generate_strategy_prompt(logs, strategy_name)
    llm_func = llm_func or ask_llm
    gpt_response = llm_func(prompt, use_local=use_local_llm)

    print(f"\n🧠 GPT Feedback voor '{strategy_name}':\n{gpt_response}\n")

    actions = extract_actions(gpt_response)
    store_result = store_feedback(strategy_name, gpt_response, actions["mute_strategy"])

    if store_result.data:
        print(f"✅ Feedback opgeslagen in Supabase voor {strategy_name}.")
        if actions["mute_strategy"]:
            print(f"🔇 Strategie '{strategy_name}' aanbevolen om tijdelijk te muten.")
            mute_strategy(strategy_name)
        else:
            print(f"🟢 Strategie '{strategy_name}' blijft actief.")
            activate_strategy(strategy_name)
    else:
        print(f"⚠️ Feedback NIET opgeslagen — check Supabase policies of verbinding.")
