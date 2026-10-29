# Decision context: how IronClaude primitives reach codegraph (task P3, issue #323)

Question: after Serena is removed (Phase 1) and codegraph is installed and registered (Phase 2), through which access path do skills, commands and agents call codegraph?

## Facts (ground truth: `.dev/codegraph-migration/research/codegraph-evaluation.md`, cited EVAL §n)

- 8 MCP tools, all read-only: `codegraph_explore`, `_search`, `_callers`, `_callees`, `_impact`, `_node`, `_files`, `_status` (EVAL §3). Claude Code names them `mcp__codegraph__codegraph_<x>`.
- Only `codegraph_explore` is LISTED by default (`DEFAULT_MCP_TOOLS = new Set(['explore'])`). Others still answer a raw `tools/call`, but Claude Code offers the model listed tools only. `CODEGRAPH_MCP_TOOLS=explore,node,search,callers,callees,impact,files,status` in the server env lists all; an explicit list blocks any tool not named (EVAL §3).
- Phase 2's planned registration: `claude mcp add-json codegraph '{"type":"stdio","command":"<abs>","args":["serve","--mcp"],"alwaysLoad":true,"env":{"CODEGRAPH_TELEMETRY":"0","CODEGRAPH_NO_UPDATE_CHECK":"1"}}' --scope user` (EVAL §7 step 5). It does not set `CODEGRAPH_MCP_TOOLS`. Adding it is a one-line change in Phase 2's JSON.
- MCP latency 3-15 ms per call after a 220 ms init; CLI about 290-300 ms per call (EVAL §5.5, §5.6).
- A connected MCP client starts a per-project daemon with a file watcher (2000 ms debounce) that keeps the index fresh; CLI-only sessions have no watcher; CLI `codegraph status` freshness without a daemon was never measured (EVAL §4, §5.7; brainstorm INV-001).
- CLI has mutating verbs next to read verbs: `init`, `index`, `sync`, `uninit`, `install`, `uninstall`, `upgrade`, `unlock`, `telemetry on|off` (EVAL §3). A broad `Bash(codegraph *)` allowlist would pre-approve `install`, which edits Claude config (EVAL §2).
- `affected` (changed files → test files) and `init` are CLI only (EVAL §3, §6.1).
- `codegraph_explore` returned 24,913 characters in one sample and pulled unrelated symbols (EVAL §5.6).
- Subagents do not see the MCP server's instructions (EVAL §3). Restricted read-only agents (troubleshoot-analyst, reflect-reviewer, reuse-auditor) have no Bash; today they list `mcp__serena__*` tools in `tools:` (`.dev/codegraph-migration/inventory/primitive-usage.md` §6). `tests/troubleshoot/test_diagnostic_worker_contract.py:17-26` pins the troubleshoot-analyst roster exactly.
- `src/superclaude/skills/sc-cleanup-audit-protocol/SKILL.md:86`: "MCP tools are unavailable to background subagents". Whether foreground agents with MCP names in `tools:` can call them is not measured here (UNVERIFIED either way).
- Closed-Bash orchestrators exist: pr-submit (`Bash(gh *) git uv make jq`), auggie-review, cleanup-audit (brainstorm §2.1).
- The brainstorm (`.dev/codegraph-migration/brainstorm/P3-codegraph-opportunities/merged-requirements.md` §2.1, D-28, FR-04, FR-11) recommended CLI-first and no `CODEGRAPH_MCP_TOOLS` in v1, mainly because the listing is a global decision and the always-loaded schema overhead is unmeasured. The draft Phase 3 replacement map (`.dev/codegraph-migration/specs/phase-3-codegraph-adoption-spec.md` §1) assumed MCP-first.
- Repo rule: smallest correct change; no speculative machinery (`~/.claude/CLAUDE.md` rule 7, the ladder).

## Criteria

1. Correctness of answers reaching the model (freshness, worktree provenance).
2. Works for every primitive class: main session, unrestricted-Bash orchestrators, closed-Bash orchestrators, read-only agents.
3. Safety (no path to mutating verbs; read-only agents stay read-only).
4. Token and latency cost.
5. Cross-phase dependency (what Phase 2 must change) and implementation size in Phase 3.
6. Failure behaviour when codegraph or the index is missing.
