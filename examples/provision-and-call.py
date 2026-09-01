#!/usr/bin/env python3
"""Minimal YG3 agent integration — provision a workspace and call MCP."""

from __future__ import annotations

import json
import sys

try:
    import httpx
except ImportError:
    print("Install httpx: pip install httpx", file=sys.stderr)
    raise SystemExit(1)

PROVISION_URL = "https://agency.yg3.ai/api/v1/workspaces"
MCP_URL = "https://mcp.yg3.ai/mcp"


def provision(domain: str, *, industry: str, location: str) -> dict:
    r = httpx.post(
        PROVISION_URL,
        json={"domain": domain, "industry": industry, "location": location},
        timeout=60,
    )
    r.raise_for_status()
    return r.json()


def mcp_call(token: str, tool: str, arguments: dict | None = None) -> dict:
    r = httpx.post(
        MCP_URL,
        headers={"Authorization": f"Bearer {token}"},
        json={
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {"name": tool, "arguments": arguments or {}},
        },
        timeout=120,
    )
    r.raise_for_status()
    return r.json()


def main() -> None:
    domain = sys.argv[1] if len(sys.argv) > 1 else "example-demo.com"
    industry = sys.argv[2] if len(sys.argv) > 2 else "Demo"
    location = sys.argv[3] if len(sys.argv) > 3 else "Tampa, FL"

    print(f"Provisioning workspace for {domain}…")
    data = provision(domain, industry=industry, location=location)
    token = data["token"]
    print(json.dumps({k: v for k, v in data.items() if k != "token"}, indent=2))
    print(f"\nToken (store securely): {token[:12]}…")
    claim = data.get("claim_endpoint")
    if claim:
        print(f"\nHand this claim URL to a human owner (never /get-started):\n  {claim}")

    print("\nCalling get_client_snapshot…")
    result = mcp_call(token, "get_client_snapshot")
    content = result.get("result", {}).get("content", [])
    if content:
        print(content[0].get("text", "")[:500])
    else:
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
