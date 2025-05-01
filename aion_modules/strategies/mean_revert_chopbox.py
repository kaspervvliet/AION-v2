from aion_core.ai.strategy_interface import StrategyInterface

class MeanRevertChopbox(StrategyInterface):
    name = "mean_revert_chopbox"

    def validate_market(self, recent_logs):
        # TODO: vervang dit met echte validatielogica
        return True
