
"""
📄 Bestand: strategy_runner.py
🔍 Doel: Centrale live-loop runner voor AION strategie
🧩 Gebruikt door: main_live.py, web_entry.py
📦 Behoort tot: aion_core/kernel
🧠 Verwacht implementatie van: get_context, execute_strategy
"""

from aion_core.context.context_manager import get_context
from aion_core.kernel.strategy_executor import execute_strategy
from aion_core.utils.logger import logger

def run_signal_engine(symbol: str, strategy) -> None:
    """Haalt context op en voert strategie uit."""
    logger.info(f"⚙️ Nieuwe tick: context ophalen voor {symbol}")
    context = get_context(symbol)
    result = execute_strategy(symbol, context, strategy)

    if result:
        logger.info(f"📡 Signaal gegenereerd: {result}")
