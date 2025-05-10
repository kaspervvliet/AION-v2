"""
📄 Bestand: main_backtest.py
🔍 Doel: CLI-runner voor backtests met AION-strategieën
🧩 Gebruikt door: Dev/debug sessions, backtest workflows
📦 Behoort tot: /
🧠 Verwacht implementatie van: strategy_executor, adaptive_strategy_selector
"""

import argparse
from aion_core.kernel.strategy_executor import run_strategy_on_market
from aion_core.kernel.adaptive_strategy_selector import select_best_strategy
from aion_core.utils.logger import logger
from config import get_config
from aion_core.backtest.context_manager import create_context
from aion_core.database.supabase_writer import upload_backtest_results


def main():
    parser = argparse.ArgumentParser(description="AION V2 Backtest Runner")
    parser.add_argument("--symbol", type=str, default="SOL/USDT", help="Trading pair")
    parser.add_argument("--tf", type=str, default="15m", help="Timeframe (15m, 1h, etc.)")
    parser.add_argument("--limit", type=int, default=500, help="How many candles to load")
    args = parser.parse_args()

    logger.info(f"🚀 Start AION backtest voor {args.symbol} op {args.tf} ({args.limit} candles)")

    config = get_config()
    context = create_context(symbol=args.symbol, timeframe=args.tf, limit=args.limit)

    best_strategy = select_best_strategy(context)
    logger.info(f"🧠 Gekozen strategie: {best_strategy.__class__.__name__}")

    results = run_strategy_on_market(strategy=best_strategy, context=context)

    if results:
        logger.info("✅ Resultaten gegenereerd, upload naar Supabase...")
        upload_backtest_results(results, strategy_name=best_strategy.__class__.__name__)
    else:
        logger.warning("⚠️ Geen resultaten gegenereerd.")

if __name__ == "__main__":
    main()
