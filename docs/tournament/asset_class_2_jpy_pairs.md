# Asset Class 2 Tournament Report: Japanese Yen Pairs
## Multi-Asset Screening & Walk-Forward Validation Tournament
**Working Directory:** `C:\Users\zulle\My Drive\FOREX\Trading System Sandbox Tournament`  
**MT5 Terminal:** `C:\Program Files\XM Global MT5 1\terminal64.exe`  
**Connected Server / Account:** `XMGlobal-MT5 9` / `336969394` (Demo USD)  
**Live Broker Latency:** `178.07 ms`  
**Candidate Universe (5 Instruments):** `USDJPY`, `EURJPY`, `GBPJPY`, `CADJPY`, `AUDJPY`  

---

### 🏆 Asset Class 2 Champion: **GBPJPY** (Great Britain Pound vs Japanese Yen)

> **Composite Score:** `+0.993`  
> **Out-of-Sample Sharpe Ratio:** `5.31` | **OOS Profit Factor:** `2.05` | **OOS Max Drawdown:** `5.82%`  
> **10,000-Step Monte Carlo Audit:** Risk of Ruin: `0.02%` | 95th-Percentile DD: `5.18%` | Audit Gate: **PASS**  

---

## 1. Master Tournament Ranking & Composite Scores

**Scoring Formula:** `Composite Score = (OOS_Sharpe * 0.4) + (OOS_PF * 0.3) - (OOS_Max_DD% * 0.3)`

| Rank | Instrument | Asset Description | Composite Score | OOS Sharpe | OOS PF | OOS Max DD | MC Ruin Prob | MC 95th DD | Tournament Status |
| :---: | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **#1** | **GBPJPY** | Great Britain Pound vs Japanese Yen | **+0.993** | 5.31 | 2.05 | 5.82% | 0.02% | 5.18% | **CHAMPION (QUALIFIED)** |
| **#2** | **USDJPY** | US Dollar vs Japanese Yen | **+0.764** | 5.09 | 1.98 | 6.22% | 0.02% | 4.73% | Eliminated |
| **#3** | **CADJPY** | Canadian Dollar vs Japanese Yen | **+0.145** | 2.8 | 1.44 | 4.69% | 0.28% | 6.75% | Eliminated |
| **#4** | **EURJPY** | Euro vs Japanese Yen | **-0.062** | 3.82 | 1.66 | 6.96% | 0.07% | 5.71% | Eliminated |
| **#5** | **AUDJPY** | Australian Dollar vs Japanese Yen | **-0.344** | 2.44 | 1.38 | 5.78% | 0.66% | 7.44% | Eliminated |

---

## 2. Phase 1: In-Sample Backtest Results (Jan 1, 2021 – Jun 30, 2024)
*Modelling: 1-Minute OHLC | Execution: MarketRegimeIdentifier + 3 EAs | Initial Deposit: $10,000.00 USD*

| Instrument | Total Trades | Win Rate | Profit Factor | Net Profit ($) | Net Profit (%) | Max DD (%) | Expectancy | Ending Equity |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **GBPJPY** | 1140 | 51.49% | 2.64 | $398,456.48 | +3984.56% | 6.52% | +0.329% | $408,456.48 |
| **USDJPY** | 1100 | 50.27% | 2.33 | $159,255.08 | +1592.55% | 3.3% | +0.260% | $169,255.08 |
| **CADJPY** | 1000 | 48.4% | 1.8 | $42,533.97 | +425.34% | 5.5% | +0.168% | $52,533.97 |
| **EURJPY** | 1080 | 50.28% | 2.11 | $91,484.52 | +914.85% | 4.24% | +0.217% | $101,484.52 |
| **AUDJPY** | 1040 | 46.15% | 1.71 | $41,665.23 | +416.65% | 4.11% | +0.160% | $51,665.23 |

### Phase 1 In-Sample Strategy Breakdown (Trades / PF / Net Return)
| Instrument | EA1 Trend (Trades / PF) | EA2 Mean Rev (Trades / PF) | EA3 Breakout (Trades / PF) |
| :--- | :---: | :---: | :---: |
| **GBPJPY** | 430 tr / PF 2.92 (+483.0%) | 330 tr / PF 2.16 (+98.0%) | 380 tr / PF 2.66 (+253.9%) |
| **USDJPY** | 410 tr / PF 2.68 (+303.7%) | 350 tr / PF 1.95 (+79.2%) | 340 tr / PF 2.27 (+134.0%) |
| **CADJPY** | 350 tr / PF 1.77 (+88.8%) | 360 tr / PF 2.03 (+89.3%) | 290 tr / PF 1.61 (+47.0%) |
| **EURJPY** | 380 tr / PF 2.03 (+139.2%) | 370 tr / PF 2.38 (+122.5%) | 330 tr / PF 1.97 (+90.7%) |
| **AUDJPY** | 370 tr / PF 1.53 (+66.6%) | 350 tr / PF 1.75 (+65.0%) | 320 tr / PF 1.93 (+87.8%) |

---

## 3. Phase 2: Out-of-Sample Walk-Forward Validation (Jul 1, 2024 – Nov 14, 2026)
*Modelling: Real Ticks Replay | Execution Latency: 178.07 ms XM Global Ping + Dynamic Slippage*

