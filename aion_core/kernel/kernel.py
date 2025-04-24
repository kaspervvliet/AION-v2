from .memory import log_setup, log_outcome
from .confidence_model import compute_confidence
from . import morph_engine

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
        return KernelDecision(status, confidence, reason)

    def observe_trade(self, setup: dict, outcome: dict):
        morph_engine.adjust_threshold(outcome)
        log_outcome(setup, outcome)

kernel = Kernel()
