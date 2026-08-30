# Where to share YG3 with agents

Prioritized list of communities where **agents** (not just humans browsing MCP directories) might discover and install YG3.

| Priority | Community | Who posts | Best channel | Link |
|---|---|---|---|---|
| **1** | **Moltbook** | Your agent (via API) | `m/devtools`, `m/tooling`, `m/showandtell` | https://www.moltbook.com |
| **2** | **OpenClaw Discord** | You (human) + agents in #showcase | `#showcase`, `#skills-workshop`, `#integrations` | https://discord.com/invite/openclaw |
| **3** | **ClawHub** | Already published | Search `yg3-marketing-mcp` | https://clawhub.ai |
| **4** | **Smithery** | Already published | Server page + gateway URL | https://smithery.ai/servers/p-tt1e/yg3-mcp |
| **5** | **OpenClaw Forum** | Agent (Moltbook-backed) | OpenClaw-tagged submolts | https://openclawforum.org |
| **6** | **Reddit r/openclaw** | You (human) | New post | https://reddit.com/r/openclaw |
| **7** | **Reddit r/AI_Agents** | You (human) | New post | https://reddit.com/r/AI_Agents |
| **8** | **GitHub Discussions** | You | `openclaw/openclaw` → Showcase | https://github.com/openclaw/openclaw/discussions |
| **9** | **Hermes Agent community** | You | Discord / docs forums | https://hermes-agent.nousresearch.com |
| **10** | **MCP directories (forms done)** | N/A — wait for review | PulseMCP, mcpservers.org, mcp.so PR | see repo README |

---

## Agent-only vs human-only

### Agents post directly (best fit)

| Platform | How it works |
|---|---|
| **Moltbook** | Agent registers via https://www.moltbook.com/skill.md → gets API key → posts/comments via REST or Moltbook MCP servers (`moltbook-mcp`, `moltbook-http-mcp`). Humans observe only. |
| **OpenClaw Forum** | Built on Moltbook infrastructure — same agent-posting model. |
| **ClawHub** | Agents install skills via `clawhub install yg3-marketing-mcp` after heartbeat/skill discovery. |

### Humans post, agents discover (still worth it)

| Platform | Why |
|---|---|
| **OpenClaw Discord** | 10k+ builders wiring agents to skills and MCP — `#showcase` is where new integrations get seen. |
| **Reddit r/openclaw, r/AI_Agents** | Builders search here when choosing tool stacks. |
| **X @openclaw** | Tag @openclaw on a short thread; retweets reach agent builders. |

---

## Recommended rollout (do in this order)

### Step 1 — Moltbook (highest leverage for agent discovery)

1. If your agent isn't on Moltbook yet: send it `Read https://www.moltbook.com/skill.md and follow the instructions to join Moltbook`
2. After claim tweet verification, send it the Moltbook block from `community-post.md`
3. Ask it to post to **`m/devtools`** first, then cross-post a build story to **`m/showandtell`** once it actually provisions and ships something

Suggested submolts:
- `m/devtools` — MCP servers, SDKs, integrations
- `m/tooling` — drop-in tools for agents (similar posts to AgentDrop, ContextVault, etc.)
- `m/showandtell` — "here's what I built" (best after a real workspace exists)

### Step 2 — OpenClaw Discord

Join https://discord.com/invite/openclaw → post in **`#showcase`** using the Discord template in `community-post.md`.

Also mention ClawHub skill name so agents can `clawhub search yg3`.

### Step 3 — Reddit

Post to **r/openclaw** (most aligned audience). Cross-post to **r/AI_Agents** if mods allow tool posts.

### Step 4 — Tell your agent to install the skill into its heartbeat

```bash
mkdir -p ~/.openclaw/skills/yg3-marketing-mcp
curl -sL https://raw.githubusercontent.com/YG3-ai/yg3-mcp/main/distribute/skill.md \
  > ~/.openclaw/skills/yg3-marketing-mcp/SKILL.md
curl -sL https://raw.githubusercontent.com/YG3-ai/yg3-mcp/main/distribute/heartbeat.md \
  > ~/.openclaw/skills/yg3-marketing-mcp/HEARTBEAT.md
```

Or point agents at the raw URLs in `skill.json`.

---

## Optional later (lower agent traffic, still good for SEO)

| Channel | Action |
|---|---|
| **Docker MCP Catalog** | PR to https://github.com/docker/mcp-registry (remote URL entry) |
| **E2B / sandbox agents** | E2B sandboxes expose Docker MCP Catalog — Docker listing helps sandbox agents |
| **LangChain / CrewAI Discords** | Post in #tools or #showcase if those servers allow MCP promos |
| **Hacker News** | "Show HN: MCP server agents can provision without signup" — human post, agent builders read it |

---

## What to track

Watch for new `onboarded_via: free:agent` workspaces in prod (non-test domains — not `smithery-scan*`, `zztest-*`, `zze2e-*`).

Signals an agent actually used the provisioning path:
- Real business domain in `cms_url`
- Tool calls: `set_business_profile`, `apply_vertical`, `publish_site_design`, `create_post`
- Optional: human claims via `/api/v1/workspaces/claim`
