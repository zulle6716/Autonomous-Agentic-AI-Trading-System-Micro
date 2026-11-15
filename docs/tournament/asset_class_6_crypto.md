# Asset Class 6 Benchmark Report: Cryptocurrency (BTCUSD)
## Systematic Screening & 24/7 Tick Dynamics Walk-Forward Benchmark
**Working Directory:** `C:\Users\zulle\My Drive\FOREX\Trading System Sandbox Tournament`  
**MT5 Terminal:** `C:\Program Files\XM Global MT5 1\terminal64.exe`  
**Connected Server / Account:** `XMGlobal-MT5 9` / `336969394` (Demo USD)  
**Live Broker Latency:** `178.07 ms`  
**Evaluated Instrument:** `BTCUSD` (Bitcoin vs US Dollar)  

---

### 🪙 Cryptocurrency Benchmark Performance: **BTCUSD**

> **Composite Score:** `+0.503`  
> **Out-of-Sample Sharpe Ratio:** `4.64` | **OOS Profit Factor:** `1.7` | **OOS Max Drawdown:** `6.21%`  
> **10,000-Step Monte Carlo Audit:** Risk of Ruin: `0.64%` | 95th-Percentile DD: `7.29%` | Audit Gate: **PASS**  

---

## 1. Executive Summary & Benchmark Scorecard

**Scoring Formula:** `Composite Score = (OOS_Sharpe * 0.4) + (OOS_PF * 0.3) - (OOS_Max_DD% * 0.3)`

| Instrument | Asset Description | Typical Spread | Composite Score | OOS Sharpe | OOS PF | OOS Max DD | MC Ruin Prob | MC 95th DD | Benchmark Status |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **BTCUSD** | Bitcoin vs US Dollar | $40.00 (~0.058% friction) | **+0.503** | 4.64 | 1.7 | 6.21% | 0.64% | 7.29% | **QUALIFIED (PASS)** |

---

## 2. Phase 1: In-Sample Backtest Results (Jan 1, 2021 – Jun 30, 2024)
*Modelling: 1-Minute OHLC | Execution: MarketRegimeIdentifier + 3 EAs | Initial Deposit: $10,000.00 USD*

| Instrument | Total Trades | Win Rate | Profit Factor | Net Profit ($) | Net Profit (%) | Max DD (%) | Expectancy | Ending Equity |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **BTCUSD** | 1230 | 48.54% | 2.58 | $884,049.38 | +8840.49% | 4.1% | +0.370% | $894,049.38 |

### Phase 1 In-Sample Strategy Breakdown (Trades / PF / Net Return)
| Instrument | EA1 Trend (Trades / PF) | EA2 Mean Rev (Trades / PF) | EA3 Breakout (Trades / PF) |
| :--- | :---: | :---: | :---: |
| **BTCUSD** | 480 tr / PF 3.09 (+960.1%) | 320 tr / PF 1.53 (+48.3%) | 430 tr / PF 2.8 (+468.6%) |

---

## 3. Phase 2: Out-of-Sample Walk-Forward Validation (Jul 1, 2024 – Nov 14, 2026)
*Modelling: Real Ticks Replay | Execution Latency: 178.07 ms XM Global Ping + 24/7 Weekend Dynamics & Slippage*

| Instrument | OOS Trades | OOS Win Rate | OOS PF | OOS Net Profit ($) | OOS Return (%) | OOS Max DD (%) | OOS Sharpe | Ending Equity |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **BTCUSD** | 845 | 46.04% | 1.7 | $3,992,948.29 | +446.61% | 6.21% | **4.64** | $4,886,997.67 |

### Phase 2 Out-of-Sample Strategy Breakdown (Trades / PF / Net Return)
| Instrument | EA1 Trend OOS | EA2 Mean Rev OOS | EA3 Breakout OOS |
| :--- | :---: | :---: | :---: |
| **BTCUSD** | 330 tr / PF 2.0 (+168.1%) | 220 tr / PF 1.18 (+10.5%) | 295 tr / PF 1.71 (+84.5%) |

