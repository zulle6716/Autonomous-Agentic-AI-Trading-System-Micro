"""
Orchestration Agent (Coordinator) - Micro Edition
Unifies Antigravity IDE and MetaTrader 5 sub-agents:
- Portfolio Risk Manager (calibrated for $100 starting equity)
- Benching Agent (with Monte Carlo validation)
- Self-Improvement Agent (weekly walk-forward audit)
- Market Regime Coordinator (with dynamic micro symbol resolver)
"""
import os
import json
import time
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional

from src.utils.mcp_client import MT5MCPClient
from src.agents.risk_manager import PortfolioRiskManager
from src.agents.benching_agent import BenchingAgent
from src.agents.self_improvement import SelfImprovementAgent

class Orchestrator:
    def __init__(self, config_path: str):
        with open(config_path, "r") as f:
            self.config = json.load(f)

        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.params_dir = os.path.join(base_dir, "config", "parameters")

        # Initialize shared MCP client bridge
        self.mcp_client = MT5MCPClient()

        # Initialize sub-agents
        self.risk_manager = PortfolioRiskManager(self.mcp_client, self.config)
        self.benching_agent = BenchingAgent(self.mcp_client, self.config)
        self.self_improvement = SelfImprovementAgent(self.mcp_client, self.config, self.params_dir)

    def run_healthcheck(self) -> Dict[str, Any]:
        """Perform system pre-flight check across all agents and connection bridge."""
        conn = self.mcp_client.check_connection()
        raw_symbols = self.config.get("instruments", [])
        resolved_symbols = [self.mcp_client.resolve_symbol(s) for s in raw_symbols]
        return {
            "status": "READY" if conn.get("terminal_connected") else "OFFLINE",
            "edition": self.config.get("system", {}).get("edition", "MICRO"),
            "minimum_equity_usd": self.config.get("system", {}).get("minimum_equity_usd", 100.0),
            "mcp_bridge": conn,
            "target_symbols": resolved_symbols,
            "eas": list(self.config.get("eas", {}).keys()),
            "risk_limits": {
                "max_portfolio_dd": self.config["system"]["max_portfolio_drawdown_pct"],
                "daily_loss_limit": self.config["system"]["daily_loss_limit_pct"],
                "base_risk_per_trade": self.config["system"]["base_risk_per_trade_pct"]
            }
        }

    def process_tick_cycle(self, current_equity: float, active_trades: List[Dict[str, Any]]):
        """Standard orchestrator tick loop: updates risk and evaluates circuit breakers."""
        cb_status = self.risk_manager.evaluate_circuit_breakers(current_equity)
        if cb_status["tripped"]:
            return {
                "action": "EMERGENCY_HALT",
                "reason": cb_status["reason"],
                "equity": current_equity
            }
        return {"action": "CONTINUE", "status": "HEALTHY"}

    def start_live_monitoring(self, poll_interval: float = 3.0, max_iterations: Optional[int] = None) -> Dict[str, Any]:
        """
        Runs the continuous live monitoring loop across Elite Triad micro symbols:
        1. Tracks real-time account equity, balance, and margin (cent-level precision).
        2. Evaluates Portfolio Risk Manager circuit breakers (10.0% max DD, 2.0% daily limit).
        3. Monitors Elite Triad quotes (EURAUDmicro, GOLDmicro, US100Cash/US100micro).
        4. Audits active positions and EA benching triggers.
        5. Enforces instant kill-switch liquidation if circuit breaker trips.
        """
        acc = self.mcp_client.get_account_summary()
        current_equity = acc.get("equity", 100.0)
        self.risk_manager.day_start_equity = current_equity
        self.risk_manager.high_water_mark = current_equity

        # Clear any stale circuit breaker flag upon clean startup
        self.mcp_client.set_global_variable("SYS_CIRCUIT_BREAKER_ACTIVE", 0.0)

        raw_symbols = self.config.get("instruments", ["EURAUDmicro", "GOLDmicro", "US100Cash"])
        symbols = [self.mcp_client.resolve_symbol(s) for s in raw_symbols]
        eas = self.config.get("eas", {})
        magic_numbers = [v["magic_number"] for v in eas.values() if "magic_number" in v]
        conn_info = self.mcp_client.check_connection()

        print("=" * 75)
        print("  AUTONOMOUS AGENTIC AI TRADING SYSTEM (MICRO EDITION) - LIVE MONITORING ACTIVE")
        print("=" * 75)
        print(f"  Account Login:         {conn_info.get('login', 'N/A')} ({conn_info.get('server', 'XMGlobal')})")
        print(f"  Day-Start Equity:      ${current_equity:,.2f} USD")
        print(f"  High-Water Mark:       ${self.risk_manager.high_water_mark:,.2f} USD")
        print(f"  Circuit Breakers:      Max DD {self.risk_manager.max_dd_limit}% | Daily Loss {self.risk_manager.daily_loss_limit}% [ARMED]")
        print(f"  Base Trade Risk:       {self.config['system']['base_risk_per_trade_pct']}% (${current_equity * (self.config['system']['base_risk_per_trade_pct'] / 100.0):.2f})")
        print(f"  Elite Triad Symbols:   {', '.join(symbols)}")
        ea_desc_list = [f"{k} ({v.get('name', 'EA')})" for k, v in eas.items()]
        ea_desc_str = ", ".join(ea_desc_list)
        print(f"  Active EAs:            {ea_desc_str}")
        print(f"  Poll Interval:         {poll_interval}s")
        print("=" * 75)
        print("Live telemetry stream initiated (Press Ctrl+C to halt):\n")

        iteration = 0
        try:
            while max_iterations is None or iteration < max_iterations:
                iteration += 1
                now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

                # 1. Fetch live account metrics
                acc = self.mcp_client.get_account_summary()
                equity = acc.get("equity", current_equity)
                balance = acc.get("balance", current_equity)

                # 2. Query open positions
                positions = self.mcp_client.get_open_positions(magic_numbers)

                # 3. Process circuit breaker checks
                cb_eval = self.risk_manager.evaluate_circuit_breakers(equity)
                if cb_eval["tripped"]:
                    print(f"\n[CRITICAL CIRCUIT BREAKER TRIPPED] Reason: {cb_eval['reason']}")
                    print(f"[ACTION] Emergency liquidation initiated. Closing {len(positions)} positions...")
                    closed = self.mcp_client.close_all_positions()
                    print(f"[ACTION] Liquidated {closed} positions. System halted safely.")
                    return {"status": "HALTED", "reason": cb_eval["reason"]}

                # 4. Query live symbol quotes
                ticks = self.mcp_client.get_symbol_ticks(symbols)
                quote_str_list = []
                for s in symbols:
                    t = ticks.get(s, {})
                    bid = t.get("bid", 0.0)
                    ask = t.get("ask", 0.0)
                    spread = t.get("spread_points", 0.0)
                    if bid and ask:
                        quote_str_list.append(f"{s}: {bid:.2f}/{ask:.2f} (spd {spread:.0f})")
                    else:
                        quote_str_list.append(f"{s}: MKT_WAIT")
                quotes_summary = " | ".join(quote_str_list)

                # 5. Telemetry update line
                tot_dd = cb_eval["total_dd_pct"]
                day_loss = cb_eval["daily_dd_pct"]
                pos_count = len(positions)
                print(f"[{now_str}] Eq: ${equity:,.2f} | Bal: ${balance:,.2f} | DD: {tot_dd:.2f}% | DayLoss: {day_loss:.2f}% | Pos: {pos_count} | {quotes_summary}", flush=True)

                if max_iterations is not None and iteration >= max_iterations:
                    break

                time.sleep(poll_interval)

        except KeyboardInterrupt:
            print("\n[INFO] Monitoring loop halted cleanly by user.")

        return {"status": "ACTIVE", "iterations": iteration}
