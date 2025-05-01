# 📄 Bestand: aion_ai_agent.py
# Nieuwe AION V2.5 agent — kiest en activeert best passende strategie

import datetime
from aion_core.ai.supabase_reader import get_recent_logs
from aion_core.ai.strategy_selector import select_best_strategy
from aion_core.ai.entry_engine import generate_entry_payload
from supabase import create_client
import os

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY") or os.getenv("SUPABASE_SERVICE_ROLE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def evaluate_and_execute(logs_limit: int = 10):
    strategies = set()
    all_logs = []

    print("📥 Ophalen van logs...")
    rows = supabase.table("strategy_logs").select("*").order("timestamp", desc=True).limit(100).execute()
    for row in rows.data:
        strategies.add(row["strategy"])
        all_logs.append(row)

    print("🔍 Strategieën valideren...")
    for strategy in strategies:
        logs = [log for log in all_logs if log["strategy"] == strategy][:logs_limit]
        if not logs:
            continue

        selected = select_best_strategy(logs)
        if selected and selected.name == strategy:
            print(f"✅ '{strategy}' gevalideerd als best passende strategie")

            entry = generate_entry_payload(strategy)
            print(f"📈 Entry gegenereerd: {entry}")

            supabase.table("strategy_signals").insert({
                "strategy": entry["strategy"],
                "entry_price": entry["entry"],
                "stop_loss": entry["stop_loss"],
                "take_profit": entry["take_profit"],
                "risk_reward_ratio": entry["risk_reward_ratio"],
                "timestamp": datetime.datetime.utcnow().isoformat()
            }).execute()
            return entry

    print("⚠️ Geen geldige strategie gevonden op dit moment.")
    return None
