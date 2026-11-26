# Design spec: codegraph support in /sc:analyze (issue #504, analyze session)

- Type: component. Format: spec. Target: `src/superclaude/commands/analyze.md` (125 lines, no backing skill, none to be created).
- Guide followed: `~/.claude/CODEGRAPH.md` (installed copy of `src/superclaude/core/CODEGRAPH.md`). Pattern copied in spirit from `sc-troubleshoot-protocol` and `sc-reflect-protocol`: one readiness check, codegraph only when `index_state: fresh`, permanent Grep/Glob/Read floor, a `graph:*` note on degradation, never halt.
- Ownership: only `src/superclaude/commands/analyze.md` (plus a pinning test only if one must change; the grep over `tests/` found none that pins analyze.md content).

## 1. Requirements

| ID | Requirement |
|---|---|
| R1 | Exactly one codegraph readiness check per run, done once before the Discover step, following section 2 of `~/.claude/CODEGRAPH.md`. No re-check unless the run itself wrote a file (analyze writes only the report, so none). |
| R2 | When `index_state: fresh` and `access: mcp`, use `codegraph_search`, `codegraph_node`, `codegraph_callers`, `codegraph_callees`, `codegraph_impact`, `codegraph_files` before the existing Glob/Grep/Read step in Discover, Scan and Evaluate. The Glob/Grep/Read step stays unchanged. |
| R3 | Any other state (`stale`, `not_initialized`, `foreign_index`, `absent`, `disabled`, `error`, `access: none`) continues on Glob/Grep/Read, records the matching `graph:*` token from the closed list, and never stops the run. |
| R4 | Frontmatter declares the codegraph MCP server the way `reflect.md` does (`mcp-servers: [codegraph]`); Tool Coordination names the tools. |
| R5 | Every existing behaviour, flag, the Unattended mode section and every Boundary (Will / Will Not / Output / Next Step) is kept as written. |
| R6 | No new `src/superclaude/` read-instruction; the guide is named by its installed path `~/.claude/CODEGRAPH.md`. |
| R7 | codegraph stays read-only: no `codegraph init`, `index`, `sync`, `explore`, `context`, no `codegraph_node` file mode without `symbolsOnly:true`, no wildcard allowlist. |

## 2. Interface (edits to analyze.md)

### 2.1 Frontmatter
`mcp-servers: []` becomes `mcp-servers: [codegraph]`. No `allowed-tools` is added: the file has none today and `reflect.md` declares codegraph only through `mcp-servers`.

### 2.2 Behavioral Flow
Keep the five numbered steps. Add one lead-in line before step 1 and one short codegraph clause per step:

- Before step 1: "**Readiness (once per run, before Discover):** run the codegraph readiness check of `~/.claude/CODEGRAPH.md` section 2 once and keep `index_state`, `checked_at`, `worktree_root` for the whole run. Do not repeat it."
- 1 Discover: when fresh, `codegraph_files {format:"grouped", maxDepth:2}` for layout and `codegraph_search` to locate symbols in the target; then the existing language detection (Glob/Read).
- 2 Scan: when fresh, `codegraph_node {symbol, file?, includeCode:true}` for a symbol body, `codegraph_node {file, symbolsOnly:true}` for a file outline, `codegraph_callers` / `codegraph_callees` for call paths (security: entry points to sinks; performance: hot-path callers); then the existing Grep pattern matching.
- 3 Evaluate: when fresh, `codegraph_impact {symbol, depth}` and `codegraph_callers` supply dependency and blast-radius evidence for architecture and quality findings (coupling, change reach, dead-code candidates as leads only).
- 4, 5 unchanged. Report gets one line: `Codegraph: index_state=<state>, checked_at=<UTC>; degraded: <graph:* tokens or none>`.

### 2.3 Tool Coordination
Add one bullet group after Bash/Write, keeping the existing five bullets unchanged:

- **codegraph** (`mcp__codegraph__codegraph_status` once; then `_search`, `_node`, `_callers`, `_callees`, `_impact`, `_files`): used only when `index_state: fresh`, always before the matching Glob/Grep/Read step; Glob, Grep and Read remain the floor.

### 2.4 New section `## Codegraph (optional)` (after Key Patterns, before Examples)
A compact rule block; the guide is the only place the full rules live:

1. Readiness: once per run; `SUPERCLAUDE_CODEGRAPH_PRIMITIVES=off` means `graph:disabled` and the floor (all handled by the guide's section 2).
2. Use only when `index_state: fresh`. Otherwise Glob/Grep/Read, add the matching `graph:*` token to the report's Codegraph line, continue; never halt, never ask.
3. Graph rows are leads, never citations: re-Read a `file:line` before citing it; an empty result is not a "no callers" finding; caller rows give the definition line, so confirm a call site (guide section 5) before citing; a caller list showing fewer than the total is `graph:truncated`.
4. Read-only: never run `codegraph init`, `index`, `sync`, `explore` or `context`.
5. Exact tool names only (`mcp__codegraph__codegraph_<tool>`), `projectPath` = `worktree_root` on every call.
6. Subagents (if the run fans out): pass `index_state`, `checked_at`, `worktree_root`; they call codegraph only when `index_state: fresh`.

### 2.5 Unattended mode and Boundaries
Unchanged. The Codegraph report line is written into the report; `return-contract.yaml` fields do not change. An unreadable or missing codegraph does not make the run failed (success remains "report written").

## 3. Validation

| Acceptance | Check |
|---|---|
| (a) one readiness check, tools named per step | `grep -n 'readiness' analyze.md` shows one check instruction; Discover/Scan/Evaluate lines name the tools |
| (b) fresh-only, floor with note | text "only when `index_state: fresh`" and "graph:*" and "never halt" present |
| (c) frontmatter | `mcp-servers: [codegraph]` |
| (d) no src path | `grep -n 'src/superclaude' analyze.md` has no hit |
| (e) sync | `make sync-dev` then `make verify-sync` |
| (f) tests | `uv run pytest` over tests that cover command files / install of commands |

## 4. Risks
- Over-long edit to a basic-complexity command: keep the new section under about 25 lines.
- Another session edits other src files in this checkout: `verify-sync` may name files not owned here; re-run `make sync-dev` once, never edit them.
