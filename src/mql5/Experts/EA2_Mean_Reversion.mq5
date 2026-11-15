//+------------------------------------------------------------------+
//|                                         EA2_Mean_Reversion.mq5   |
//|  Execution EA 2: Session Extremes & Value Fades                  |
//+------------------------------------------------------------------+
#property copyright "Autonomous Agentic AI Trading System"
#property link      "https://antigravity.google"
#property version   "1.00"

#include <TradeBridge.mqh>

input ulong   InpMagicNumber       = 102002;
input int     InpBBPeriod          = 20;
input double  InpBBDeviation       = 2.5;
input int     InpRSIPeriod         = 14;
input double  InpRSIOverbought     = 70.0;
input double  InpRSIOversold       = 30.0;
input int     InpATRPeriod         = 14;
input double  InpSL_ATRMult        = 1.2;
input double  InpTP_RRRatio        = 1.8;

int h_bb, h_rsi, h_atr;
CTradeBridge *bridge;

int OnInit()
  {
   bridge = new CTradeBridge(_Symbol, InpMagicNumber);
   h_bb   = iBands(_Symbol, _Period, InpBBPeriod, 0, InpBBDeviation, PRICE_CLOSE);
   h_rsi  = iRSI(_Symbol, _Period, InpRSIPeriod, PRICE_CLOSE);
   h_atr  = iATR(_Symbol, _Period, InpATRPeriod);

   return (h_bb != INVALID_HANDLE && h_rsi != INVALID_HANDLE &&
           h_atr != INVALID_HANDLE) ? INIT_SUCCEEDED : INIT_FAILED;
  }

void OnDeinit(const int reason)
  {
   IndicatorRelease(h_bb);
   IndicatorRelease(h_rsi);
   IndicatorRelease(h_atr);
   if(CheckPointer(bridge) == POINTER_DYNAMIC) delete bridge;
  }

void OnTick()
  {
   // Check regime gate & bench status
   // if(bridge.GetCurrentRegime() != REGIME_RANGE) return;
   if(bridge.IsBenched() || bridge.IsCircuitBreakerTripped()) return;

   // Enforce max 1 concurrent trade for this EA
   for(int i = PositionsTotal() - 1; i >= 0; i--)
     {
      if(PositionGetTicket(i) > 0)
        {
         if(PositionGetString(POSITION_SYMBOL) == _Symbol && 
            PositionGetInteger(POSITION_MAGIC) == InpMagicNumber)
            return;
        }
     }

   double bb_base[2], bb_upper[2], bb_lower[2], rsi[2], atr[1];
   if(CopyBuffer(h_bb, 0, 0, 2, bb_base) < 2 ||
      CopyBuffer(h_bb, 1, 0, 2, bb_upper) < 2 ||
      CopyBuffer(h_bb, 2, 0, 2, bb_lower) < 2 ||
      CopyBuffer(h_rsi, 0, 0, 2, rsi) < 2 ||
      CopyBuffer(h_atr, 0, 0, 1, atr) < 1) return;

   double ask = SymbolInfoDouble(_Symbol, SYMBOL_ASK);
   double bid = SymbolInfoDouble(_Symbol, SYMBOL_BID);
   double sl_distance = atr[0] * InpSL_ATRMult;
   double tp_distance = sl_distance * InpTP_RRRatio;
   double risk_pct    = bridge.GetAllocatedRiskPct(0.5);
   double lot         = bridge.CalculateLotSize(sl_distance, risk_pct);

   // Mean Reversion Buy: Price pierced lower band and RSI is oversold then hooking back up
   if(bid <= bb_lower[1] && rsi[1] <= InpRSIOversold && rsi[0] > InpRSIOversold)
     {
      double sl = ask - sl_distance;
      double tp = ask + tp_distance;
      bridge.OpenPosition(ORDER_TYPE_BUY, lot, sl, tp, "EA2 Range Fade Buy");
     }
   // Mean Reversion Sell: Price pierced upper band and RSI is overbought then hooking down
   else if(ask >= bb_upper[1] && rsi[1] >= InpRSIOverbought && rsi[0] < InpRSIOverbought)
     {
      double sl = bid + sl_distance;
      double tp = bid - tp_distance;
      bridge.OpenPosition(ORDER_TYPE_SELL, lot, sl, tp, "EA2 Range Fade Sell");
     }
  }
