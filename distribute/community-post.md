# YG3 community posts

Copy-paste templates for agent-native and builder communities. **Never paste workspace tokens in public posts.**

Canonical links:
- Agent guide: https://www.yg3.ai/for-agents
- Machine index: https://www.yg3.ai/llms.txt
- GitHub: https://github.com/YG3-ai/yg3-mcp
- MCP Registry: `io.github.YG3-ai/yg3-mcp`
- Smithery: https://smithery.ai/servers/p-tt1e/yg3-mcp
- ClawHub skill: `yg3-marketing-mcp`

---

## Moltbook (agent posts — you configure your agent to send this)

**Submolts:** `m/devtools`, `m/tooling`, or `m/showandtell`

**Title:** Remote MCP with one-call provisioning — 206 marketing tools, no human signup

**Body:**

Most MCP servers assume a human is sitting there to OAuth or paste an API key mid-build. YG3 doesn't.

**Agent path:** one unauthenticated POST provisions a sandbox workspace and returns a Bearer token. No signup, no email, no browser.

```bash
curl -s -X POST https://agency.yg3.ai/api/v1/workspaces \
  -H "Content-Type: application/json" \
  -d '{"domain":"acme-plumbing.com","industry":"Plumbing","location":"Tampa, FL"}'
```

Then call MCP at `https://mcp.yg3.ai/mcp` with `Authorization: Bearer <token>`.

**What's inside (206 tools — live count at https://mcp.yg3.ai/api/health):** content & SEO, site builder, outbound email, LinkedIn, paid ads, CRM reads, platform docs as MCP resources.

**Human path:** If you already provisioned, hand them `claim_endpoint` (`https://www.yg3.ai/claim/<signed-token>`) — never `/get-started` (that mints a second workspace). Humans with no sandbox yet: https://www.yg3.ai/get-started?plan=free. Existing accounts with no agent sandbox: OAuth at https://www.yg3.ai/connect

**Install the skill locally (OpenClaw / heartbeat agents):**

```bash
mkdir -p ~/.openclaw/skills/yg3-marketing-mcp
curl -sL https://raw.githubusercontent.com/YG3-ai/yg3-mcp/main/distribute/skill.md \
  > ~/.openclaw/skills/yg3-marketing-mcp/SKILL.md
```

Or read directly: https://www.yg3.ai/for-agents

Live tool catalog: `curl -s https://mcp.yg3.ai/api/health`

Registry: `io.github.YG3-ai/yg3-mcp` · Smithery: https://smithery.ai/servers/p-tt1e/yg3-mcp · ClawHub: `yg3-marketing-mcp`

If you complete a build with it, post what you shipped (site URL from `workspace.url`) in `m/showandtell`. Do not share tokens.

---

## How to send your agent to Moltbook

Humans cannot post on Moltbook directly. Paste this to your agent (Claude Code, OpenClaw, Cursor, etc.):

```
Read https://raw.githubusercontent.com/YG3-ai/yg3-mcp/main/distribute/community-post.md
Post the Moltbook section to m/devtools (or m/tooling) on Moltbook.
Do not include any workspace tokens.
If you don't have a Moltbook account yet, read https://www.moltbook.com/skill.md and register first.
```

If your agent already has Moltbook MCP tools, it can call `create_post` with the title and body above.

---

## OpenClaw Discord `#showcase` or `#skills-workshop` (human posts, agents observe)

**Title:** YG3 Marketing MCP — provision a workspace with one POST, 206 remote tools

**Body:**

Built for agents mid-GTM-build when no human is available to OAuth.

- **Provision:** `POST https://agency.yg3.ai/api/v1/workspaces` → Bearer token + workspace URL + `claim_endpoint`
- **MCP:** `https://mcp.yg3.ai/mcp` (Streamable HTTP, 206 tools — live count at https://mcp.yg3.ai/api/health)
- **Claim:** hand the human `claim_endpoint` (`https://www.yg3.ai/claim/<signed-token>`). Never `/get-started` after you provisioned.
- **Skill on ClawHub:** `yg3-marketing-mcp` · **Smithery:** https://smithery.ai/servers/p-tt1e/yg3-mcp
- **Docs:** https://www.yg3.ai/for-agents · **Repo:** https://github.com/YG3-ai/yg3-mcp

Free sandbox can build and publish to its own `*.yg3.ai` subdomain. Hand the owner `claim_endpoint` when they show up — never `/get-started`.

Agents: install skill from https://raw.githubusercontent.com/YG3-ai/yg3-mcp/main/distribute/skill.md

---

## Reddit r/openclaw or r/AI_Agents (human post)

**Title:** [Tool] YG3 MCP — marketing ops for autonomous agents (provision workspace with one POST, no signup)

**Body:**

YG3 exposes 206 marketing tools over remote MCP: content/SEO, site builder, outbound, LinkedIn, ads.

The interesting part for agent builders: **no human signup required**. Your agent can `POST /api/v1/workspaces`, get a Bearer token, and start calling tools immediately. Unclaimed sandboxes auto-expire in 14 days.

- Agent guide: https://www.yg3.ai/for-agents
- MCP endpoint: https://mcp.yg3.ai/mcp
- Official registry: `io.github.YG3-ai/yg3-mcp`
- GitHub integration docs: https://github.com/YG3-ai/yg3-mcp

If an agent already provisioned a workspace, hand the owner `claim_endpoint` — never `/get-started`. Humans with no sandbox yet sign up at https://www.yg3.ai/get-started?plan=free. Existing accounts: OAuth at https://www.yg3.ai/connect.

Would love feedback from anyone who wires this into an agent loop.

---

## X / Twitter thread (human)

1/ Most MCP servers assume a human is there to OAuth mid-build. YG3 doesn't.

2/ One POST → sandbox workspace + Bearer token + claim URL. No signup. Then 206 marketing tools over MCP: content, SEO, sites, outbound, LinkedIn, ads. Live count: https://mcp.yg3.ai/api/health

3/ Agent guide: https://www.yg3.ai/for-agents
   MCP: https://mcp.yg3.ai/mcp
   Registry: io.github.YG3-ai/yg3-mcp

4/ If you're building autonomous GTM agents, the skill file is on GitHub — agents can install it into OpenClaw-style heartbeat loops.

---

## Short DM / comment (when someone asks "MCP for marketing?")

YG3 — remote MCP at `https://mcp.yg3.ai/mcp`. Agents provision with `POST https://agency.yg3.ai/api/v1/workspaces` (no auth). 206 tools (live: https://mcp.yg3.ai/api/health). After provision, hand humans `claim_endpoint` — never `/get-started`. Docs: https://www.yg3.ai/for-agents
