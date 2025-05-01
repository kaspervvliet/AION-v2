from aion_core.ai.strategy_interface import StrategyInterface

class TrendFollowFVG(StrategyInterface):
    name = "trend_follow_fvg"

    def validate_market(self, recent_logs):
        if not recent_logs or len(recent_logs) < 3:
            return False

        bullish_logs = [log for log in recent_logs if log.get("bias") == "bullish"]
        fvg_signals = [log for log in recent_logs if log.get("entry_type") == "FVG"]

        # Vereist minimaal 2 bullish logs en ten minste 1 FVG-entry
        return len(bullish_logs) >= 2 and len(fvg_signals) >= 1
