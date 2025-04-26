"""
📄 Bestand: web_entry.py
🔍 Doel: AION live loop inclusief echte HTF bias bepaling
🧩 Gebruikt door: Render deployment
📦 Behoort tot: AION v2
🧠 Verwacht implementatie van: AIONContext, analyse_market, kernel.evaluate, htf_context
"""

import time
from aion_core.context.htf_context import fetch_htf_candles, determine_htf_bias
from aion_core.kernel.kernel import kernel
from aion_core.utils.logger import logger
from aion_core.context.aion_context import AIONContext
from aion_core.context.market_structure import analyse_market

def live_loop():
    logger.info("🧠 AION live loop gestart...")
    ctx = AIONContext(symbol="SOL/USDT", timeframe="15m")

    while True:
        try:
            # ➔ Stap 1: HTF bias ophalen
            candles = fetch_htf_candles(symbol="SOLUSDT", interval=60)
            bias = determine_htf_bias(candles)
            logger.info(f"[HTF] 📈 Bepaalde bias: {bias}")

            # ➔ Stap 2: Laatste candle ophalen (LTF)
            candle = ctx.fetch_latest_candle()

            if candle:
                # ➔ Stap 3: Analyseer markt incl. bias
                setup = analyse_market(candle, bias=bias)
                decision = kernel.evaluate(setup)

                logger.info(f"Status: {decision.status}, Confidence: {decision.confidence}, Reason: {decision.reason}")

                if decision.status == "GO":
                    logger.info("🚀 GO - Trade activatie mogelijk")
                elif decision.status == "SKIP":
                    logger.info("⚠️ SKIP - Geen entry door HTF bias")
                else:
                    logger.info("🔎 CAUTION - Setup twijfelachtig")
            else:
                logger.warning("[LIVE_LOOP] Geen candle opgehaald.")

        except Exception as e:
            logger.warning(f"[LIVE_LOOP ERROR] {e}")

        time.sleep(15)

if __name__ == "__main__":
    live_loop()