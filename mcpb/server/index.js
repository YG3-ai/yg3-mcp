#!/usr/bin/env node
/**
 * Stdio bridge to the hosted YG3 MCP server via mcp-remote.
 * Bundled for Claude Desktop Extensions (.mcpb) submission only.
 */
const { spawn } = require("child_process");

const url = process.env.YG3_MCP_URL || "https://mcp.yg3.ai/mcp";
const token = (process.env.YG3_TOKEN || "").trim();

const args = ["-y", "mcp-remote@latest", url, "--transport", "http-only"];

if (token) {
  args.push("--header", `Authorization: Bearer ${token}`);
}

const child = spawn("npx", args, {
  stdio: "inherit",
  env: process.env,
  shell: process.platform === "win32",
});

child.on("exit", (code, signal) => {
  if (signal) process.kill(process.pid, signal);
  process.exit(code ?? 1);
});

child.on("error", (err) => {
  console.error("[yg3-mcp] Failed to start mcp-remote:", err.message);
  process.exit(1);
});
