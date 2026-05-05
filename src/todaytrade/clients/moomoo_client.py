
import moomoo as ft
from moomoo import OpenQuoteContext, OpenSecTradeContext, TickerHandlerBase


class MoomooClient:
    """Moomoo OpenD gateway client (default ``127.0.0.1:11111``).

    Call :meth:`connect` before using :attr:`quote` or :attr:`trade`, or use
    ``with MoomooClient(...) as client`` to connect on enter and disconnect on
    exit. If you use :meth:`start_quote`, :meth:`close` / :meth:`disconnect`
    stops async quote reception for you.
    """

    def __init__(self, host: str = "127.0.0.1", port: int = 11111) -> None:
        self.host = host
        self.port = port
        self._quote: OpenQuoteContext | None = None
        self._trade: OpenSecTradeContext | None = None
        self._connected = False
        self._quote_started = False

    def connect(self) -> None:
        """Open TCP sessions to OpenD (quote + HK/sec trade context). Idempotent."""
        if self._connected:
            return
        self._quote = ft.OpenQuoteContext(host=self.host, port=self.port)
        self._trade = ft.OpenSecTradeContext(host=self.host, port=self.port)
        self._connected = True

    def disconnect(self) -> None:
        """Stop quote worker if running, then close quote and trade contexts."""
        self.close()

    @property
    def quote(self) -> OpenQuoteContext:
        self._require_connected()
        assert self._quote is not None
        return self._quote

    @property
    def trade(self) -> OpenSecTradeContext:
        self._require_connected()
        assert self._trade is not None
        return self._trade

    def _require_connected(self) -> None:
        if not self._connected:
            msg = "Not connected to OpenD. Call connect() first."
            raise RuntimeError(msg)

    def start_quote(self, handler: TickerHandlerBase | None = None) -> None:
        """Begin async quote reception; optional ticker handler (default base no-op)."""
        h = handler if handler is not None else ft.TickerHandlerBase()
        self.quote.set_handler(h)
        self.quote.start()
        self._quote_started = True

    def stop_quote(self) -> None:
        if self._quote_started and self._quote is not None:
            self._quote.stop()
            self._quote_started = False

    def close(self) -> None:
        self.stop_quote()
        if self._quote is not None:
            self._quote.close()
            self._quote = None
        if self._trade is not None:
            self._trade.close()
            self._trade = None
        self._connected = False

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()
