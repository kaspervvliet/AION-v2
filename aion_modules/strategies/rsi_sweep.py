from aion_core.ai.strategy_interface import StrategyInterface

class RsiSweep(StrategyInterface):
    name = "rsi_sweep"

    def validate_market(self, recent_logs):
        # TODO: vervang dit met echte validatielogica
        return True
