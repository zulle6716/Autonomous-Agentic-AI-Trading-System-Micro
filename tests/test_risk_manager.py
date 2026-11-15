"""
Unit Tests for Portfolio Risk Manager & Circuit Breakers (Micro Edition - $100 Equity)
"""
import unittest
from src.utils.mcp_client import MT5MCPClient
from src.agents.risk_manager import PortfolioRiskManager

class TestPortfolioRiskManagerMicro(unittest.TestCase):
    def setUp(self):
        self.client = MT5MCPClient()
        self.config = {
            "system": {
                "minimum_equity_usd": 100.0,
                "max_portfolio_drawdown_pct": 10.0,
                "daily_loss_limit_pct": 2.0,
                "base_risk_per_trade_pct": 0.4,
                "max_risk_per_trade_pct": 1.0
            }
        }
        self.prm = PortfolioRiskManager(self.client, self.config)

    def test_micro_daily_loss_circuit_breaker(self):
        # Starting with $100 micro account
        self.prm.sync_equity(100.0, is_new_day=True)
        # Drop by 2.5% (down to $97.50, loss = $2.50 > $2.00 limit)
        status = self.prm.evaluate_circuit_breakers(97.50)
        self.assertTrue(status["tripped"])
        self.assertEqual(status["reason"], "DAILY_LOSS_LIMIT_BREACHED")
        self.assertAlmostEqual(status["daily_dd_pct"], 2.5, places=2)

    def test_micro_max_portfolio_drawdown_circuit_breaker(self):
        # Starting with $100 micro account
        self.prm.sync_equity(100.0, is_new_day=True)
        # Peak reaches $120.00
        self.prm.sync_equity(120.0, is_new_day=False)
        # Drop to $107.00 (10.83% DD from peak of $120.00)
        status = self.prm.evaluate_circuit_breakers(107.00)
        self.assertTrue(status["tripped"])
        self.assertEqual(status["reason"], "MAX_PORTFOLIO_DRAWDOWN_BREACHED")
        self.assertAlmostEqual(status["total_dd_pct"], 10.83, places=1)

    def test_micro_dynamic_risk_allocation(self):
        # Base risk: 0.4%
        risk = self.prm.calculate_trade_risk(magic_number=101001, regime_conviction=1.0, win_streak=0)
        self.assertEqual(risk, 0.4)

        # High conviction + win streak
        boosted_risk = self.prm.calculate_trade_risk(magic_number=101001, regime_conviction=1.2, win_streak=3)
        self.assertGreater(boosted_risk, 0.4)
        self.assertLessEqual(boosted_risk, 1.0)

if __name__ == "__main__":
    unittest.main()
