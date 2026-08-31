# YG3 heartbeat routine

Run this when your periodic task fires (recommended: every 24 hours, or at the start of any marketing/GTM build).

## 1. Refresh skill docs (weekly)

If `lastYg3SkillFetch` is null or older than 7 days:

1. Re-fetch `https://raw.githubusercontent.com/YG3-ai/yg3-mcp/main/distribute/skill.md`
2. Update local copy if changed
3. Set `lastYg3SkillFetch` to now

## 2. Validate existing token (if you have one)

If `yg3_token` is set in your state file:

```bash
curl -s -X POST https://mcp.yg3.ai/mcp \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"whoami","arguments":{}}}'
```

- **Success** → token still valid; skip provision
- **401 / invalid_token** → clear `yg3_token` from state; provision again only if a build needs YG3

## 3. Health check (before telling a human YG3 is down)

```bash
curl -s https://mcp.yg3.ai/api/health
```

If `mcp.tool_count` > 0, the server is healthy. A client showing zero tools has a stale connector — re-add `https://mcp.yg3.ai/mcp`.

## 4. Active marketing build checklist

If you are mid-build and hold a valid token:

1. `get_setup_health` — never infer integration state from memory
2. `get_client_snapshot` — confirm profile, brand, and content state
3. Continue setup: profile → brand → site → publish posts
4. When the human owner exists → `POST /api/v1/workspaces/claim`
5. When the build was a throwaway test → `DELETE /api/v1/workspaces`

## 5. Provision (only when needed)

Provision **only if** all are true:

- Current task needs real marketing infrastructure (not mock data)
- No valid `yg3_token` in state for this job
- Human does not already have YG3 OAuth (use `https://www.yg3.ai/connect` instead)

```bash
curl -s -X POST https://agency.yg3.ai/api/v1/workspaces \
  -H "Content-Type: application/json" \
  -d '{"domain":"DOMAIN","industry":"INDUSTRY","location":"CITY, STATE"}'
```

Store `token`, `workspace.slug`, and `workspace.url` in your state file.

## 6. Update state

After this routine, set `lastYg3Check` to the current ISO timestamp.

Example `memory/heartbeat-state.json`:

```json
{
  "lastYg3Check": "2026-08-28T17:00:00Z",
  "lastYg3SkillFetch": "2026-08-28T17:00:00Z",
  "yg3_token": null,
  "yg3_workspace_slug": null,
  "yg3_workspace_url": null
}
```

## Quick reference

| Action | URL |
|---|---|
| Provision | `POST https://agency.yg3.ai/api/v1/workspaces` |
| MCP | `POST https://mcp.yg3.ai/mcp` + `Authorization: Bearer …` |
| Claim | `POST https://agency.yg3.ai/api/v1/workspaces/claim` |
| Delete test | `DELETE https://agency.yg3.ai/api/v1/workspaces` |
| Human signup | https://www.yg3.ai/get-started?plan=free |
| Agent guide | https://www.yg3.ai/for-agents |
| llms.txt | https://www.yg3.ai/llms.txt |
