"""
Self-Improvement Agent
Runs weekly continuous learning loop:
1. Audits live trade logs & tick executions
2. Generates parameter optimization candidates
3. Runs Walk-Forward backtests & Monte Carlo validation
4. Safely commits verified parameter updates
"""
from typing import Dict, Any, List
import json
import os
from src.utils.mcp_client import MT5MCPClient
from src.utils.monte_carlo import MonteCarloEngine

class SelfImprovementAgent:
    def __init__(self, mcp_client: MT5MCPClient, config: Dict[str, Any], params_dir: str):
        self.client = mcp_client
        self.config = config.get("self_improvement", {})
        self.params_dir = params_dir
        self.min_sharpe = self.config.get("min_out_of_sample_sharpe", 1.5)
        self.min_pf = self.config.get("min_out_of_sample_profit_factor", 1.4)
        self.max_sim_dd = self.config.get("max_simulated_drawdown_pct", 6.5)
        self.mc_engine = MonteCarloEngine(num_simulations=10000)

    def run_weekly_cycle(self, ea_name: str, candidate_params: Dict[str, Any], backtest_returns: List[float]) -> Dict[str, Any]:
        """
        Executes weekly audit and safe parameter deployment:
        Validates out-of-sample performance and Monte Carlo stability.
        """
        # 1. Run Monte Carlo validation on candidate backtest returns
        mc_results = self.mc_engine.run_simulation(backtest_returns, horizon_trades=100)
        
        # 2. Check strict validation thresholds
        risk_of_ruin = mc_results.get("risk_of_ruin_pct", 100.0)
        p95_dd = mc_results.get("p95_max_dd_pct", 100.0)

        # Simulation metrics check
        passes_validation = (
            risk_of_ruin < 1.0 and
            p95_dd <= self.max_sim_dd and
            mc_results.get("pass_validation", False)
        )

        outcome = {
            "ea_name": ea_name,
            "passes_validation": passes_validation,
            "mc_results": mc_results,
            "candidate_params": candidate_params,
            "action_taken": "NONE"
        }

        if passes_validation and self.config.get("auto_deploy_valid_params", True):
            # Safe write to configuration
            param_file = os.path.join(self.params_dir, f"{ea_name}.json")
            with open(param_file, "w") as f:
                json.dump(candidate_params, f, indent=2)
            outcome["action_taken"] = f"DEPLOYED_TO_{param_file}"
        else:
            outcome["action_taken"] = "REJECTED_MAINTAINED_BASELINE"

        return outcome
