
"""
📄 Bestand: main_backtest.py
🔍 Doel: Draait een strategie als backtest zonder UI
🧩 Gebruikt door: devs, CI pipelines
📦 Behoort tot: projectroot
"""

from aion_core.loader import StrategyLoader
from aion_core.context import AIONContext
from aion_core import config

# Configuratie
STRATEGIE = "rsi_sweep"  # voorbeeldnaam
SYMBOL = "SOL/USDT"
TIMEFRAME = "15m"

# Initialiseer
loader = StrategyLoader()
module = loader.load_strategy(STRATEGIE)
StrategyClass = getattr(module, "Strategy", None)

if not StrategyClass:
    raise Exception("❌ Strategy class niet gevonden")

context = AIONContext(
    symbol=SYMBOL,
    timeframe=TIMEFRAME,
    supabase_url=config.SUPABASE_URL,
    supabase_key=config.SUPABASE_KEY
)
context.load_from_supabase()

strategy = StrategyClass(config={}, context=context)

print(f"\n🔄 Draai backtest voor strategie: {strategy.get_metadata().get('name')}")
print("Laatste prijs:", context.get_latest_price())
print("Entry signaal:", strategy.is_entry(context.candle_data))
