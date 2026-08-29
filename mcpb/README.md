# YG3 MCPB bundle (form submission)

This folder builds a **Claude Desktop Extensions** `.mcpb` file for directory forms that require a file upload.

YG3’s real MCP server is **remote** at `https://mcp.yg3.ai/mcp`. The bundle is a thin stdio bridge (`mcp-remote`) — not a second server implementation.

## Build

```bash
cd mcpb
npx @anthropic-ai/mcpb pack . ../dist/yg3-marketing-mcp.mcpb
```

Output: **`../dist/yg3-marketing-mcp.mcpb`**

## Upload this file

```
Winning/yg3-mcp/dist/yg3-marketing-mcp.mcpb
```

Or from GitHub after push: download from the repo’s `dist/` folder.

## User config in the bundle

- **Workspace token (optional):** Bearer from `POST https://agency.yg3.ai/api/v1/workspaces`
- **Leave blank:** OAuth via `https://www.yg3.ai/connect`
