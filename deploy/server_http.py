"""HTTP entry point for HF Space deployment.

Imports the same FastMCP instance from src/tafsir/server.py and runs it
over Streamable HTTP. The STDIO server is not modified.

DNS rebinding protection note:
    src/tafsir/server.py constructs FastMCP without explicit host=, so the
    SDK auto-enables DNS rebinding protection limited to localhost. Setting
    mcp.settings.host = "0.0.0.0" later does NOT update transport_security.

    We override mcp.settings.transport_security at runtime (location
    confirmed via SDK introspection). This is safe because:
    - HF proxy terminates TLS and is the real security boundary
    - Content is public Quranic data (no secrets to protect)
    - DNS rebinding targets localhost servers, not public cloud endpoints
"""
import os
import sys

from mcp.server.transport_security import TransportSecuritySettings
from starlette.requests import Request
from starlette.responses import JSONResponse

from tafsir.server import mcp


@mcp.custom_route("/health", methods=["GET"])
async def health(request: Request) -> JSONResponse:
    """Health check for Fly.io / load balancer probes.

    Returns minimal payload with NO secrets — custom_route bypasses MCP auth
    middleware by design (FastMCP documented behavior).
    """
    return JSONResponse({"status": "ok", "service": "tafsir-mcp"})


def main() -> None:
    mcp.settings.host = "0.0.0.0"
    mcp.settings.port = int(os.getenv("PORT", 7860))

    mcp.settings.transport_security = TransportSecuritySettings(
        enable_dns_rebinding_protection=False
    )
    print(
        "[server_http] DNS rebinding protection disabled via "
        "mcp.settings.transport_security",
        file=sys.stderr,
    )

    mcp.run(transport="streamable-http")


if __name__ == "__main__":
    main()