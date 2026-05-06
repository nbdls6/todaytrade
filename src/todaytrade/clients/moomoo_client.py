from typing import Any, Optional, Self
import moomoo as ft  # pyright: ignore[reportMissingImports]
from todaytrade.global_configs import MOOMOO_CLIENT_CONFIG


class MoomooQuoteClient:
    """Thin wrapper around OpenQuoteContext with optional handlers."""

    def __init__(
        self,
        host: Optional[str] = None,
        port: Optional[int] = None,
        handlers: Optional[list[Any]] = None,
    ) -> None:
        host = host or MOOMOO_CLIENT_CONFIG["host"]
        port = port or MOOMOO_CLIENT_CONFIG["port"]
        self.ctx = ft.OpenQuoteContext(host=host, port=port)
        for h in handlers or []:
            self.ctx.set_handler(h)

    def close(self) -> None:
        self.ctx.close()

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()
