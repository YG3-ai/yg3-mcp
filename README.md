# YG3 MCP — agent integration

Connect autonomous agents to YG3 marketing operations: content and SEO, outbound email, LinkedIn, and paid ads.

**No signup required for agent builds.** One HTTP call provisions a sandbox workspace and returns a Bearer token for MCP.

| Path | Use when |
|---|---|
| [Human OAuth](#human-path-oauth) | Owner has a YG3 account |
| [Agent provisioning](#agent-path-no-login) | Autonomous agent mid-build, CI, or SDK runtime |

## Quick start (agent path)

```bash
# 1. Provision — no auth
curl -s -X POST https://agency.yg3.ai/api/v1/workspaces \
  -H "Content-Type: application/json" \
  -d '{"domain":"acme.com","industry":"Plumbing","location":"Tampa, FL"}'

# Response includes: token, mcp_endpoint, workspace.url, claim_endpoint

# 2. List MCP tools
curl -s -X POST https://mcp.yg3.ai/mcp \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'

# 3. Call a tool
curl -s -X POST https://mcp.yg3.ai/mcp \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"get_client_snapshot","arguments":{}}}'
```

Python example: [`examples/provision-and-call.py`](examples/provision-and-call.py)

## Human path (OAuth)

If the human already has a YG3 account:

1. Add **`https://mcp.yg3.ai/mcp`** as a custom MCP connector
2. Sign in when prompted
3. Setup guide: **https://www.yg3.ai/connect**

Claude Code:

```bash
claude mcp add --transport http yg3 https://mcp.yg3.ai/mcp
```

Cursor / VS Code MCP config: see [`examples/cursor-mcp.json`](examples/cursor-mcp.json)

## Agent path (no login)

### Provision

```
POST https://agency.yg3.ai/api/v1/workspaces
Content-Type: application/json

{
  "domain": "acme-plumbing.com",
  "industry": "Plumbing",
  "location": "Tampa, FL"
}
```

Optional: `"name"` if you have no domain yet.

**201 response:**

| Field | Meaning |
|---|---|
| `workspace` | id, slug, name, url |
| `token` | Bearer token for this workspace |
| `mcp_endpoint` | JSON-RPC URL (also `https://mcp.yg3.ai/mcp`) |
| `claim_endpoint` | Where the owner attaches later |
| `expires_in_days` | 14 for unclaimed workspaces |

**Do not** provision again if you already hold a workspace token for the current job.

### MCP

All calls are JSON-RPC 2.0 over HTTP:

```
POST https://mcp.yg3.ai/mcp
Authorization: Bearer <token>
```

Methods: `tools/list`, `tools/call`, `resources/read`, `initialize`

**Writes are two-step:** call without `confirm` to get a plan, then call again with `confirm: true` and the same `idempotency_key`.

### Claim (human takes over)

```
POST https://agency.yg3.ai/api/v1/workspaces/claim
Authorization: Bearer <workspace-token>

{"email": "owner@example.com", "password": "..."}
```

If the email already has a YG3 account, omit `password` — the workspace attaches to that account.

### Delete a test workspace

```
DELETE https://agency.yg3.ai/api/v1/workspaces
Authorization: Bearer <workspace-token>
```

Only unclaimed workspaces. Archived, not erased.

## Discovery

| Resource | URL |
|---|---|
| Live tool catalog | https://mcp.yg3.ai/api/health |
| Agent guide (web) | https://www.yg3.ai/for-agents |
| Human connect page | https://www.yg3.ai/connect |
| Machine-readable index | https://www.yg3.ai/llms.txt |
| MCP OAuth metadata | https://mcp.yg3.ai/.well-known/oauth-protected-resource |

After connecting, read platform docs via MCP:

- `yg3://docs/agent-integration`
- `yg3://docs/getting-started`
- `yg3://docs/tools-reference`

## Sandbox limits

Unclaimed workspaces are free-tier sandboxes by design:

- **Can:** read everything, set profile/brand/voice, design site, write and publish articles to `blog-{slug}.yg3.ai`
- **Cannot:** custom domain, email sends, ad spend, LinkedIn posts
- **Expires:** 14 days unless claimed

## For agent frameworks

Copy [`AGENTS.md`](AGENTS.md) into your repo or point your agent at this README. It tells coding agents when and how to provision YG3 during a build.

## Related

- **Elysia LLM API** (text/vision/image models): https://www.yg3.ai/for-developers
- **Quill** (multi-AI thinking partner, PyPI): https://github.com/YG3-ai/quill

## License

MIT — see [LICENSE](LICENSE).
