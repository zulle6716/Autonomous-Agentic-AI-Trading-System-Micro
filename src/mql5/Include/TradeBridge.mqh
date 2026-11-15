//+------------------------------------------------------------------+
//|                                                  TradeBridge.mqh |
//|  Micro Edition: IPC, Safety Bridge & Fractional Lot Sizer        |
//+------------------------------------------------------------------+
#property copyright "Autonomous Agentic AI Trading System (Micro Edition)"
#property link      "https://antigravity.google"
#property strict

#include <Trade\Trade.mqh>
#include "RiskTypes.mqh"

class CTradeBridge
  {
private:
   string             m_symbol;
   ulong              m_magic;
   CTrade             m_trade;

public:
                     CTradeBridge(string symbol, ulong magic)
     {
      m_symbol = symbol;
      m_magic  = magic;
      m_trade.SetExpertMagicNumber(magic);
      m_trade.SetMarginMode();
      m_trade.SetTypeFillingBySymbol(symbol);
     }
                    ~CTradeBridge() {}

   //--- Global Variable Keys
   string            GetRegimeKey() { return "SYS_REGIME_" + m_symbol; }
   string            GetBenchKey()  { return "SYS_BENCH_EA_" + IntegerToString(m_magic); }
   string            GetRiskKey()   { return "SYS_RISK_EA_" + IntegerToString(m_magic); }
   string            GetCircuitBreakerKey() { return "SYS_CIRCUIT_BREAKER_ACTIVE"; }

   //--- Query Active Market Regime
   ENUM_MARKET_REGIME GetCurrentRegime()
     {
      string key = GetRegimeKey();
      if(GlobalVariableCheck(key))
         return (ENUM_MARKET_REGIME)((int)GlobalVariableGet(key));
      return REGIME_UNCERTAIN;
     }

   //--- Set Market Regime (called by MarketRegimeIdentifier)
   void              SetCurrentRegime(ENUM_MARKET_REGIME regime)
     {
      GlobalVariableSet(GetRegimeKey(), (double)regime);
     }

   //--- Check if this specific EA is benched by Benching Agent
   bool              IsBenched()
     {
      string key = GetBenchKey();
      if(GlobalVariableCheck(key))
         return (GlobalVariableGet(key) > 0.5);
      string flag = "SYS_BENCH_EA_" + IntegerToString(m_magic) + ".flag";
      if(FileIsExist(flag, 0) || FileIsExist(flag, FILE_COMMON))
         return true;
      return false;
     }

   //--- Check if Master Emergency Circuit Breaker is active
   bool              IsCircuitBreakerTripped()
     {
      string key = GetCircuitBreakerKey();
      if(GlobalVariableCheck(key))
         return (GlobalVariableGet(key) > 0.5);
      if(FileIsExist("SYS_CIRCUIT_BREAKER_ACTIVE.flag", 0) || FileIsExist("SYS_CIRCUIT_BREAKER_ACTIVE.flag", FILE_COMMON))
         return true;
      return false;
     }

   //--- Query dynamic equity risk allocated by Portfolio Risk Manager
   double            GetAllocatedRiskPct(double default_risk = 0.4)
     {
      string key = GetRiskKey();
      if(GlobalVariableCheck(key))
        {
         double r = GlobalVariableGet(key);
         if(r > 0.05 && r <= 2.0) return r;
        }
      return default_risk;
     }

   //--- Calculate Lot Size based on risk percentage and stop loss distance
   double            CalculateLotSize(double sl_distance_price, double risk_pct)
     {
      if(sl_distance_price <= 0.0) return 0.0;
      double equity = AccountInfoDouble(ACCOUNT_EQUITY);
      double risk_amount = equity * (risk_pct / 100.0);
      
      double tick_value = SymbolInfoDouble(m_symbol, SYMBOL_TRADE_TICK_VALUE);
      double tick_size  = SymbolInfoDouble(m_symbol, SYMBOL_TRADE_TICK_SIZE);
      if(tick_size <= 0.0 || tick_value <= 0.0) return 0.01;

      double ticks_at_risk = sl_distance_price / tick_size;
      double loss_per_lot  = ticks_at_risk * tick_value;
      if(loss_per_lot <= 0.0) return 0.01;

      double raw_lot = risk_amount / loss_per_lot;
      
      double min_lot  = SymbolInfoDouble(m_symbol, SYMBOL_VOLUME_MIN);
      double max_lot  = SymbolInfoDouble(m_symbol, SYMBOL_VOLUME_MAX);
      double lot_step = SymbolInfoDouble(m_symbol, SYMBOL_VOLUME_STEP);
      if(lot_step <= 0.0) lot_step = 0.01;

      double lot = MathFloor(raw_lot / lot_step) * lot_step;
      if(lot < min_lot) lot = min_lot;
      if(lot > max_lot) lot = max_lot;

      // Safety check: if min_lot risks > 2.5x the desired risk amount on micro accounts, block or warn
      double min_lot_loss = loss_per_lot * min_lot;
      if(min_lot_loss > risk_amount * 2.5 && equity < 250.0)
        {
         Print("WARNING [Micro Sizer]: Min lot (", min_lot, ") risk ($", DoubleToString(min_lot_loss, 2), 
               ") exceeds risk budget ($", DoubleToString(risk_amount, 2), ").");
        }

      int lot_digits = 2;
      if(lot_step <= 0.001) lot_digits = 3;
      else if(lot_step <= 0.01) lot_digits = 2;
      else if(lot_step <= 0.1) lot_digits = 1;
      else lot_digits = 0;

      return NormalizeDouble(lot, lot_digits);
     }

   //--- Execution Wrapper with Built-in Safeguards
   bool              OpenPosition(ENUM_ORDER_TYPE order_type, double volume, double sl, double tp, string comment="")
     {
      if(IsBenched() || IsCircuitBreakerTripped())
        {
         Print("TRADE BLOCKED: EA ", m_magic, " is benched or circuit breaker tripped.");
         return false;
        }

      double price = (order_type == ORDER_TYPE_BUY) ? 
                     SymbolInfoDouble(m_symbol, SYMBOL_ASK) : 
                     SymbolInfoDouble(m_symbol, SYMBOL_BID);

      return m_trade.PositionOpen(m_symbol, order_type, volume, price, sl, tp, comment);
     }
  };
