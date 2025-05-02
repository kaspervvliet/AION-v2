"""
📄 Bestand: mean_revert_chopbox.py
🔍 Doel: Mean Revert-strategie in chopbox ranges met FVG + Sweep + BOS
🧩 Gebruikt door: strategy_pool_initializer, kernel.signal_engine
📦 Behoort tot: aion_modules/strategies
🧠 Verwacht implementatie van: StrategyInterface
"""
from aion_core.ai.strategy_interface import StrategyInterface
from aion_core.utils.risk_manager import calculate_sl_tp
from aion_core.utils.logger import get_logger
from aion_core.knowledge.concepts import is_range_bound, find_fvg, detect_bos, is_sweep

class MeanRevertChopbox(StrategyInterface):
    name = "mean_revert_chopbox"
    logger = get_logger(__name__)

    def get_metadata(self):
        return {
            "name": self.name,
            "description": "Reageert op sweep + BOS binnen een rangebound chopbox met FVG als entryzone.",
            "author": "AION DevPilot",
            "version": "1.0",
            "tags": ["range", "sweep", "fvg", "bos"]
        }

    def validate_market(self, recent_logs):
        if not recent_logs or len(recent_logs) < 20:
            return False
        return is_range_bound(recent_logs)

    def generate_signal(self, df, context):
        last = df.iloc[-1]
        if not is_range_bound(df):
            return None
        if not is_sweep(df):
            return None
        if not detect_bos(df):
            return None
        fvg = find_fvg(df)
        if fvg is None:
            return None
        self.log("Sweep + BOS + FVG binnen chopbox geactiveerd.")
        return {
            "entry": last.close,
            "direction": "long",
            "fvg": fvg,
            "context_snapshot": context.snapshot()
        }

    def build_trade(self, signal, df):
        if signal is None:
            return None
        entry = signal["entry"]
        sl, tp = calculate_sl_tp(entry, direction=signal["direction"], rr=1.5)
        trade = {
            "entry": entry,
            "sl": sl,
            "tp": tp,
            "direction": signal["direction"],
            "meta": {
                "strategy": self.name,
                "fvg": signal["fvg"]
            }
        }
        self.log(f"Trade gebouwd: {trade}")
        return trade

    def log(self, message):
        self.logger.info(f"[Mean Revert Chopbox] {message}")
