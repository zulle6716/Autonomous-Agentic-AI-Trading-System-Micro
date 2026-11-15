"""
Performance & Risk Metrics Calculator
"""
from typing import List, Dict, Any
import math

def calculate_drawdown_series(equity_curve: List[float]) -> Dict[str, float]:
    """Calculate peak equity, current drawdown, and max drawdown percentage."""
    if not equity_curve:
        return {"peak": 0.0, "current_drawdown_pct": 0.0, "max_drawdown_pct": 0.0}
    
    peak = equity_curve[0]
    max_dd = 0.0
    
    for val in equity_curve:
        if val > peak:
            peak = val
        dd = (peak - val) / peak * 100.0 if peak > 0 else 0.0
        if dd > max_dd:
            max_dd = dd
            
    current_val = equity_curve[-1]
    current_dd = (peak - current_val) / peak * 100.0 if peak > 0 else 0.0
    return {
        "peak": peak,
        "current_equity": current_val,
        "current_drawdown_pct": current_dd,
        "max_drawdown_pct": max_dd
    }

def calculate_sharpe_ratio(returns: List[float], risk_free_rate: float = 0.0, periods_per_year: int = 252) -> float:
    """Calculate annualized Sharpe ratio."""
    if len(returns) < 2:
        return 0.0
    mean_ret = sum(returns) / len(returns)
    variance = sum((r - mean_ret) ** 2 for r in returns) / (len(returns) - 1)
    std_dev = math.sqrt(variance)
    if std_dev == 0.0:
        return 0.0
    return (mean_ret - risk_free_rate) / std_dev * math.sqrt(periods_per_year)

def calculate_profit_factor(trades_pnl: List[float]) -> float:
    """Calculate profit factor (gross profits / gross losses)."""
    gross_profit = sum(p for p in trades_pnl if p > 0)
    gross_loss = abs(sum(p for p in trades_pnl if p < 0))
    if gross_loss == 0.0:
        return 99.0 if gross_profit > 0 else 0.0
    return gross_profit / gross_loss

def calculate_consecutive_losses(trades_pnl: List[float]) -> int:
    """Calculate consecutive loss streak ending at the most recent trade."""
    streak = 0
    for pnl in reversed(trades_pnl):
        if pnl < 0:
            streak += 1
        else:
            break
    return streak
