# Notion MCP Server Recommendation

## Top Pick: Notion's Official Hosted MCP Server

**Source:** `https://mcp.notion.com/mcp` (operated by Notion, Inc.)
**Docs:** https://developers.notion.com/guides/mcp/overview
**Help:** https://www.notion.com/help/notion-mcp

### Why this is the recommended pick

Notion ships and maintains a **first-party hosted MCP server**. For nearly every use case (Claude Code, Claude Desktop, Cursor, VS Code Copilot, ChatGPT Pro), this is the right default:

- **Official and actively developed** — built by Notion's own engineering team; their local-binary alternative (`makenotion/notion-mcp-server`) is now soft-deprecated in favor of the hosted endpoint.
- **OAuth, not API tokens** — one-click auth flow tied to your real Notion permissions; no integration token to provision, scope, or rotate manually.
- **Zero install / zero infra** — it's a hosted HTTP MCP endpoint. No Docker image to pull, no Node process to keep alive, no `.env` to manage.
- **18 tools covering search, page read/write, database query, comments, and view management** — sufficient for the overwhelming majority of agentic Notion workflows (PRD drafting, doc search, task updates, release notes).
- **Broad client support out of the box** — Notion publishes copy-paste configs for Claude Code, Cursor, VS Code, ChatGPT.

### Install commands (Claude Code)

```bash
claude mcp add --transport http notion https://mcp.notion.com/mcp
# then in Claude Code:
/mcp   # complete the OAuth flow
```

For a richer experience, install the **Notion plugin for Claude Code**, which bundles the MCP server together with pre-built Skills and slash commands for common Notion workflows (referenced in Notion's official "Connecting to Notion MCP" guide).

### Configuration (Cursor / VS Code / Claude Desktop)

```json
{
  "mcpServers": {
    "notion": {
      "url": "https://mcp.notion.com/mcp"
    }
  }
}
```

(VS Code uses `"servers"` instead of `"mcpServers"` and requires `"type": "http"`.)

---

## Runners-up (only if the hosted server doesn't fit)

| Server | When to use it instead |
| --- | --- |
| **`makenotion/notion-mcp-server`** (official local, MIT) | You need a headless / server-side deployment driven by a long-lived `NOTION_TOKEN` integration token (OAuth user-present flow isn't viable). Soft-deprecated but still functional; Docker Hub image `mcp/notion` available. |
| **StackOne Notion MCP** | You need block-level surgical edits (vs. page-level replace), file-attachment access, headless agent-framework use (LangChain, CrewAI), or data-source management without the Enterprise + Notion AI gate. Third-party commercial. |
| **`suekou/mcp-notion-server`** | You want a community Node server targeting the newer `2026-03-11` Notion API with compact, AI-friendly response shaping and MCP Apps support. |
| **`ccabanillas/notion-mcp`** (Python) | You specifically want a Python implementation to extend / fork. Smaller surface area, MIT-licensed, Smithery-installable. |

---

## Quick decision rubric

- **Default (interactive desktop/IDE agent):** Hosted official → `https://mcp.notion.com/mcp`.
- **Headless backend / CI / automation with an integration token:** `makenotion/notion-mcp-server` (local) or StackOne.
- **Need surgical block edits / file attachments / agent-framework wiring:** StackOne.
- **Want a Python codebase to customize:** `ccabanillas/notion-mcp`.

## Sources

- [Notion MCP — Notion Help Center](https://www.notion.com/help/notion-mcp)
- [Notion MCP Overview — developers.notion.com](https://developers.notion.com/guides/mcp/overview)
- [Connecting to Notion MCP — developers.notion.com](https://developers.notion.com/guides/mcp/get-started-with-mcp)
- [makenotion/notion-mcp-server (Official local server)](https://github.com/makenotion/notion-mcp-server)
- [Notion MCP Server: Capabilities, Limitations, and Alternatives — StackOne](https://www.stackone.com/blog/notion-mcp-deep-dive)
- [suekou/mcp-notion-server](https://github.com/suekou/mcp-notion-server)
- [ccabanillas/notion-mcp](https://github.com/ccabanillas/notion-mcp)
- [Notion's hosted MCP server: an inside look — Notion Blog](https://www.notion.com/blog/notions-hosted-mcp-server-an-inside-look)
