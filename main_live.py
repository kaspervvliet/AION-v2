"""
📄 Bestand: main_live.py
🔍 Doel: Realtime signaaltrigger voor AION
🧩 Gebruikt door: CLI, scheduler, live-runner
📦 Behoort tot: cli/
🧠 Gebruikt strategie_executor + adaptive selector
"""

from aion_core.utils.logger import log
from aion_core.utils.kraken import get_recent_ohlc
from aion_core.context.context_manager import AionContext
from aion_core.kernel.strategy_executor import evaluate_all
from aion_core.adaptive_strategy_selector import select_adaptive_strategy


def execute_signal(signal, context_data):
    if not context_data:
        log("⚠️ Geen context data beschikbaar voor signaal.", level="warning")
        return
    try:
        log(f"🚀 Signaal uitgevoerd: {signal}", level="info")
        # signal.do_trade()  # Uitgecommentarieerd voor veiligheid
    except Exception as e:
        log(f"💥 Fout in trading loop: {e}", level="error")


def main():
    df = get_recent_ohlc("SOL/USDT", interval="15m")
    context = AionContext(df)

    selected = select_adaptive_strategy(context)
    if not selected:
        log("❌ Geen strategie geselecteerd.", level="warning")
        return

    trades = evaluate_all(df, context)
    if not trades:
        log("🔍 Geen signalen gegenereerd.", level="info")
        return

    for t in trades:
        log(f"✅ Signaal: {t['strategy']} | Entry: {t['trade']['entry']} | TP: {t['trade']['tp']} | SL: {t['trade']['sl']}", level="success")
        execute_signal(t, context)


if __name__ == "__main__":
    main()
