"""
Vectorized 10,000-Step Monte Carlo Walk-Forward Simulation Engine
"""
from typing import List, Dict, Any
import random
import math

class MonteCarloEngine:
    def __init__(self, num_simulations: int = 10000, ruin_drawdown_threshold: float = 10.0):
        self.num_simulations = num_simulations
        self.ruin_drawdown_threshold = ruin_drawdown_threshold

    def run_simulation(self, trade_returns_pct: List[float], horizon_trades: int = 100) -> Dict[str, Any]:
        """
        Executes a 10,000-step bootstrapping/resampling Monte Carlo simulation.
        
        :param trade_returns_pct: Historical sequence of trade returns in percentage (e.g. [+1.5, -0.8, ...])
        :param horizon_trades: Number of forward trades to simulate per path
        :return: Risk of Ruin %, Probability of DD > 10%, Median Max DD, Worst Max DD
        """
        if not trade_returns_pct:
            return {
                "simulations": self.num_simulations,
                "risk_of_ruin_pct": 100.0,
                "prob_dd_exceeds_threshold": 100.0,
                "median_max_dd_pct": 100.0,
                "worst_max_dd_pct": 100.0,
                "pass_validation": False
            }

        ruin_count = 0
        threshold_breach_count = 0
        sim_max_dds = []

        n_samples = len(trade_returns_pct)

        for _ in range(self.num_simulations):
            # Resample trades with replacement
            sampled_trades = [trade_returns_pct[random.randint(0, n_samples - 1)] for _ in range(horizon_trades)]
            
            # Walk forward equity curve
            equity = 100.0
            peak = 100.0
            max_dd = 0.0
            ruined = False

            for ret in sampled_trades:
                equity *= (1.0 + ret / 100.0)
                if equity > peak:
                    peak = equity
                dd = (peak - equity) / peak * 100.0 if peak > 0 else 0.0
                if dd > max_dd:
                    max_dd = dd
                if dd >= self.ruin_drawdown_threshold:
                    ruined = True

            if ruined:
                ruin_count += 1
            if max_dd >= self.ruin_drawdown_threshold:
                threshold_breach_count += 1

            sim_max_dds.append(max_dd)

        sim_max_dds.sort()
        median_dd = sim_max_dds[int(self.num_simulations * 0.50)]
        p95_dd = sim_max_dds[int(self.num_simulations * 0.95)]
        worst_dd = sim_max_dds[-1]

        risk_of_ruin = (ruin_count / self.num_simulations) * 100.0
        prob_breach = (threshold_breach_count / self.num_simulations) * 100.0

        # Pass criteria: Risk of Ruin < 1.0% and 95th-percentile Max DD < 8.0%
        passes = (risk_of_ruin < 1.0) and (p95_dd < 8.0)

        return {
            "simulations": self.num_simulations,
            "horizon_trades": horizon_trades,
            "risk_of_ruin_pct": round(risk_of_ruin, 2),
            "prob_dd_exceeds_threshold": round(prob_breach, 2),
            "median_max_dd_pct": round(median_dd, 2),
            "p95_max_dd_pct": round(p95_dd, 2),
            "worst_max_dd_pct": round(worst_dd, 2),
            "pass_validation": passes
        }
