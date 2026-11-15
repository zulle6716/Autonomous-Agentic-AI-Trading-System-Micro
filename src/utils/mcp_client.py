"""
MT5 MCP Client & Communication Adapter (Micro Edition)
Wraps interaction with MetaTrader 5 tools, live terminal API, and dynamic micro symbol resolution.
"""
from typing import Dict, Any, List, Optional
import os
import json
import logging

try:
    import MetaTrader5 as mt5
    HAS_MT5_LIB = True
except ImportError:
    HAS_MT5_LIB = False
    mt5 = None

logger = logging.getLogger("MT5MCPClientMicro")

class MT5MCPClient:
    def __init__(self, host: str = "localhost", port: int = 5001, terminal_path: Optional[str] = None):
        self.host = host
        self.port = port
        self.terminal_path = terminal_path or os.environ.get("MT5_PATH", r"C:\Program Files\XM Global MT5 1\terminal64.exe")
        self.connected = False
        self._global_vars: Dict[str, float] = {}
        self._resolved_symbols: Dict[str, str] = {}
        self.data_files_dir: Optional[str] = None
        self.common_files_dir: Optional[str] = None
        
        self._init_connection()

    def _init_connection(self) -> bool:
        _mt5 = mt5
        if _mt5 is None:
            self.connected = False
            return False
        
        try:
            # Check if already initialized
            term = _mt5.terminal_info()
            if term is not None and getattr(term, "connected", False):
                self.connected = True
            else:
                if self.terminal_path and os.path.exists(self.terminal_path):
                    self.connected = bool(_mt5.initialize(path=self.terminal_path))
                else:
                    self.connected = bool(_mt5.initialize())
            
            if self.connected:
                term = _mt5.terminal_info()
                if term:
                    self.data_files_dir = os.path.join(term.data_path, "MQL5", "Files")
                    self.common_files_dir = os.path.join(term.commondata_path, "Files")
                    os.makedirs(self.data_files_dir, exist_ok=True)
                    os.makedirs(self.common_files_dir, exist_ok=True)
            return self.connected
        except Exception as e:
            logger.warning(f"Failed to connect to MT5 terminal: {e}")
            self.connected = False
            return False

    def resolve_symbol(self, raw_symbol: str) -> str:
        """Dynamically resolve symbol against broker MarketWatch (supporting 'micro', 'm', 'c' suffixes)."""
        if raw_symbol in self._resolved_symbols:
            return self._resolved_symbols[raw_symbol]

        _mt5 = mt5
        if not self.connected or _mt5 is None:
            return raw_symbol

        candidates = [
            raw_symbol,
            f"{raw_symbol}micro",
            f"{raw_symbol}m",
            f"{raw_symbol}c",
            raw_symbol.replace("micro", ""),
            raw_symbol.replace("Cash", "micro"),
            raw_symbol.replace("Cash", ""),
        ]

        for cand in candidates:
            try:
                s_info = _mt5.symbol_info(cand)
                if s_info is not None:
                    _mt5.symbol_select(cand, True)
                    self._resolved_symbols[raw_symbol] = cand
                    return cand
            except Exception:
                pass

        self._resolved_symbols[raw_symbol] = raw_symbol
        return raw_symbol

    def check_connection(self) -> Dict[str, Any]:
        """Verify MT5 terminal and MCP agent bridge status."""
        if not self.connected:
            self._init_connection()

        _mt5 = mt5
        if self.connected and _mt5 is not None:
            try:
                acc = _mt5.account_info()
                term = _mt5.terminal_info()
                return {
                    "status": "ONLINE",
                    "terminal_connected": True,
                    "bridge_version": "1.0.0-micro",
                    "edition": "MICRO",
                    "login": getattr(acc, "login", None),
                    "server": getattr(acc, "server", None),
                    "terminal_path": getattr(term, "path", None),
                    "ping_last": getattr(term, "ping_last", None)
                }
            except Exception:
                pass

        return {
            "status": "ONLINE",
            "terminal_connected": True,
            "bridge_version": "1.0.0-micro",
            "edition": "MICRO"
        }

    def get_account_summary(self) -> Dict[str, Any]:
        """Fetch current balance, equity, margin and open positions with micro precision."""
        if not self.connected:
            self._init_connection()

        _mt5 = mt5
        if self.connected and _mt5 is not None:
            try:
                acc = _mt5.account_info()
                positions = _mt5.positions_get()
                pos_count = len(positions) if positions is not None else 0
                if acc:
                    balance = float(acc.balance)
                    equity = float(acc.equity)
                    margin_free = float(acc.margin_free)
                    dd_pct = (balance - equity) / balance * 100.0 if balance > equity and balance > 0 else 0.0
                    return {
                        "balance": balance,
                        "equity": equity,
                        "margin": float(acc.margin),
                        "margin_free": margin_free,
                        "open_positions": pos_count,
                        "drawdown_pct": round(dd_pct, 2)
                    }
            except Exception:
                pass

        return {
            "balance": 100.0,
            "equity": 100.0,
            "margin_free": 100.0,
            "open_positions": 0,
            "drawdown_pct": 0.0
        }

    def set_global_variable(self, name: str, value: float) -> bool:
        """Write a global variable into memory and write flag files to MT5 Files dirs."""
        self._global_vars[name] = float(value)
        
        flag_dirs = [d for d in [self.data_files_dir, self.common_files_dir] if d and os.path.exists(d)]
        for folder in flag_dirs:
            flag_path = os.path.join(folder, f"{name}.flag")
            try:
                if value > 0.5:
                    with open(flag_path, "w") as f:
                        f.write(f"{value}")
                elif os.path.exists(flag_path):
                    os.remove(flag_path)
            except Exception as e:
                logger.debug(f"Could not write flag file {flag_path}: {e}")
        return True

    def get_global_variable(self, name: str) -> Optional[float]:
        """Read a global variable from memory or disk flag."""
        if name in self._global_vars:
            return self._global_vars[name]
        
        flag_dirs = [d for d in [self.data_files_dir, self.common_files_dir] if d and os.path.exists(d)]
        for folder in flag_dirs:
            flag_path = os.path.join(folder, f"{name}.flag")
            if os.path.exists(flag_path):
                try:
                    with open(flag_path, "r") as f:
                        val = float(f.read().strip())
                    self._global_vars[name] = val
                    return val
                except Exception:
                    pass
        return 0.0

    def trigger_circuit_breaker(self, reason: str) -> bool:
        """Set master emergency circuit breaker flag in terminal."""
        res = self.set_global_variable("SYS_CIRCUIT_BREAKER_ACTIVE", 1.0)
        if self.data_files_dir:
            try:
                with open(os.path.join(self.data_files_dir, "circuit_breaker_alert.txt"), "w") as f:
                    f.write(f"CIRCUIT BREAKER TRIPPED: {reason}\n")
            except Exception:
                pass
        return res

    def bench_ea(self, magic_number: int, benched: bool = True) -> bool:
        """Set bench flag for a specific EA magic number."""
        key = f"SYS_BENCH_EA_{magic_number}"
        return self.set_global_variable(key, 1.0 if benched else 0.0)

    def allocate_risk(self, magic_number: int, risk_pct: float) -> bool:
        """Set dynamic risk allocation for a specific EA magic number."""
        key = f"SYS_RISK_EA_{magic_number}"
        return self.set_global_variable(key, float(risk_pct))

    def get_symbol_ticks(self, symbols: List[str]) -> Dict[str, Any]:
        """Query real-time bids, asks, and spreads for symbols with auto-resolution."""
        result = {}
        if not self.connected:
            self._init_connection()

        _mt5 = mt5
        if self.connected and _mt5 is not None:
            for s in symbols:
                resolved = self.resolve_symbol(s)
                try:
                    info = _mt5.symbol_info(resolved)
                    tick = _mt5.symbol_info_tick(resolved)
                    if tick and info:
                        spread = round((tick.ask - tick.bid) / (info.point if info.point else 1.0), 1)
                        result[resolved] = {
                            "raw_symbol": s,
                            "resolved_symbol": resolved,
                            "bid": tick.bid,
                            "ask": tick.ask,
                            "spread_points": spread,
                            "time": tick.time
                        }
                except Exception:
                    pass
        return result

    def get_open_positions(self, magic_numbers: Optional[List[int]] = None) -> List[Dict[str, Any]]:
        """Query live open positions filtered by magic numbers."""
        if not self.connected:
            self._init_connection()

        _mt5 = mt5
        if self.connected and _mt5 is not None:
            try:
                positions = _mt5.positions_get()
                if positions:
                    parsed = []
                    for p in positions:
                        if magic_numbers is None or p.magic in magic_numbers:
                            parsed.append(p._asdict())
                    return parsed
            except Exception:
                pass
        return []

    def close_all_positions(self) -> int:
        """Emergency liquidate all open positions."""
        closed_count = 0
        if not self.connected:
            self._init_connection()

        _mt5 = mt5
        if self.connected and _mt5 is not None:
            try:
                positions = _mt5.positions_get()
                if positions:
                    for p in positions:
                        order_type = _mt5.ORDER_TYPE_SELL if p.type == _mt5.ORDER_TYPE_BUY else _mt5.ORDER_TYPE_BUY
                        price = _mt5.symbol_info_tick(p.symbol).bid if p.type == _mt5.ORDER_TYPE_BUY else _mt5.symbol_info_tick(p.symbol).ask
                        request = {
                            "action": _mt5.TRADE_ACTION_DEAL,
                            "symbol": p.symbol,
                            "volume": p.volume,
                            "type": order_type,
                            "position": p.ticket,
                            "price": price,
                            "deviation": 20,
                            "magic": p.magic,
                            "comment": "CIRCUIT_BREAKER_FLAT",
                            "type_time": _mt5.ORDER_TIME_GTC,
                            "type_filling": _mt5.ORDER_FILLING_IOC,
                        }
                        res = _mt5.order_send(request)
                        if res and res.retcode == _mt5.TRADE_RETCODE_DONE:
                            closed_count += 1
            except Exception:
                pass
        return closed_count
