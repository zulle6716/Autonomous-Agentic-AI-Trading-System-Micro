//+------------------------------------------------------------------+
//|                                        EA1_Trend_Momentum.mq5    |
//|  Execution EA 1: Intraday Trend Continuation & Dynamic Pullbacks |
//+------------------------------------------------------------------+
#property copyright "Autonomous Agentic AI Trading System"
#property link      "https://antigravity.google"
#property version   "1.00"

#include <TradeBridge.mqh>

input ulong   InpMagicNumber       = 101001;
input int     InpFastEMA           = 21;
input int     InpSlowEMA           = 55;
input int     InpTrendEMA          = 200;
input int     InpRSIPeriod         = 14;
input double  InpRSILower          = 45.0;
input double  InpRSIUpper          = 55.0;
input int     InpATRPeriod         = 14;
input double  InpSL_ATRMult        = 1.5;
input double  InpTP_ATRMult        = 3.0;

int h_fast_ema, h_slow_ema, h_trend_ema, h_rsi, h_atr;
CTradeBridge *bridge;

int OnInit()
  {
   bridge = new CTradeBridge(_Symbol, InpMagicNumber);
   h_fast_ema  = iMA(_Symbol, _Period, InpFastEMA, 0, MODE_EMA, PRICE_CLOSE);
   h_slow_ema  = iMA(_Symbol, _Period, InpSlowEMA, 0, MODE_EMA, PRICE_CLOSE);
   h_trend_ema = iMA(_Symbol, _Period, InpTrendEMA, 0, MODE_EMA, PRICE_CLOSE);
   h_rsi       = iRSI(_Symbol, _Period, InpRSIPeriod, PRICE_CLOSE);
   h_atr       = iATR(_Symbol, _Period, InpATRPeriod);

   return (h_fast_ema != INVALID_HANDLE && h_slow_ema != INVALID_HANDLE &&
           h_trend_ema != INVALID_HANDLE && h_rsi != INVALID_HANDLE &&
           h_atr != INVALID_HANDLE) ? INIT_SUCCEEDED : INIT_FAILED;
  }

void OnDeinit(const int reason)
  {
   IndicatorRelease(h_fast_ema);
   IndicatorRelease(h_slow_ema);
   IndicatorRelease(h_trend_ema);
   IndicatorRelease(h_rsi);
   IndicatorRelease(h_atr);
   if(CheckPointer(bridge) == POINTER_DYNAMIC) delete bridge;
  }

void OnTick()
  {
   // Check regime gate & bench status
   // if(bridge.GetCurrentRegime() != REGIME_TREND) return;
   if(bridge.IsBenched() || bridge.IsCircuitBreakerTripped()) return;

   // Check if already in an active position for this EA
   if(PositionsTotal() > 0)
     {
      for(int i = PositionsTotal() - 1; i >= 0; i--)
        {
         if(PositionGetTicket(i) > 0)
           {
            if(PositionGetString(POSITION_SYMBOL) == _Symbol && 
               PositionGetInteger(POSITION_MAGIC) == InpMagicNumber)
               return; // Only 1 active trade at a time per EA
           }
        }
     }

   double fast[2], slow[2], trend[2], rsi[2], atr[1];
   if(CopyBuffer(h_fast_ema, 0, 0, 2, fast) < 2 ||
      CopyBuffer(h_slow_ema, 0, 0, 2, slow) < 2 ||
      CopyBuffer(h_trend_ema, 0, 0, 2, trend) < 2 ||
      CopyBuffer(h_rsi, 0, 0, 2, rsi) < 2 ||
      CopyBuffer(h_atr, 0, 0, 1, atr) < 1) return;

   double ask = SymbolInfoDouble(_Symbol, SYMBOL_ASK);
   double bid = SymbolInfoDouble(_Symbol, SYMBOL_BID);
   double sl_distance = atr[0] * InpSL_ATRMult;
   double tp_distance = atr[0] * InpTP_ATRMult;
   double risk_pct    = bridge.GetAllocatedRiskPct(0.5);
   double lot         = bridge.CalculateLotSize(sl_distance, risk_pct);

   // Bullish Trend Continuation: Price > 200 EMA, Fast > Slow, RSI pulling back to support
   if(bid > trend[0] && fast[0] > slow[0] && rsi[1] <= InpRSILower && rsi[0] > InpRSILower)
     {
      double sl = ask - sl_distance;
      double tp = ask + tp_distance;
      bridge.OpenPosition(ORDER_TYPE_BUY, lot, sl, tp, "EA1 Trend Buy");
     }
   // Bearish Trend Continuation: Price < 200 EMA, Fast < Slow, RSI pulling back to resistance
   else if(ask < trend[0] && fast[0] < slow[0] && rsi[1] >= InpRSIUpper && rsi[0] < InpRSIUpper)
     {
      double sl = bid + sl_distance;
      double tp = bid - tp_distance;
      bridge.OpenPosition(ORDER_TYPE_SELL, lot, sl, tp, "EA1 Trend Sell");
     }
  }
