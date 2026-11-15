"""
Benching Agent
Monitors EA performance and runs 10,000-step Monte Carlo Walk-Forward Simulation
whenever an EA underperforms par.
"""
from typing import Dict, Any, List
from src.utils.mcp_client import MT5MCPClient
from src.utils.monte_carlo import MonteCarloEngine
from src.utils.metrics import calculate_consecutive_losses, calculate_profit_factor, calculate_drawdown_series

class BenchingAgent:
    def __init__(self, mcp_client: MT5MCPClient, config: Dict[str, Any]):
        self.client = mcp_client
        self.config = config.get("benching", {})
        self.max_consecutive_losses = self.config.get("max_consecutive_losses", 3)
        self.rolling_7d_dd_limit = self.config.get("rolling_7d_drawdown_limit_pct", 3.0)
        self.rolling_window = self.config.get("rolling_trades_window", 15)
        self.min_pf = self.config.get("min_profit_factor_threshold", 1.10)
        self.mc_engine = MonteCarloEngine(num_simulations=self.config.get("monte_carlo_simulations", 10000))
        
        # Benched registry: magic_number -> bench state dict
        self.benched_eas: Dict[int, Dict[str, Any]] = {}

    def evaluate_ea(self, magic_number: int, recent_trades_pnl: List[float], recent_equity_curve: List[float]) -> Dict[str, Any]:
        """
        Evaluate performance against benching triggers:
        1. 3 consecutive losses
        2. Rolling 7-day DD > 3.0%
        3. Rolling 15-trade profit factor < 1.10
        """
        consecutive_losses = calculate_consecutive_losses(recent_trades_pnl)
        dd_metrics = calculate_drawdown_series(recent_equity_curve)
        current_dd = dd_metrics["current_drawdown_pct"]
        max_dd = dd_metrics["max_drawdown_pct"]
        
        window_trades = recent_trades_pnl[-self.rolling_window:] if len(recent_trades_pnl) >= self.rolling_window else recent_trades_pnl
        pf = calculate_profit_factor(window_trades)

        trigger_reasons = []
        if consecutive_losses >= self.max_consecutive_losses:
            trigger_reasons.append(f"CONSECUTIVE_LOSSES ({consecutive_losses} >= {self.max_consecutive_losses})")
        if max_dd >= self.rolling_7d_dd_limit:
            trigger_reasons.append(f"ROLLING_DD_BREACH (Max DD {max_dd:.2f}% >= {self.rolling_7d_dd_limit}%)")
        if len(window_trades) >= 5 and pf < self.min_pf:
            trigger_reasons.append(f"PROFIT_FACTOR_DECAY ({pf:.2f} < {self.min_pf})")

        should_bench = len(trigger_reasons) > 0

        result = {
            "magic_number": magic_number,
            "should_bench": should_bench,
            "trigger_reasons": trigger_reasons,
            "consecutive_losses": consecutive_losses,
            "current_drawdown_pct": round(current_dd, 2),
            "profit_factor": round(pf, 2),
            "mc_result": None
        }

        if should_bench:
            # 1. Instantly bench in MT5
            self.client.bench_ea(magic_number, benched=True)
            
            # 2. Run 10,000-Step Monte Carlo Walk-Forward Simulation
            mc_sim = self.mc_engine.run_simulation(recent_trades_pnl, horizon_trades=100)
            result["mc_result"] = mc_sim
            
            self.benched_eas[magic_number] = {
                "magic_number": magic_number,
                "reasons": trigger_reasons,
                "mc_result": mc_sim,
                "status": "BENCHED"
            }
        else:
            # If healthy and was previously benched, check if it can be restored
            if magic_number in self.benched_eas:
                self.client.bench_ea(magic_number, benched=False)
                del self.benched_eas[magic_number]
                result["status"] = "RESTORED"

        return result
