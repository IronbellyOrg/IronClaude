# Active command literal inventory

**Scan date:** 2026-09-11
**Scope:** `src/superclaude`, `docs`, and focused `tests`; no `.claude`, plugin, user/machine config, hook, or eval namespace migration.

| Surface | Literal | Classification | Disposition |
|---|---|---|---|
| `src/superclaude/cli/install_mcp.py` | all selected old/floating commands | required update | Phase 3.1 |
| `.mcp.json` | third-party `npx -y auggie-mcp` | preserve namespace | Phase 3.2 changes command only; retains key |
| `tests/cli/test_install_mcp_tavily.py` | Tavily `0.2.20` expectations | required update | Phase 4.1 |
| `tests/docs/test_tavily_doc_alignment.py` | allowed pin `0.2.20` | required update | Phase 4.1 |
| `docs/user-guide/mcp-installation.md` | catalog/selector facts | required update if changed literal found | Phase 4.3 |
| `docs/user-guide/mcp-servers.md` | Tavily old pin, Serena Git command, Morph deprecated package, unpinned Sequential | required update | Phase 4.3 |
| `docs/troubleshooting/serena-installation.md` | Serena Git launcher/context | required update | Phase 4.3 |
| `docs/reference/mcp-server-guide.md` | Serena Git launcher/context | required update | Phase 4.3, command-only |
| `src/superclaude/mcp/MCP_Tavily.md` | Tavily `0.2.20` | required update | Phase 4.3 |
| `src/superclaude/mcp/MCP_Auggie.md` | `@latest` global instruction | required update | Phase 4.3 |
| `src/superclaude/mcp/configs/{sequential,serena,morphllm}.json` | old or floating template commands | explicit exclusion | Package/template consolidation deferred by R-004 |
| `src/superclaude/cli/eval/suites/real.yaml` | explanatory Tavily old pin | required update | Phase 4.3 text-only, no eval behavior change |
| `src/superclaude/hooks/**`, `src/superclaude/cli/eval/**` uses of `auggie-mcp` | stable namespace | preserve namespace | no change |

**Negative results:** No required code change was found for excluded Context7, Playwright, Chrome DevTools, Magic, AIRIS, Markdown Collab, or user-level Codebase Memory.
