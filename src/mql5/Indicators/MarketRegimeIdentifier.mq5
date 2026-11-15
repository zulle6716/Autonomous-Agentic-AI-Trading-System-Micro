//+------------------------------------------------------------------+
//|                                   MarketRegimeIdentifier.mq5     |
//|  Multi-Timeframe Regime Detection Engine for Antigravity AI       |
//+------------------------------------------------------------------+
#property copyright "Autonomous Agentic AI Trading System"
#property link      "https://antigravity.google"
#property version   "1.00"
#property indicator_chart_window
#property indicator_buffers 0
#property indicator_plots   0

#include <TradeBridge.mqh>

input ENUM_TIMEFRAMES InpHigherTF          = PERIOD_H1;  // Higher Timeframe for Trend
input ENUM_TIMEFRAMES InpLowerTF           = PERIOD_M15; // Lower Timeframe for Volatility
input int             InpFastEMAPeriod     = 21;         // Fast Trend EMA
input int             InpSlowEMAPeriod     = 55;         // Slow Trend EMA
input int             InpADXPeriod         = 14;         // ADX Period
input double          InpADXTrendThreshold = 25.0;       // ADX Trend Min Level
input double          InpADXRangeThreshold = 20.0;       // ADX Range Max Level
input int             InpATRPeriod         = 14;         // ATR Volatility Period
input double          InpBreakoutATRRatio  = 1.35;       // Ratio of current ATR to baseline

int    h_ema_fast;
int    h_ema_slow;
int    h_adx;
int    h_atr_curr;
int    h_atr_base;

CTradeBridge *bridge;
ENUM_MARKET_REGIME last_stable_regime = REGIME_UNCERTAIN;
int confirmation_count = 0;

//+------------------------------------------------------------------+
//| Custom indicator initialization function                         |
//+------------------------------------------------------------------+
int OnInit()
  {
   bridge = new CTradeBridge(_Symbol, 999999);

   h_ema_fast = iMA(_Symbol, InpHigherTF, InpFastEMAPeriod, 0, MODE_EMA, PRICE_CLOSE);
   h_ema_slow = iMA(_Symbol, InpHigherTF, InpSlowEMAPeriod, 0, MODE_EMA, PRICE_CLOSE);
   h_adx      = iADX(_Symbol, InpHigherTF, InpADXPeriod);
   h_atr_curr = iATR(_Symbol, InpLowerTF, InpATRPeriod);
   h_atr_base = iATR(_Symbol, InpLowerTF, InpATRPeriod * 6);

   if(h_ema_fast == INVALID_HANDLE || h_ema_slow == INVALID_HANDLE || 
      h_adx == INVALID_HANDLE || h_atr_curr == INVALID_HANDLE || h_atr_base == INVALID_HANDLE)
     {
      Print("Failed to initialize technical indicator handles.");
      return INIT_FAILED;
     }

   return INIT_SUCCEEDED;
  }

//+------------------------------------------------------------------+
//| Custom indicator deinitialization function                       |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
  {
   IndicatorRelease(h_ema_fast);
   IndicatorRelease(h_ema_slow);
   IndicatorRelease(h_adx);
   IndicatorRelease(h_atr_curr);
   IndicatorRelease(h_atr_base);
   if(CheckPointer(bridge) == POINTER_DYNAMIC)
      delete bridge;
  }

//+------------------------------------------------------------------+
//| Custom indicator iteration function                              |
//+------------------------------------------------------------------+
int OnCalculate(const int rates_total,
                const int prev_calculated,
                const datetime &time[],
                const double &open[],
                const double &high[],
                const double &low[],
                const double &close[],
                const long &tick_volume[],
                const long &volume[],
                const int &spread[])
  {
   if(rates_total < 50) return 0;

   double ema_fast[2], ema_slow[2], adx[1], atr_curr[1], atr_base[1];

   if(CopyBuffer(h_ema_fast, 0, 0, 2, ema_fast) < 2 ||
      CopyBuffer(h_ema_slow, 0, 0, 2, ema_slow) < 2 ||
      CopyBuffer(h_adx, 0, 0, 1, adx) < 1 ||
      CopyBuffer(h_atr_curr, 0, 0, 1, atr_curr) < 1 ||
      CopyBuffer(h_atr_base, 0, 0, 1, atr_base) < 1)
     {
      return prev_calculated;
     }

   double current_adx = adx[0];
   double current_atr = atr_curr[0];
   double baseline_atr = atr_base[0];
   double atr_ratio = (baseline_atr > 0.0) ? (current_atr / baseline_atr) : 1.0;

   ENUM_MARKET_REGIME raw_regime = REGIME_UNCERTAIN;

   // 1. Breakout / Volatility Expansion Condition
   if(atr_ratio >= InpBreakoutATRRatio)
     {
      raw_regime = REGIME_BREAKOUT;
     }
   // 2. Strong Trend / Momentum Condition
   else if(current_adx >= InpHigherTrendThreshold() && 
           MathAbs(ema_fast[1] - ema_slow[1]) > 0.0)
     {
      raw_regime = REGIME_TREND;
     }
   // 3. Range-bound / Mean Reverting Condition
   else if(current_adx <= InpADXRangeThreshold && atr_ratio < 1.1)
     {
      raw_regime = REGIME_RANGE;
     }
   else
     {
      raw_regime = REGIME_UNCERTAIN;
     }

   // Hysteresis Filter (2 Consecutive bar closes)
   if(raw_regime == last_stable_regime)
     {
      confirmation_count = 0;
     }
   else
     {
      confirmation_count++;
      if(confirmation_count >= 2)
        {
         last_stable_regime = raw_regime;
         confirmation_count = 0;
         bridge.SetCurrentRegime(last_stable_regime);
         PrintFormat("[MRI %s] Regime shift confirmed -> %s (ADX: %.2f, ATR Ratio: %.2f)", 
                     _Symbol, EnumToString(last_stable_regime), current_adx, atr_ratio);
        }
     }

   return rates_total;
  }

double InpHigherTrendThreshold() { return InpADXTrendThreshold; }
