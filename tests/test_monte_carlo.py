"""
Unit Tests for 10,000-Step Monte Carlo Simulation Engine
"""
import unittest
from src.utils.monte_carlo import MonteCarloEngine

class TestMonteCarloEngine(unittest.TestCase):
    def setUp(self):
        self.engine = MonteCarloEngine(num_simulations=5000, ruin_drawdown_threshold=10.0)

    def test_profitable_strategy_passes_mc(self):
        # 60% win rate, 1.5:1 R:R
        profitable_trades = [1.5, -1.0, 1.8, -0.9, 1.2, 2.0, -1.0, 1.4, -0.8, 1.6] * 10
        result = self.engine.run_simulation(profitable_trades, horizon_trades=50)
        self.assertLess(result["risk_of_ruin_pct"], 1.0)
        self.assertLess(result["p95_max_dd_pct"], 10.0)

    def test_losing_strategy_fails_mc(self):
        # Heavy losing trades
        losing_trades = [-2.5, -1.8, 0.5, -3.0, -1.2, -2.0, 0.8] * 10
        result = self.engine.run_simulation(losing_trades, horizon_trades=50)
        self.assertGreater(result["risk_of_ruin_pct"], 5.0)
        self.assertFalse(result["pass_validation"])

if __name__ == "__main__":
    unittest.main()
