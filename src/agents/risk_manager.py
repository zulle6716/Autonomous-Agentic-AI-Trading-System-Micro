"""
Portfolio Risk Manager Agent (Micro Edition)
Enforces 10% max portfolio drawdown ceiling, 2.0% daily circuit breaker,
and dynamically sizes equity at risk per trade for micro accounts ($100 starting equity).
"""
from typing import Dict, Any, List
from src.utils.mcp_client import MT5MCPClient
from src.utils.metrics import calculate_drawdown_series

class PortfolioRiskManager:
    def __init__(self, mcp_client: MT5MCPClient, config: Dict[str, Any]):
        self.client = mcp_client
        self.config = config.get("system", {})
        self.max_dd_limit = self.config.get("max_portfolio_drawdown_pct", 10.0)
        self.daily_loss_limit = self.config.get("daily_loss_limit_pct", 2.0)
        self.max_concurrent_risk = self.config.get("max_concurrent_risk_pct", 2.0)
        self.base_risk = self.config.get("base_risk_per_trade_pct", 0.4)
        self.max_trade_risk = self.config.get("max_risk_per_trade_pct", 1.0)
        
        initial_equity = float(self.config.get("minimum_equity_usd", 100.0))
        self.day_start_equity = initial_equity
        self.high_water_mark = initial_equity

    def sync_equity(self, current_equity: float, is_new_day: bool = False):
        """Update current equity and daily/all-time benchmarks."""
        if is_new_day:
            self.day_start_equity = current_equity
            if self.high_water_mark <= 0.0 or self.high_water_mark == 10000.0:
                self.high_water_mark = current_equity
        if current_equity > self.high_water_mark:
            self.high_water_mark = current_equity

    def evaluate_circuit_breakers(self, current_equity: float) -> Dict[str, Any]:
        """
        Check daily loss and max portfolio drawdown thresholds.
        Returns whether circuit breaker tripped and the triggering reason.
        """
        self.sync_equity(current_equity)

        # 1. Total Portfolio Drawdown Check
        total_dd_pct = (self.high_water_mark - current_equity) / self.high_water_mark * 100.0 if self.high_water_mark > 0 else 0.0
        if total_dd_pct >= self.max_dd_limit:
            self.client.trigger_circuit_breaker(f"Max Portfolio Drawdown breached: {total_dd_pct:.2f}% >= {self.max_dd_limit}%")
            return {
                "tripped": True,
                "reason": "MAX_PORTFOLIO_DRAWDOWN_BREACHED",
                "total_dd_pct": total_dd_pct,
                "daily_dd_pct": 0.0
            }

        # 2. Daily Loss Limit Check
        daily_loss_pct = (self.day_start_equity - current_equity) / self.day_start_equity * 100.0 if self.day_start_equity > 0 else 0.0
        if daily_loss_pct >= self.daily_loss_limit:
            self.client.trigger_circuit_breaker(f"Daily Loss Limit breached: {daily_loss_pct:.2f}% >= {self.daily_loss_limit}%")
            return {
                "tripped": True,
                "reason": "DAILY_LOSS_LIMIT_BREACHED",
                "total_dd_pct": total_dd_pct,
                "daily_dd_pct": daily_loss_pct
            }

        return {
            "tripped": False,
            "reason": "NORMAL",
            "total_dd_pct": total_dd_pct,
            "daily_dd_pct": daily_loss_pct
        }

    def calculate_trade_risk(self, magic_number: int, regime_conviction: float = 1.0, win_streak: int = 0) -> float:
        """
        Calculate volatility-adjusted equity risk per trade:
        Base (0.4%) scaled by regime conviction (0.8 - 1.2) & win streak (0.7 - 1.3),
        bounded by [0.3%, max_trade_risk (1.0%)].
        """
        conviction_mult = max(0.8, min(1.2, regime_conviction))
        streak_mult = 1.0
        if win_streak >= 2:
            streak_mult = 1.2
        elif win_streak < 0: # Losing streak penalty
            streak_mult = max(0.6, 1.0 + (win_streak * 0.15))

        allocated_risk = self.base_risk * conviction_mult * streak_mult
        allocated_risk = max(0.3, min(self.max_trade_risk, allocated_risk))
        
        # Dispatch updated risk to MT5 terminal
        self.client.allocate_risk(magic_number, round(allocated_risk, 2))
        return round(allocated_risk, 2)
