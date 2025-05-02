"""
📄 Bestand: rsi_sweep.py
🔍 Doel: RSI Sweep-strategie met entry op sweep + FVG + BOS
🧩 Gebruikt door: strategy_pool_initializer, kernel.signal_engine
📦 Behoort tot: aion_modules/strategies
🧠 Verwacht implementatie van: StrategyInterface
"""
from aion_core.ai.strategy_interface import StrategyInterface
from aion_core.utils.risk_manager import calculate_sl_tp
from aion_core.utils.logger import get_logger
from aion_core.knowledge.concepts import is_sweep, find_fvg, detect_bos

class RsiSweep(StrategyInterface):
    name = "rsi_sweep"
    logger = get_logger(__name__)

    def get_metadata(self):
        return {
            "name": self.name,
            "description": "Detecteert sweep onder RSI-conditie + FVG + BOS confirmatie.",
            "author": "AION DevPilot",
            "version": "1.0",
            "tags": ["sweep", "fvg", "bos", "rsi"]
        }

    def validate_market(self, recent_logs):
        if not recent_logs or len(recent_logs) < 10:
            return False
        return True

    def generate_signal(self, df, context):
        last = df.iloc[-1]
        if not is_sweep(df):
            return None
        if not detect_bos(df):
            return None
        fvg = find_fvg(df)
        if fvg is None:
            return None
        self.log("Valid sweep + BOS + FVG gedetecteerd.")
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
        sl, tp = calculate_sl_tp(entry, direction=signal["direction"], rr=2.0)
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
        self.logger.info(f"[RSI Sweep] {message}")
