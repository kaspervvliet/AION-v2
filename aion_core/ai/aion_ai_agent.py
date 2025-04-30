import datetime
from supabase_reader import get_recent_logs
from prompt_engine import generate_strategy_prompt
from llm_bridge import ask_llm
import os
from supabase import create_client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def store_feedback(strategy_name: str, gpt_feedback: str):
    now = datetime.datetime.utcnow().isoformat()
    result = supabase.table("strategy_feedback").insert({
        "strategy": strategy_name,
        "timestamp": now,
        "feedback_text": gpt_feedback,
        "source": "GPT-4"
    }).execute()
    return result

def evaluate_strategy(strategy_name: str, use_local_llm=False):
    logs = get_recent_logs(strategy_name)
    prompt = generate_strategy_prompt(logs, strategy_name)
    gpt_response = ask_llm(prompt, use_local=use_local_llm)

    print(f"\n🧠 GPT Feedback voor '{strategy_name}':\n{gpt_response}\n")

    store_result = store_feedback(strategy_name, gpt_response)
    if store_result.data:
        print(f"✅ Feedback opgeslagen in Supabase voor {strategy_name}.")
    else:
        print(f"⚠️ Feedback NIET opgeslagen — check Supabase policies of verbinding.")
