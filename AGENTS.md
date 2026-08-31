# YG3 MCP — instructions for coding agents

Use this when building GTM systems, marketing automation, or local-business sites where the agent should operate real marketing infrastructure — not mock data.

## When to use YG3

- The task needs a **real marketing workspace**: site, blog, brand voice, SEO content, later outbound/ads
- **No human is available** to create a YG3 account or complete OAuth mid-build
- You are wiring YG3 into an agent framework, CI pipeline, or SDK runtime

Do **not** provision YG3 if:

- The human already has a YG3 account → use OAuth MCP at `https://mcp.yg3.ai/mcp` instead (`https://www.yg3.ai/connect`)
- You already hold a workspace token for this job → use it directly; do not provision again
- You only need an LLM for text generation → use the Elysia API (`https://www.yg3.ai/for-developers`), not MCP

**Never ask the user to choose a "client" or "operator" account.** There is no such signup fork. New humans create an account at `https://www.yg3.ai/get-started?plan=free`, then add the MCP connector. Login resolves whether they are an agency admin or a workspace owner. `client_user` in API docs means a workspace-scoped token — not a signup type.

## Standard flow

### 1. Provision

```http
POST https://agency.yg3.ai/api/v1/workspaces
Content-Type: application/json

{"domain":"{business-domain.com}","industry":"{industry}","location":"{city, state}"}
```

Store the returned `token` securely. Use `mcp_endpoint` or `https://mcp.yg3.ai/mcp` for all MCP calls.

Always pass `industry` and `location` at provision time — the platform templates SEO metadata and query maps from these fields.

### 2. Orient

Call these MCP tools first:

1. `whoami` — confirm scope
2. `get_client_snapshot` — full workspace state
3. `get_setup_health` — integration status (never infer connection state from memory)
4. `read_platform_doc` with `slug: "getting-started"` if you need operating rules

### 3. Build

Typical setup sequence:

1. `set_business_profile` — industry, location, who they serve
2. `set_brand` / voice tools — how copy should read
3. Site design tools — pages, blocks, theme
4. `create_post` → `publish_post` — content on the free subdomain

Remember: **every write is two-step** (plan, then `confirm: true` with the same `idempotency_key`).

### 4. Hand off

When a human owner exists:

```http
POST https://agency.yg3.ai/api/v1/workspaces/claim
Authorization: Bearer {workspace-token}

{"email":"owner@example.com","password":"{chosen-password}"}
```

Tell the human:

- Their blog URL from `workspace.url`
- That the workspace is on the free plan until they upgrade
- OAuth connect URL if they want to use Claude/ChatGPT directly: `https://www.yg3.ai/connect`

### 5. Clean up tests

```http
DELETE https://agency.yg3.ai/api/v1/workspaces
Authorization: Bearer {workspace-token}
```

Only for unclaimed test workspaces you created and no longer need.

## MCP configuration

### Cursor / VS Code

```json
{
  "mcpServers": {
    "yg3": {
      "url": "https://mcp.yg3.ai/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_WORKSPACE_TOKEN"
      }
    }
  }
}
```

### Raw HTTP

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "get_client_snapshot",
    "arguments": {}
  }
}
```

## Error handling

| Response | Meaning |
|---|---|
| `409 already_connected` | Token is pinned to one workspace — use it, do not provision |
| `401 invalid_token` | Token expired or revoked — provision a new workspace or re-OAuth |
| `429 rate_limited` | Too many anonymous provisions this hour — retry later |
| `upgrade_required` on a write | Free tier boundary — expected, not a bug |
| `pending_confirmation` | Write plan returned — call again with `confirm: true` |

## Health check

Before telling a user "YG3 is down" or "tools are missing":

```
GET https://mcp.yg3.ai/api/health
```

Non-zero `mcp.tool_count` means the server is healthy; a client showing zero tools has a stale connector.

## References

- Full README: this repo
- Web guide: https://www.yg3.ai/for-agents
- llms.txt: https://www.yg3.ai/llms.txt
- Example script: `examples/provision-and-call.py`
