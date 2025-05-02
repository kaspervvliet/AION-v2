from aion_core.ai.strategy_interface import StrategyInterface

class AnalyseBosChoc(StrategyInterface):
    name = "analyse_bos_choc"

    def validate_market(self, recent_logs):
        if not recent_logs or len(recent_logs) < 3:
            return False

        # Zoek CHoCH gevolgd door BOS
        found_choc = False
        for i, log in enumerate(recent_logs):
            if log.get("entry_type") == "CHoCH":
                found_choc = True
                next_logs = recent_logs[i+1:i+3]
                for nlog in next_logs:
                    if nlog.get("entry_type") == "BOS":
                        break
                else:
                    found_choc = False
                break

        no_sl_hits = all(log.get("sl_hit") is False for log in recent_logs[:3])
        return found_choc and no_sl_hits
