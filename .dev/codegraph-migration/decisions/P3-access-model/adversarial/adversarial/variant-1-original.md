# Option A: MCP-first

Read `context.md` in this folder first.

## Proposal

- Phase 2 adds `"CODEGRAPH_MCP_TOOLS":"explore,node,search,callers,callees,impact,files,status"` to the registration `env` (one line in its JSON), so all eight tools are listed in every session.
- Every primitive calls codegraph through MCP: `mcp__codegraph__codegraph_search`, `_node`, `_callers`, `_callees`, `_impact`, `_files`, `_status`. This is the direct 1:1 replacement of the `mcp__serena__*` names each primitive uses today.
- Read-only agents get the MCP names they need in `tools:` (troubleshoot-analyst, reflect-reviewer: search, node, callers, impact; reuse-auditor: search, node, callers; auggie-reviewer: node, callers, callees). The pinned roster test changes in the same commit.
- CLI only where no MCP tool exists: `codegraph affected --stdin` (test selection) and `codegraph init` (only in a user-typed command). Orchestrators that need `affected` add exactly `Bash(codegraph affected *)`.
- `codegraph_explore` is allowed only for "how does this area work" questions with `maxFiles` set; never a default step.

## Strengths

- Smallest Phase 3 change: each Serena tool name maps to one codegraph tool name in the same place; agents keep their current shape.
- MCP connection keeps the daemon and watcher alive, so the index stays fresh while a session runs (EVAL §4).
- 3-15 ms per call vs about 300 ms CLI; structured parameters (`file`, `line`, `limit`, `symbolsOnly`) are documented (EVAL §3), while several CLI flags are undocumented.
- No Bash needed: read-only agents stay without a shell; no allowlist patterns to get wrong; MCP tools cannot reach mutating verbs.

## Weaknesses

- Depends on a Phase 2 change; without it only explore is listed.
- Always-loaded schemas for 8 tools in every session; overhead unmeasured.
- Background subagents may not get MCP tools (cleanup-audit note); foreground agent behaviour UNVERIFIED.
- Nested-worktree answers come with a warning that must be read from tool output.
