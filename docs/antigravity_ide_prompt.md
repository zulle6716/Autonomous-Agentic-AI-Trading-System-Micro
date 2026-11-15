# Universal Antigravity IDE Deployment & Execution Prompts

This guide provides both the **Initial Deployment Pipeline Prompt** and the **Daily Live Execution Prompt** for the Autonomous Agentic AI Trading System in Antigravity IDE.

---

## 1. Initial 4-Step Deployment Pipeline Prompt

Use this prompt when setting up or cloning the workspace for the first time:

```text
/plan /goal
You are the Orchestration Agent for the Autonomous Agentic AI Trading System.
My workspace folder is located at:
"<PATH_TO_YOUR_WORKSPACE_FOLDER>" (e.g. C:\Users\zulle\My Drive\FOREX\Autonomous Agentic AI Trading System)

My MetaTrader 5 terminal is installed at:
"<PATH_TO_YOUR_MT5_TERMINAL64.EXE>" (e.g. C:\Program Files\XM Global MT5 1\terminal64.exe)

Execute the following automated 4-step deployment pipeline:

1. MT5 MCP INITIALIZATION & LATENCY DETECTION:
   - Connect to my MT5 terminal via MCP (mcp-mt5 / metatrader5).
   - Ping the broker server 5 times and calculate the exact mean execution latency.
   - Verify tick data, digits, lot step, and trade permissions for the 3 active instruments:
     * US100Cash (Nasdaq 100)
     * GOLD (XAUUSD)
     * EURAUD (Currency Cross)

2. COMPILATION & BINARY DEPLOYMENT:
   - Compile all 4 MQL5 files in src/mql5/ using metaeditor64.exe:
     * src/mql5/Indicators/MarketRegimeIdentifier.mq5
     * src/mql5/Experts/EA1_Trend_Momentum.mq5
     * src/mql5/Experts/EA2_Mean_Reversion.mq5
     * src/mql5/Experts/EA3_Session_Breakout.mq5
   - Verify 0 compilation errors and ensure the compiled .ex5 binaries and TradeBridge.mqh are deployed to my MT5 terminal's MQL5 folder.

3. ENVIRONMENT & CIRCUIT BREAKER VERIFICATION:
   - Run the Python unit test suite: python -m unittest discover -s tests
   - Verify all 7 tests pass (Monte Carlo engine, Portfolio Risk Manager, Circuit Breakers, Benching Agent).
   - Confirm active risk limits: 10.0% max portfolio drawdown ceiling, 2.0% daily loss limit, 0.4% base risk per trade.

4. SYSTEM STARTUP:
   - Execute python main.py to start the system runtime healthcheck.
   - Confirm healthcheck returns status 'READY' and begins monitoring US100Cash, GOLD, and EURAUD.
   - Report final deployment confirmation and operational status.
```

---

## 2. Daily Live Execution Prompt (Method B)

Once the system has been deployed, use this prompt in Antigravity IDE chat to start live monitoring:

```text
/plan /goal
Initialize and run the Autonomous Agentic AI Trading System via main.py in live monitoring mode across US100Cash, GOLD, and EURAUD with Portfolio Risk Manager circuit breakers armed.
```
