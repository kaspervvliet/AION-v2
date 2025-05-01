from aion_core.ai.strategy_interface import StrategyInterface

class BreakoutSnipe(StrategyInterface):
    name = "breakout_snipe"

    def validate_market(self, recent_logs):
        print(f"🔎 DEBUG — Ontvangen logs voor {self.name}:")
        for i, log in enumerate(recent_logs, start=1):
            print(f"  {i}. {log}")

        if not recent_logs or len(recent_logs) < 3:
            print("❌ Niet genoeg logs.")
            return False

        has_choch = any(log.get("entry_type") == "CHoCH" for log in recent_logs)
        non_bearish = all(log.get("bias") in ("neutral", "bullish") for log in recent_logs)
        no_sl_hits = all(log.get("sl_hit") == False for log in recent_logs[:3])

        print(f"✅ has_choch: {has_choch}")
        print(f"✅ non_bearish: {non_bearish}")
        print(f"✅ no_sl_hits: {no_sl_hits}")

        return has_choch and non_bearish and no_sl_hits
