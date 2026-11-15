//+------------------------------------------------------------------+
//|                                        EA3_Session_Breakout.mq5  |
//|  Execution EA 3: Opening Range & Volatility Expansion            |
//+------------------------------------------------------------------+
#property copyright "Autonomous Agentic AI Trading System"
#property link      "https://antigravity.google"
#property version   "1.00"

#include <TradeBridge.mqh>

input ulong   InpMagicNumber       = 103003;
input int     InpLookbackBars      = 16;
input int     InpBufferPoints      = 50;
input int     InpATRPeriod         = 14;
input double  InpSL_ATRMult        = 1.0;
input double  InpTP_RRRatio        = 2.5;

int h_atr;
CTradeBridge *bridge;

int OnInit()
  {
   bridge = new CTradeBridge(_Symbol, InpMagicNumber);
   h_atr  = iATR(_Symbol, _Period, InpATRPeriod);
   return (h_atr != INVALID_HANDLE) ? INIT_SUCCEEDED : INIT_FAILED;
  }

void OnDeinit(const int reason)
  {
   IndicatorRelease(h_atr);
   if(CheckPointer(bridge) == POINTER_DYNAMIC) delete bridge;
  }

void OnTick()
  {
   // Check regime gate & bench status
   // if(bridge.GetCurrentRegime() != REGIME_BREAKOUT) return;
   if(bridge.IsBenched() || bridge.IsCircuitBreakerTripped()) return;

   // Enforce max 1 concurrent position
   for(int i = PositionsTotal() - 1; i >= 0; i--)
     {
      if(PositionGetTicket(i) > 0)
        {
         if(PositionGetString(POSITION_SYMBOL) == _Symbol && 
            PositionGetInteger(POSITION_MAGIC) == InpMagicNumber)
            return;
        }
     }

   double high_arr[], low_arr[], atr[1];
   ArraySetAsSeries(high_arr, true);
   ArraySetAsSeries(low_arr, true);

   if(CopyHigh(_Symbol, _Period, 1, InpLookbackBars, high_arr) < InpLookbackBars ||
      CopyLow(_Symbol, _Period, 1, InpLookbackBars, low_arr) < InpLookbackBars ||
      CopyBuffer(h_atr, 0, 0, 1, atr) < 1) return;

   double highest_high = high_arr[0];
   double lowest_low   = low_arr[0];
   for(int i = 1; i < InpLookbackBars; i++)
     {
      if(high_arr[i] > highest_high) highest_high = high_arr[i];
      if(low_arr[i] < lowest_low)   lowest_low   = low_arr[i];
     }

   double ask = SymbolInfoDouble(_Symbol, SYMBOL_ASK);
   double bid = SymbolInfoDouble(_Symbol, SYMBOL_BID);
   double point = SymbolInfoDouble(_Symbol, SYMBOL_POINT);
   double buffer = InpBufferPoints * point;

   double sl_distance = atr[0] * InpSL_ATRMult;
   double tp_distance = sl_distance * InpTP_RRRatio;
   double risk_pct    = bridge.GetAllocatedRiskPct(0.5);
   double lot         = bridge.CalculateLotSize(sl_distance, risk_pct);

   // Bullish Breakout above range high
   if(ask > (highest_high + buffer))
     {
      double sl = ask - sl_distance;
      double tp = ask + tp_distance;
      bridge.OpenPosition(ORDER_TYPE_BUY, lot, sl, tp, "EA3 Volatility Breakout Buy");
     }
   // Bearish Breakdown below range low
   else if(bid < (lowest_low - buffer))
     {
      double sl = bid + sl_distance;
      double tp = bid - tp_distance;
      bridge.OpenPosition(ORDER_TYPE_SELL, lot, sl, tp, "EA3 Volatility Breakout Sell");
     }
  }