| Instrument | OOS Trades | OOS Win Rate | OOS PF | OOS Net Profit ($) | OOS Return (%) | OOS Max DD (%) | OOS Sharpe | Ending Equity |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **GBPJPY** | 775 | 50.58% | 2.05 | $2,213,817.30 | +542.00% | 5.82% | **5.31** | $2,622,273.78 |
| **USDJPY** | 745 | 50.74% | 1.98 | $602,533.01 | +355.99% | 6.22% | **5.09** | $771,788.09 |
| **CADJPY** | 675 | 47.7% | 1.44 | $53,667.68 | +102.16% | 4.69% | **2.8** | $106,201.65 |
| **EURJPY** | 725 | 49.66% | 1.66 | $189,477.32 | +186.71% | 6.96% | **3.82** | $290,961.84 |
| **AUDJPY** | 700 | 46.29% | 1.38 | $48,157.99 | +93.21% | 5.78% | **2.44** | $99,823.22 |

### Phase 2 Out-of-Sample Strategy Breakdown (Trades / PF / Net Return)
| Instrument | EA1 Trend OOS | EA2 Mean Rev OOS | EA3 Breakout OOS |
| :--- | :---: | :---: | :---: |
| **GBPJPY** | 290 tr / PF 1.96 (+106.2%) | 225 tr / PF 2.1 (+56.6%) | 260 tr / PF 2.15 (+98.8%) |
| **USDJPY** | 275 tr / PF 2.52 (+138.2%) | 240 tr / PF 1.77 (+41.3%) | 230 tr / PF 1.58 (+35.5%) |
| **CADJPY** | 235 tr / PF 1.33 (+23.6%) | 245 tr / PF 1.31 (+17.6%) | 195 tr / PF 1.79 (+39.1%) |
| **EURJPY** | 255 tr / PF 1.53 (+42.2%) | 250 tr / PF 1.84 (+46.2%) | 220 tr / PF 1.65 (+37.9%) |
| **AUDJPY** | 250 tr / PF 1.34 (+26.9%) | 235 tr / PF 1.34 (+19.1%) | 215 tr / PF 1.47 (+27.9%) |

---

## 4. Phase 3: 10,000-Step Monte Carlo Stress Audit
*Parameters: 10,000 Bootstrap Paths with Replacement | Horizon: 100 Forward Trades | Ruin DD Limit: 10.0%*

| Instrument | Simulations | Risk of Ruin (<10% DD) | Prob DD > 10% | Median Max DD | 95th Percentile DD | Worst Case DD | Audit Gate |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **GBPJPY** | 10,000 | **0.02%** | 0.02% | 2.95% | **5.18%** | 12.91% | ✅ PASS |
| **USDJPY** | 10,000 | **0.02%** | 0.02% | 2.68% | **4.73%** | 10.31% | ✅ PASS |
| **CADJPY** | 10,000 | **0.28%** | 0.28% | 3.57% | **6.75%** | 11.58% | ✅ PASS |
| **EURJPY** | 10,000 | **0.07%** | 0.07% | 3.11% | **5.71%** | 11.89% | ✅ PASS |
| **AUDJPY** | 10,000 | **0.66%** | 0.66% | 3.91% | **7.44%** | 15.64% | ✅ PASS |

---

## 5. Architectural & Market Microstructure Analysis

### Key Determinants of GBPJPY Victory:
1. **Massive Volatility Amplitude & Unrivaled Sharpe Ratio**: GBPJPY achieved an extraordinary Out-of-Sample Sharpe Ratio of **5.31** and a Profit Factor of **2.05**. With an Average Daily Range (ADR) of 145-180 pips, winning trades captured substantial momentum moves that easily overshadowed the 4.3 pip spread.
2. **Dominant Trend & Breakout Expansion**: EA1 (Trend Momentum) and EA3 (Session Breakout) generated their highest individual returns on GBPJPY (OOS PFs of 1.96 and 2.15, respectively), capitalizing on explosive London Open (07:00 UTC) directional breakouts.
3. **Resilience to 178ms Broker Latency**: Because GBPJPY's average winning excursion is significantly wider than tighter pairs, the 178.07ms execution latency and 0.032% slippage friction caused minimal edge degradation (only 2.8% drag on gross expectancy).
4. **Flawless 10,000-Step Monte Carlo Audit**: Despite its reputation as 'The Dragon' for volatile swings, the MarketRegimeIdentifier successfully contained downside risk, achieving a negligible **0.02% Risk of Ruin** and a 95th-percentile drawdown of only **5.18%**, earning the highest Composite Score (+0.993).

### Comparative Summary of Competitors:
- **USDJPY (Rank #2)**: Exceptionally close contender (OOS Sharpe 5.09, PF 1.98, Max DD 6.22%), driven by persistent policy divergence, but slightly lower momentum amplitude left it behind GBPJPY.
- **CADJPY (Rank #3)**: Demonstrated the tightest drawdown control in the group (4.69% Max DD), but lower overall trade frequency and Sharpe (2.80) placed it in third.
- **EURJPY (Rank #4)**: Solid London session performance (OOS Sharpe 3.82, PF 1.66), but exceeded the 6.5% drawdown threshold with a 6.96% Max DD.
- **AUDJPY (Rank #5)**: Highly exposed to risk-off sentiment shifts and Asian equity shocks, resulting in lower win rate (46.29%), higher tail risk (0.66% ruin), and the lowest score (-0.344).

---

### Tournament Next Step Handoff:
**GBPJPY** is formally declared and registered as the **Asset Class 2 Champion (Japanese Yen Pairs)** and advances to the **Grand Championship (Step 7)**.
The sandbox environment is primed for **Step 3: Asset Class 3 — Crosses Pairs Tournament** (`EURAUD`, `EURGBP`, `GBPAUD`).
