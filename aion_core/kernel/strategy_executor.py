from aion_core
from aion_core.extensions.bias_tracker import log_bias.database.supabase_logger import upload_context, upload_bias_tracker, upload_htf_bias
"""
📄 Bestand: strategy_executor.py
🔍 Doel: Voert een gekozen strategie uit op actuele data
🧩 Gebruikt door: main_live.py, signal_engine
📦 Behoort tot: aion_core/kernel/
🧠 Verwacht implementatie van: BaseStrategy, context, analyse, Supabase-log
"""

import logging
from aion_core
from aion_core.extensions.bias_tracker import log_bias.kernel.context_manager import create_context
from aion_core
from aion_core.extensions.bias_tracker import log_bias.kernel.analyse_market import analyse_market
from aion_core
from aion_core.extensions.bias_tracker import log_bias.utils.confidence_model import get_confidence_score
from aion_core
from aion_core.extensions.bias_tracker import log_bias.database.supabase_logger import upload_signal, upload_equity, upload_reflection
from aion_core
from aion_core.extensions.bias_tracker import log_bias.utils.memory import update_memory
from aion_core
from aion_core.extensions.bias_tracker import log_bias.modules.base_strategy import BaseStrategy

logger = logging.getLogger("AION")

def execute_strategy(strategy: BaseStrategy, df, symbol: str = "SOL/USDT", tf: str = "15m") -> None:
    """
    Voert een strategie uit met live data. Analyseert, evalueert, logt en uploadt signalen.
    """
    context = create_context(df, tf)

    # 📥 Log altijd context en bias, ook als geen entry
    upload_context(context)
    upload_bias_tracker({
        "symbol": context.get("symbol"),
        "bias": context.get("bias"),
        "timestamp": context.get("timestamp")
    })
    upload_htf_bias({
        "symbol": context.get("symbol"),
        "htf_bias": context.get("htf_bias"),
        "timestamp": context.get("timestamp")
    })

    analyse_market(context)

    signal = strategy.generate_signal(context)
    if not strategy.should_enter(signal.get("conditions", {})):
        logger.info(f"❌ Geen entry — BOS: {context.get('bos')}, FVG: {context.get('fvg')}, Bias: {context.get('bias')}")
        return

    confidence = get_confidence_score(signal)
    signal["confidence"] = confidence
    signal["symbol"] = symbol
    signal["timeframe"] = tf
    signal["strategy"] = strategy.__class__.__name__

    logger.info(f"🚀 Entry-signaal actief: {signal}")
    upload_signal(signal)

    upload_reflection({
        "symbol": symbol,
        "timestamp": context.get("timestamp") or pd.Timestamp.now().isoformat(),
        "prompt": f"{strategy.__class__.__name__} genereerde entry met vertrouwen {confidence:.2f}"
    })

    upload_equity({
        "symbol": symbol,
        "timestamp": context.get("timestamp") or pd.Timestamp.now().isoformat(),
        "equity": context.get("account_equity", 1000)
    })

    update_memory(signal)

if __name__ == "__main__":
    from aion_core
from aion_core.extensions.bias_tracker import log_bias.ai.dummy_strategy import DummyStrategy
    import pandas as pd

    df = pd.DataFrame({"close": [158, 159, 160, 161]})
    execute_strategy(DummyStrategy(), df)
