# /sc:recommend — MCP server for Notion (--plugin mode)

**Mode:** `--plugin` (local surface ignored). User explicitly asked for an MCP server, so per `refs/plugin-ecosystem-sources.md` the scope opens to MCP servers, clearly labeled as such (not as plugins or skills).

**Search path:** Tavily MCP (shallow, focused). One vendor and one canonical repo were sufficient — no `tech-research` / `deep-research` hand-off needed.

---

## Top picks for "find an MCP server for Notion"

### 1. Notion MCP (hosted, official remote) — pick this if you want zero-infrastructure OAuth setup on Claude Code

- **Type:** MCP server (remote, Streamable HTTP)
- **Name:** Notion MCP — `https://mcp.notion.com/mcp`
- **Capability:** Notion's officially hosted MCP server. AI agents can read and write Notion pages, query databases / data sources, manage comments, and search across the workspace. OAuth-authenticated; tools are optimized for AI agents with efficient (markdown-based) formatting.
- **Install (Claude Code, single-line):**
  ```bash
  claude mcp add --transport http notion https://mcp.notion.com/mcp
  ```
  Then run `/mcp` in Claude Code and complete the OAuth flow.
- **Scope flags (optional):** `--scope local` (default, current project only), `--scope project` (team-shared via `.mcp.json`), `--scope user` (across all projects).
- **Repo / source:** Hosted by Notion; no code repo. Server endpoint: `https://mcp.notion.com/mcp` (SSE fallback: `https://mcp.notion.com/sse`).
- **Version / activity:** Actively maintained as of 2026; Notion's recommended path. (Notion's own docs say to prefer this over the open-source server.)
- **Integration notes:**
  - OAuth flow runs on first tool call — user must be present (no headless / fully-automated use).
  - Tool count and capabilities are managed server-side; client receives them on `initialize`.
  - For richer Notion-specific Claude Code workflows, optionally pair with the `claude-code-notion-plugin` (skills + slash commands bundle over the same MCP).
- **Caveats:**
  - Requires human-in-the-loop OAuth — not suitable for fully automated cloud agents.
  - File / image uploads not yet supported via MCP (workaround: file upload API).
  - Some MCP clients only support local stdio — use the `mcp-remote` bridge in that case (covered in Notion's troubleshooting docs).
- **Citation:**
  - https://developers.notion.com/guides/mcp/get-started-with-mcp
  - https://developers.notion.com/guides/mcp/overview

---

### 2. `@notionhq/notion-mcp-server` (open-source, local STDIO) — pick this if you need headless / token-auth automation

- **Type:** MCP server (local, STDIO; optional Streamable HTTP)
- **Name:** `@notionhq/notion-mcp-server` (a.k.a. `makenotion/notion-mcp-server`)
- **Capability:** Notion's original open-source MCP server. Uses a Notion integration token (`NOTION_TOKEN=ntn_...`) instead of OAuth, which makes it usable in headless / CI / fully-automated contexts where the hosted server's OAuth requirement is blocking. Exposes 22 tools (post v2.0.0 data-source migration, Notion API `2025-09-03`).
- **Install (Claude Code, single-line):**
  ```bash
  claude mcp add --env NOTION_TOKEN=ntn_your_token notion-local -- npx -y @notionhq/notion-mcp-server
  ```
  (Replace `ntn_your_token` with your Notion internal integration secret. Equivalent to the JSON `command: npx, args: [-y, @notionhq/notion-mcp-server], env: { NOTION_TOKEN }` documented in the README.)
- **Repo / source:** https://github.com/makenotion/notion-mcp-server
- **Version / activity:** v2.1.0 released 2026-01-31. **Repository is in maintenance-only mode** — Notion explicitly states they "may sunset this local MCP server repository in the future" and issues / PRs are not actively monitored. Still functional, but not actively developed.
- **Integration notes:**
  - Create an internal integration at `https://www.notion.so/profile/integrations`, then grant page / database access via the integration's Access tab (or per-page "Connect to integration").
  - For finer-grained safety, create a read-only token by limiting Capabilities to "Read content" only.
  - Docker option available (`mcp/notion` on Docker Hub) if you prefer container-isolated execution.
  - v2.0.0 breaking change: database tools (`post-database-query`, `update-a-database`, `create-a-database`) were replaced by data-source equivalents — update any hardcoded tool-name references.
- **Caveats:**
  - Officially de-prioritized by Notion; use only when OAuth-based hosted MCP is not viable.
  - Exposes a Notion integration token to the LLM context — security-conscious users should restrict integration capabilities (read-only, scoped pages).
  - HTTP transport requires bearer-token authentication (auto-generated, CLI-arg, or `AUTH_TOKEN` env var).
- **Citation:**
  - https://github.com/makenotion/notion-mcp-server
  - https://developers.notion.com/guides/mcp/get-started-with-mcp (FAQ: "What's the difference between Notion MCP and the open-source server?")

---

### 3. `mcp-remote` bridge to Notion MCP — pick this if your MCP client only supports local STDIO servers

- **Type:** Bridge package (lets STDIO-only clients talk to the hosted remote MCP)
- **Name:** `mcp-remote` (npm, generic) wrapping `https://mcp.notion.com/mcp`
- **Capability:** A thin STDIO-to-HTTP bridge that lets MCP clients without native remote-server support connect to Notion's hosted MCP. Same OAuth flow, same toolset as option 1, just routed through a local `npx` process.
- **Install (Claude Code, single-line):**
  ```bash
  claude mcp add notion -- npx -y mcp-remote https://mcp.notion.com/mcp
  ```
- **Repo / source:** https://www.npmjs.com/package/mcp-remote (generic bridge — not Notion-specific)
- **Version / activity:** Active npm package; recommended by Notion's own troubleshooting docs as the fallback path.
- **Integration notes:**
  - OAuth flow still runs (browser opens on first call) — the bridge does not change auth model, only transport.
  - Useful if Claude Code's `--transport http` is unavailable in your version, or if you're plumbing into a different MCP client that lacks remote support.
- **Caveats:**
  - Adds a local process hop — slightly higher latency, one more thing that can crash.
  - Same OAuth / human-in-the-loop constraint as option 1.
- **Citation:**
  - https://developers.notion.com/guides/mcp/get-started-with-mcp (troubleshooting section: "My tool doesn't support remote MCP servers")

---

## Quick decision matrix

| Need | Pick |
|---|---|
| Default, lowest friction, OAuth user | **#1 hosted Notion MCP** |
| Headless / CI / automation with API token | **#2 open-source `notion-mcp-server`** |
| MCP client lacks remote HTTP support | **#3 `mcp-remote` bridge** |

## Notes for the user

- All three options are MCP servers, explicitly labeled — none of these are Claude Code plugins or skills. The `claude-code-notion-plugin` exists as a separate bundle (skills + slash commands over the same hosted MCP) — mention it if you want pre-built Notion workflows on top of #1, but it is out of scope for the literal "MCP server" request.
- Citation discipline: every install command and version claim above comes from `developers.notion.com/guides/mcp/get-started-with-mcp` or the `makenotion/notion-mcp-server` README, fetched live via Tavily MCP. No synthesized commands.
