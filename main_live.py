
"""
📄 Bestand: main_live.py
🔍 Doel: Realtime signaaltrigger voor AION
🧩 Gebruikt door: CLI, scheduler, live-runner
📦 Behoort tot: cli/
🧠 Gebruikt nieuwe loggingstructuur
"""

from aion_core.utils.logger import log

def execute_signal(signal, context_data):
    if not context_data:
        log("⚠️ Geen context data beschikbaar voor signaal.", level="warning")
        return

    try:
        log(f"🚀 Signaal uitgevoerd: {signal}", level="info")
        # signal.do_trade()  # Uitgecommentarieerd voor veiligheid
    except Exception as e:
        log(f"💥 Fout in trading loop: {e}", level="error")
