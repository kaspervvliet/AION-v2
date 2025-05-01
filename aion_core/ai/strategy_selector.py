# 📄 Bestand: strategy_selector.py
# Kiest de eerste strategie waarvan validate_market() True retourneert
# Nu met uitgebreide debug-output

from aion_core.ai.strategy_validator import available_strategies

def select_best_strategy(recent_logs):
    print(f"📊 Aantal logs ontvangen voor evaluatie: {len(recent_logs)}")

    for strategy in available_strategies:
        print(f"🧠 Evaluatie van strategie: {strategy.name}")
        try:
            result = strategy.validate_market(recent_logs)
            print(f"   → validate_market() gaf terug: {result}")
            if result:
                return strategy
        except Exception as e:
            print(f"❌ Fout bij strategie '{strategy.name}': {e}'")

    print("🚫 Geen strategie gevalideerd.")
    return None
