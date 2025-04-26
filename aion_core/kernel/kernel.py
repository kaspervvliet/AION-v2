"""
📄 Bestand: kernel.py
🔍 Doel: Kernel voor evaluatie + observatie van trades
🧩 Gebruikt door: main, web_entry, strategieën
📦 Behoort tot: aion_core
🧠 Supabase logging geactiveerd + HTF-bias filtering
"""

from .memory import log_setup, log_outcome
from .confidence_model import compute_confidence
from . import morph_engine
from aion_core.supabase_client import log_decision, log_outcome as supa_outcome
from aion_core.context.htf_context import determine_htf_bias

class KernelDecision:
    def __init__(self, status: str, confidence: float, reason: str):
        self.status = status
        self.confidence = confidence
        self.reason = reason

class Kernel:
    def evaluate(self, setup: dict) -> KernelDecision:
        confidence, reason = compute_confidence(setup)
        status = "GO" if confidence > 0.7 else "CAUTION" if confidence > 0.5 else "SKIP"

        # 🔍 Haal HTF bias op
        symbol = setup.get("symbol", "UNKNOWN")
        bias = determine_htf_bias(symbol)

        # 🔒 Check op bias-confluence
        if setup.get("direction") == "LONG" and bias != "bullish":
            decision = KernelDecision("SKIP", 0.0, "no confluence")
            log_decision(setup, decision.__dict__)
            return decision

        if setup.get("direction") == "SHORT" and bias != "bearish":
            decision = KernelDecision("SKIP", 0.0, "no confluence")
            log_decision(setup, decision.__dict__)
            return decision

        decision = KernelDecision(status, confidence, reason)
        log_setup(setup, confidence, status)
        log_decision(setup, decision.__dict__)
        return decision

    def observe_trade(self, setup: dict, outcome: dict):
        morph_engine.adjust_threshold(outcome)
        log_outcome(setup, outcome)
        supa_outcome(setup, outcome)

kernel = Kernel()
