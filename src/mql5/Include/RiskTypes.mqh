//+------------------------------------------------------------------+
//|                                                    RiskTypes.mqh |
//|        Autonomous Agentic AI Trading System - Data Structures    |
//+------------------------------------------------------------------+
#property copyright "Autonomous Agentic AI Trading System"
#property link      "https://antigravity.google"
#property strict

//--- Market Regimes
enum ENUM_MARKET_REGIME
  {
   REGIME_UNCERTAIN = 0, // Inactive / High Noise
   REGIME_TREND     = 1, // Trend / Momentum -> EA 1
   REGIME_RANGE     = 2, // Mean Reverting / Sideways -> EA 2
   REGIME_BREAKOUT  = 3  // Volatility Expansion -> EA 3
  };

//--- Execution Direction
enum ENUM_SIGNAL_DIRECTION
  {
   SIGNAL_NONE = 0,
   SIGNAL_BUY  = 1,
   SIGNAL_SELL = -1
  };

//--- Strategy Parameters struct
struct StrategyRiskConfig
  {
   double base_risk_pct;
   double max_risk_pct;
   double daily_loss_limit_pct;
   double max_portfolio_dd_pct;
   bool   is_benched;
   double confidence_score;
  };
