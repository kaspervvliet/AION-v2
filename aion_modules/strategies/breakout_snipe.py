from aion_core.ai.strategy_interface import StrategyInterface

class BreakoutSnipe(StrategyInterface):
    name = "breakout_snipe"

    def validate_market(self, recent_logs):
        # TODO: vervang dit met echte validatielogica
        return True
