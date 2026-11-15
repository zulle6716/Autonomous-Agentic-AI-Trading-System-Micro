"""
Unit Tests for Benching Agent and Trigger Conditions (Micro Edition)
"""
import unittest
from src.utils.mcp_client import MT5MCPClient
from src.agents.benching_agent import BenchingAgent

class TestBenchingAgentMicro(unittest.TestCase):
    def setUp(self):
        self.client = MT5MCPClient()
        self.config = {
            "benching": {
                "max_consecutive_losses": 3,
                "rolling_7d_drawdown_limit_pct": 3.0,
                "rolling_trades_window": 15,
                "min_profit_factor_threshold": 1.10,
                "monte_carlo_simulations": 1000
            }
        }
        self.agent = BenchingAgent(self.client, self.config)

    def test_benching_on_consecutive_losses_micro(self):
        # 3 consecutive micro losses ($0.30, $0.40, $0.25)
        trades = [1.00, 0.50, -0.30, -0.40, -0.25]
        equity = [100.0, 101.0, 101.50, 101.20, 100.80, 100.55]
        result = self.agent.evaluate_ea(101001, trades, equity)
        self.assertTrue(result["should_bench"])
        self.assertIn("CONSECUTIVE_LOSSES", result["trigger_reasons"][0])
        self.assertIsNotNone(result["mc_result"])

    def test_benching_on_drawdown_spike_micro(self):
        # 3.5% DD with no 3-loss streak ($3.50 loss on $100)
        trades = [1.00, -3.50, 0.50]
        equity = [100.0, 101.0, 97.50, 98.00]
        result = self.agent.evaluate_ea(102002, trades, equity)
        self.assertTrue(result["should_bench"])
        self.assertTrue(any("ROLLING_DD_BREACH" in r for r in result["trigger_reasons"]))

if __name__ == "__main__":
    unittest.main()