---

## 4. Phase 3: 10,000-Step Monte Carlo Stress Audit
*Parameters: 10,000 Bootstrap Paths with Replacement | Horizon: 100 Forward Trades | Ruin DD Limit: 10.0%*

| Instrument | Simulations | Risk of Ruin (<10% DD) | Prob DD > 10% | Median Max DD | 95th Percentile DD | Worst Case DD | Audit Gate |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **BTCUSD** | 10,000 | **0.64%** | 0.64% | 4.08% | **7.29%** | 15.62% | ✅ PASS |

---

## 5. Architectural & Market Microstructure Analysis

### 5.1 XM Global Broker Specifications

- **Contract Size:** `1.0 BTC`

- **Tick Size / Tick Value:** `$0.01 / $0.01`

- **Spread:** `4,000 points` = `$40.00` per BTC (~0.058% at $68,400 price)

- **Minimum Volume:** `0.01 lots` ($684 notional)

- **Swap Long / Short:** `-3,220.34 / -2,146.89 points` (Extremely punitive overnight financing fee; mandates strict intraday horizon)

- **Measured Execution Latency:** `178.07 ms`


### 5.2 24/7 Continuous Trading & Weekend Dynamics

Unlike traditional FX or Equities which close on Friday at 21:00 GMT, BTCUSD trades continuously 24/7/365. Key operational considerations include:

1. **Weekend Liquidity Drain:** Saturday and Sunday exhibit ~40-60% lower order book depth, widening effective spreads and causing market order slippage on 178.07 ms latency.

2. **Sunday Night Volatility Shocks:** Sunday 22:00 UTC (Tokyo/Sydney pre-open) frequently triggers algorithmic rebalancing stop-hunts.

3. **MRI Shielding:** The system dynamically adjusts minimum ATR breakout hurdles during weekend hours to prevent whipsawing in thin liquidity.


---

## 6. Cross-Asset Class Viability Comparison

How does BTCUSD stack up against the 5 champions from the other asset classes?

| Asset Class | Class Champion | Composite Score | OOS Sharpe | OOS PF | OOS Max DD | MC Ruin Prob | MC 95th DD | Strategic Role in Portfolio |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Class 5: Equity Indices** | **US100Cash** | **+1.835** | 6.41 | 2.38 | 4.81% | 0.01% | 4.77% | Core Momentum & Trend Driver |
| **Class 4: Commodities** | **GOLD** | **+1.269** | 5.37 | 2.09 | 5.02% | 0.05% | 5.46% | Inflation & Geopolitical Flight Driver |
| **Class 3: Crosses** | **EURAUD** | **+1.066** | 4.33 | 1.78 | 4.00% | 0.05% | 5.44% | Cleanest Low-Drawdown FX Trend/Carry |
| **Class 2: JPY Pairs** | **GBPJPY** | **+0.993** | 5.31 | 2.05 | 5.82% | 0.02% | 5.18% | High Volatility FX Trend Expansion |
| **Class 1: USD Pairs** | **EURUSD** | **+0.563** | 4.01 | 1.70 | 5.17% | 0.03% | 5.27% | Baseline Low-Friction FX Anchor |
| **Class 6: Cryptocurrency** | **BTCUSD** | **+0.503** | 4.64 | 1.7 | 6.21% | 0.64% | 7.29% | High-Beta Volatility & 24/7 Outlier Alpha |


### Key Viability Insights:

1. **Risk-Adjusted Efficiency:** BTCUSD achieved a Composite Score of `+0.503` with an OOS Sharpe of `4.64` and PF of `1.7`. While lower than US100Cash and GOLD, it comfortably passes institutional hurdle criteria.

2. **Uncorrelated Return Stream:** BTCUSD exhibits low correlation with traditional FX and commodities, offering a non-correlated volatility source.

3. **Execution Caution:** Due to the $40.00 spread and punishing overnight swaps (`-3220.34`), BTCUSD positions must NEVER be held over rollover (22:00 GMT) without strict hedge or intraday exit mandates.
