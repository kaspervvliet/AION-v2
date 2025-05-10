"""
📄 Bestand: performance_tracker.py
🔍 Doel: Houdt setup-performance bij in geheugen of logbestand
🧩 Gebruikt door: run_backtest, strategie-analyse
📦 Behoort tot: aion_core/performance/
🧠 Verwacht implementatie van: safe_io, supabase_writer (optioneel)
"""

from datetime import datetime
from aion_core.utils.logger import logger
from aion_core.utils.safe_io import safe_write_json
from typing import List, Dict, Any
import plotly.graph_objs as go


class PerformanceTracker:
    def __init__(self):
        self.trades: List[Dict[str, Any]] = []
        self.total_trades = 0
        self.win_rate = 0.0
        self.avg_rr = 0.0

    def load_results(self, trades: List[Dict[str, Any]]) -> None:
        self.trades = trades
        self.total_trades = len(trades)
        self._analyze()

    def _analyze(self) -> None:
        wins = [t for t in self.trades if t.get("result") == "win"]
        losses = [t for t in self.trades if t.get("result") == "loss"]
        self.win_rate = len(wins) / self.total_trades * 100 if self.total_trades else 0
        self.avg_rr = sum(t.get("rr", 0) for t in self.trades) / self.total_trades if self.total_trades else 0
        logger.info(f"📊 Trades: {self.total_trades}, Winrate: {self.win_rate:.2f}%, Avg RR: {self.avg_rr:.2f}")

    def save_to_file(self, path: str = "results/perf_log.json") -> None:
        timestamp = datetime.utcnow().isoformat()
        safe_write_json(path, {
            "timestamp": timestamp,
            "trades": self.trades,
            "summary": {
                "total_trades": self.total_trades,
                "win_rate": self.win_rate,
                "avg_rr": self.avg_rr
            }
        })

    def plot_equity_curve(self):
        equity = 100
        equity_curve = [equity]
        for trade in self.trades:
            rr = trade.get("rr", 0)
            result = trade.get("result")
            equity += equity * rr if result == "win" else equity * -0.01  # 1% verlies als placeholder
            equity_curve.append(equity)

        fig = go.Figure()
        fig.add_trace(go.Scatter(y=equity_curve, mode='lines', name='Equity'))
        fig.update_layout(title='📈 Equity Curve', xaxis_title='Trade', yaxis_title='Balance')
        return fig
