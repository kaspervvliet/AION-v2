"""
📄 Bestand: kernel.py
🔍 Doel: Kernel voor evaluatie + observatie van trades
🧩 Gebruikt door: main, web_entry, strategieën
📦 Behoort tot: aion_core
🧠 Supabase logging geactiveerd
"""

from .memory import log_setup, log_outcome
from .confidence_model import compute_confidence
from . import morph_engine
from aion_core.supabase_client import log_decision, log_outcome as supa_outcome

class KernelDecision:
    def __init__(self, status: str, confidence: float, reason: str):
        self.status = status
        self.confidence = confidence
        self.reason = reason

class Kernel:
    def evaluate(self, setup: dict) -> KernelDecision:
        confidence, reason = compute_confidence(setup)
        status = "GO" if confidence > 0.7 else "CAUTION" if confidence > 0.5 else "SKIP"
        log_setup(setup, confidence, status)

        decision = KernelDecision(status, confidence, reason)
        log_decision(setup, decision.__dict__)  # Supabase logging
        return decision

    def observe_trade(self, setup: dict, outcome: dict):
        morph_engine.adjust_threshold(outcome)
        log_outcome(setup, outcome)
        supa_outcome(setup, outcome)  # Supabase logging

kernel = Kernel()
