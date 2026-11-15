"""
Antigravity IDE Entrypoint
Autonomous Agentic AI Trading System (Micro Account Edition)
"""
import sys
import os
import argparse

# Ensure line-buffered output for real-time daemon logging
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(line_buffering=True)
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(line_buffering=True)

# Ensure project root is on Python path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from src.agents.orchestrator import Orchestrator

def main():
    parser = argparse.ArgumentParser(description="Autonomous Agentic AI Trading System (Micro Edition) Entrypoint")
    parser.add_argument("--once", action="store_true", help="Run pre-flight healthcheck once and exit")
    parser.add_argument("--cycles", type=int, default=None, help="Run live monitoring for N cycles and exit (default: continuous)")
    parser.add_argument("--interval", type=float, default=3.0, help="Polling interval in seconds (default: 3.0s)")
    args = parser.parse_args()

    print("=" * 70)
    print("Starting Autonomous Agentic AI Trading System (Micro Edition) [Antigravity IDE]")
    print("=" * 70)

    config_path = os.path.join(CURRENT_DIR, "config", "system_config.json")
    orchestrator = Orchestrator(config_path)

    # 1. Pre-flight healthcheck
    health = orchestrator.run_healthcheck()
    print("[Healthcheck]", health)

    if health["status"] != "READY":
        print("[ERROR] MT5 bridge or system initialization failed. Exiting.")
        sys.exit(1)

    print("\nSystem operational.")
    print(f"Edition: {health.get('edition', 'MICRO')} | Minimum Equity: ${health.get('minimum_equity_usd', 100.0):.2f} USD")
    print(f"Monitoring Symbols: {health['target_symbols']}")
    print(f"Loaded EAs: {health['eas']}")
    print(f"Circuit Breakers: Max DD {health['risk_limits']['max_portfolio_dd']}%, Daily Max Loss {health['risk_limits']['daily_loss_limit']}%, Base Risk {health['risk_limits']['base_risk_per_trade']}%\n")

    if args.once:
        return

    # 2. Live Monitoring Mode
    orchestrator.start_live_monitoring(poll_interval=args.interval, max_iterations=args.cycles)

if __name__ == "__main__":
    main()
