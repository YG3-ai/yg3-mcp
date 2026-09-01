# YG3 MCP — agent integration

Connect autonomous agents to YG3 marketing operations: content and SEO, outbound email, LinkedIn, and paid ads.

**No signup required for agent builds.** One HTTP call provisions a sandbox workspace and returns a Bearer token for MCP.

| Path | Use when |
|---|---|
| [Human OAuth](#human-path-oauth) | Owner already has a YG3 account, or was never provisioned by an agent |
| [Agent provisioning](#agent-path-no-login) | Autonomous agent mid-build; hand `claim_endpoint` when a human is ready |

## Quick start (agent path)

```bash
# 1. Provision — no auth
curl -s -X POST https://agency.yg3.ai/api/v1/workspaces \
  -H "Content-Type: application/json" \
  -d '{"domain":"acme.com","industry":"Plumbing","location":"Tampa, FL"}'

# Response includes: token, mcp_endpoint, workspace.url, claim_endpoint, claim_api
# Hand claim_endpoint (https://www.yg3.ai/claim/<signed-token>) to a human — never /get-started

# 2. List MCP tools
curl -s -X POST https://mcp.yg3.ai/mcp \
  -H "Authorization: Bearer $YG3_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'

# 3. Call a tool
curl -s -X POST https://mcp.yg3.ai/mcp \
  -H "Authorization: Bearer $YG3_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"get_client_snapshot","arguments":{}}}'
```

Python example: [`examples/provision-and-call.py`](examples/provision-and-call.py)

## Tools

**206** MCP tools (live count: https://mcp.yg3.ai/api/health). Common entry points:

| Tool | Purpose |
|---|---|
| `whoami` | Confirm token scope |
| `get_client_snapshot` | Full workspace state |
| `get_setup_health` | Integration status |
| `set_business_profile` | Industry, location, audience |
| `set_brand` | Brand voice and positioning |
| `create_post` / `publish_post` | Blog content on free subdomain |
| `read_platform_doc` | In-MCP docs (`getting-started`, `agent-integration`, `tools-reference`) |

Full catalog after connecting: `tools/list` or `GET https://mcp.yg3.ai/api/health`.

## Human path (OAuth)

**There is no "client vs operator" signup choice.** Humans enter email once; the platform resolves their role automatically.

Pick the path that matches whether an agent already provisioned a workspace:

| Situation | What to do |
|---|---|
| An agent already provisioned this workspace | Hand them **`claim_endpoint`** (`https://www.yg3.ai/claim/<signed-token>`). **Never `/get-started`** — that mints a second workspace. |
| Never provisioned by an agent; human needs an account | **https://www.yg3.ai/get-started?plan=free** |
| Human already has a YG3 account (no agent sandbox) | Add the MCP connector below |

After they have an account (claimed or signed up on their own):

1. Add **`https://mcp.yg3.ai/mcp`** as a custom MCP connector
2. Sign in when prompted
3. Setup guide (per AI client, including Grok): **https://www.yg3.ai/connect**

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
| `claim_endpoint` | Browser URL `https://www.yg3.ai/claim/<signed-token>` bound to **this** workspace. Hand this to a human. Expires with the 14-day unclaimed sandbox. |
| `claim_api` | Machine path: Bearer `POST /api/v1/workspaces/claim`. The thing you give a human is `claim_endpoint`, not this. |
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

**Give the human `claim_endpoint`.** That is a browser page at `https://www.yg3.ai/claim/<signed-token>`, bound to this workspace, and it expires with the 14-day unclaimed sandbox.

On that page they enter email:

- Existing YG3 account → this workspace attaches (no second client)
- New email → account is created on **this** workspace (magic-link sign-in)
- After success: the sandbox is theirs, still Free, with the blog URL from `workspace.url`. Then they connect MCP at https://www.yg3.ai/connect
- Claiming does **not** change the plan

**Never send them to `/get-started` after you provisioned.** That form mints a different workspace; this sandbox still expires.

Machine/API path (`claim_api`) still exists for agents that claim on the human's behalf:

```
POST https://agency.yg3.ai/api/v1/workspaces/claim
Authorization: Bearer <workspace-token>

{"email": "owner@example.com", "password": "..."}
```

If the email already has a YG3 account, omit `password`.

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
| Human signup (no agent sandbox) | https://www.yg3.ai/get-started?plan=free |
| Machine-readable index | https://www.yg3.ai/llms.txt |
| Skill (raw) | https://raw.githubusercontent.com/YG3-ai/yg3-mcp/main/distribute/skill.md |
| Heartbeat (raw) | https://raw.githubusercontent.com/YG3-ai/yg3-mcp/main/distribute/heartbeat.md |
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

### ClawHub (OpenClaw)

Publishable skill: [`skills/yg3-marketing-mcp/SKILL.md`](skills/yg3-marketing-mcp/SKILL.md)

```bash
clawhub login
clawhub skill publish ./skills/yg3-marketing-mcp --slug yg3-marketing-mcp --name "YG3 Marketing MCP"
```

### Moltbook / curl-based agents

Curlable skill files (Moltbook-style): [`distribute/`](distribute/)

- Install doc: `distribute/skill.md`
- Periodic routine: `distribute/heartbeat.md`
- Metadata: `distribute/skill.json`

Agents can fetch from raw GitHub:

- https://raw.githubusercontent.com/YG3-ai/yg3-mcp/main/distribute/skill.md
- https://raw.githubusercontent.com/YG3-ai/yg3-mcp/main/distribute/heartbeat.md

Or from `https://www.yg3.ai/llms.txt`.

## Registry listings

| File | Purpose |
|---|---|
| [`server.json`](server.json) | Official MCP Registry (`mcp-publisher publish`) |
| [`glama.json`](glama.json) | Glama directory indexing |

Registry namespace: `io.github.YG3-ai/yg3-mcp`

## Related

- **Elysia LLM API** (text/vision/image models): https://www.yg3.ai/for-developers
- **Quill** (multi-AI thinking partner, PyPI): https://github.com/YG3-ai/quill

## License

MIT — see [LICENSE](LICENSE).
