# CODEGRAPH.md - codegraph usage rules for IronClaude primitives

Read this file when a command, skill or agent uses codegraph. It is not loaded into every session. Primitives point here with one line and never copy these rules.

## 1. What it is

codegraph is a read-only code graph of the current git worktree: symbols, call edges, file outlines and impact, kept as one SQLite index per worktree in `<worktree>/.codegraph/` (gitignored). Markdown, files over 1 MB, ignored files and dependency folders are not indexed. A graph answer locates code; it is never a citation.

## 2. Readiness check (once per run)

1. Switch: `printenv SUPERCLAUDE_CODEGRAPH_PRIMITIVES` prints `off` → `index_state: disabled`, `access: none`, token `graph:disabled`; use the Phase 1 floor (Grep, Glob, Read) and stop the check.
2. Worktree: `worktree_root` = realpath of `git rev-parse --show-toplevel`; pass it as `projectPath` on every MCP call.
3. MCP detection: read the session's own tool list, never the kind of run. `mcp__codegraph__codegraph_status` listed → call it with `projectPath`. Not listed → CLI `codegraph status` in `worktree_root`, and only when `pgrep -f 'codegraph\.js (init|index)'` prints nothing; when it prints a line, skip `status`, set `index_state: stale` and token `graph:stale` (an init is running; CLI `status` during an init can empty the index).
4. Version: `codegraph --version` must equal the pin below; otherwise CLI access is `none` (`graph:absent` when the command is missing, `graph:version_mismatch` plus `graph:provenance_unproven` when it differs, `graph:provenance_unproven` when it cannot be read). MCP access is not affected.
5. Classify the status answer into `index_state: fresh|stale|not_initialized|foreign_index|absent|disabled|error`:
   - "belongs to a different git working tree" → `foreign_index`, `graph:foreign_index` (a nested worktree answering from its parent's index);
   - CLI "Not initialized", or MCP "isn't indexed with codegraph" → `not_initialized`, `graph:not_initialized`;
   - CLI "Index is up to date", or MCP "Changes since index: 0 added, 0 modified, 0 removed" → `fresh`;
   - a CLI "Pending Changes:" list, or non-zero MCP change counts → `stale`, `graph:stale`;
   - no binary and no MCP tool → `absent`, `graph:absent`; anything else → `error`, `graph:parse_failed`.
6. Access: lookup tools (`codegraph_search`, `codegraph_callers`, ...) listed → `access: mcp`. Only `codegraph_status` listed → token `graph:unlisted`; then `access: cli` for a primitive whose allowlist names the CLI read verbs and whose `codegraph --version` matches the pin, else `access: none` and the Phase 1 floor (or artifacts the orchestrator put in the brief).
7. Record `checked_at` (UTC, `YYYY-MM-DDTHH:MM:SSZ`). Re-check after any write in the same run: no primitive syncs the index (see Never), so rows about files the run changed are leads only.

Agents get the run's state in their brief: `index_state`, `checked_at`, `worktree_root` and the `projectPath` to pass; they call codegraph only when `index_state: fresh`.

Who indexes: Phase 2's SessionStart hook starts `codegraph init --yes` in every new checkout (switch it off with `SUPERCLAUDE_CODEGRAPH_AUTOINIT=0`); the main session may run `codegraph init --yes` as the codegraph block of `~/.claude/CLAUDE.md` says; among primitives only the user-typed `/sc:graph init` runs `init`. Switches: `SUPERCLAUDE_CODEGRAPH_PRIMITIVES=off` switches off codegraph use in primitives only; `SUPERCLAUDE_CODEGRAPH_AUTOINIT=0` switches off only the session-start index hook.

## 3. Degraded tokens (closed list; invent none)

`graph:absent`, `graph:unlisted`, `graph:disabled`, `graph:not_initialized`, `graph:foreign_index`, `graph:stale`, `graph:version_mismatch`, `graph:provenance_unproven`, `graph:empty`, `graph:ambiguous`, `graph:truncated`, `graph:parse_failed`, `graph:unresolved`, `graph:telemetry_on`.

Add the matching token to the host primitive's existing `degraded` / `degraded_components` list and continue on the floor; no token stops a run. For `graph:not_initialized` tell the user: run `/sc:graph status`; it reports `next_action: run_graph_init`. `graph:disabled` means the user set `SUPERCLAUDE_CODEGRAPH_PRIMITIVES=off`.

Pinned codegraph version: 1.6.2
Freshness experiment E-1: outcome-A

E-1 outcome A: CLI `status` lists pending files right after a write even with no MCP server running, so a stale index is detectable; graph rows are still leads only until confirmed (rule 1).

## 4. Tool table

| Job | MCP tool (seven-tool branch) | CLI form (status-only branch, orchestrators that allow it) |
|---|---|---|
| Where is X defined | `codegraph_search {query, kind?, limit}` | `codegraph query <name> --json --limit <n>` |
| Symbol body, or disambiguate | `codegraph_node {symbol, file?, includeCode:true}` | `codegraph node <name> --file <path>` |
| File outline | `codegraph_node {file, symbolsOnly:true}` | `codegraph node --file <path> --symbols-only` |
| Diff hunk → enclosing declaration | `codegraph_node {file, line}` | `codegraph query <name> --json` spans (`startLine`, `endLine`) |
| Who calls X | `codegraph_callers {symbol, file?, limit}` | `codegraph callers <name> --json --limit <n>` |
| What X calls | `codegraph_callees {symbol, file?, limit}` | `codegraph callees <name> --json --limit <n>` |
| Impact before an edit | `codegraph_impact {symbol, file?, depth}` | `codegraph impact <name> --depth <n> --json` |
| Overview | `codegraph_files {format:"grouped", maxDepth:2}` | none |
| Readiness | `codegraph_status {projectPath}` | guarded `codegraph status` (section 2) |
| Tests affected by changed files | none | `codegraph affected <files...> --json --quiet` (files as arguments; advisory) |

Status-only branch: Phase 2 may register only `codegraph_status`; then lookups use the CLI column (where the allowlist names it) or the Phase 1 floor. Other allowed CLI verbs: `codegraph --version`, `codegraph telemetry status`. `codegraph node` has no `--json`. Allowlists name one exact pattern per verb, for example `Bash(codegraph callers *)`.

## 5. Standing rules

Caller rows give the caller's definition line, not the call site. Before citing one, confirm the call site:

1. CS1: find the caller's span (`codegraph query <caller> --json` `startLine`/`endLine`, or `codegraph_node {symbol}`); none → `resolution: unresolved`.
2. CS2: Grep `\b<callee>\s*\(` with line numbers in that file and keep matches inside the span.
3. CS3: reject matches in comments, strings or docstrings, bare assignments and attribute-only uses.
4. CS4: Read the matched line; it must still hold the call → `resolution: call-site-verified`.
5. CS5: any failure drops the row from cited output; never repair it. At most 5 rows per symbol and 20 per run; every row carries `resolution: def-line|call-site-verified|unresolved`.

Rules for every primitive:

1. Read before cite or edit: re-Read a `file:line` range before quoting it and before any Edit; `codegraph_node` file mode only with `symbolsOnly:true`.
2. Fail open to the Phase 1 floor: codegraph missing, unlisted, not initialized, foreign or stale → Grep/Glob/Read, plus one token from section 3.
3. Empty is not absence: no "no callers", "no dependents" or "no tests" conclusion comes from a graph result; callers are call edges only.
4. Agents get exact names (`mcp__codegraph__codegraph_<tool>`, never a wildcard) and the run's state in the brief (section 2).
5. No mutating verb in a skill or agent, and no wildcard allowlist (see Never).
6. Both tool-list branches: the same primitive text works whether Phase 2 registered seven tools or only `codegraph_status` (section 4).
7. Guard every CLI `status` with `pgrep -f 'codegraph\.js (init|index)'`; MCP `codegraph_status` needs no guard.
8. Call the CLI as bare `codegraph` (what exact allowlist patterns match); Phase 2's pointer `~/.codegraph/.superclaude-bin` is for the hook and the main session.
9. Tier above the floor: a codegraph step goes before the existing Grep/Read step, which stays unchanged; never "skip" where a floor exists.

## 6. Known gaps and fallbacks

- No text search (names only) → Grep. No diagnostics or type checker → the project's own tools through Bash in the orchestrator. No type hierarchy and no implementations tool → `codegraph_search {kind:"class"}` candidates confirmed by Grep and Read. No edits → Read then Edit/Write. No memory.
- Caller lists show 20 rows by default: record `shown/total`, re-query once with a limit up to 100, else `graph:truncated`.
- Dependency folders are not indexed → Read the installed package source or use Context7; else mark the claim `[INFERRED]`.
- The index catches up only while a codegraph MCP server watches the worktree (E-1); otherwise it stays behind until the next sync.

## 7. Never

The only section that names these:

- Call `codegraph_explore`, `codegraph explore` or `codegraph context`.
- Use `codegraph_node` file mode without `symbolsOnly:true`.
- Run CLI `codegraph status` while an init or index is running.
- From a skill or agent, run `codegraph init` (only the user-typed `/sc:graph init` does).
- Run `codegraph install`, `codegraph upgrade`, `codegraph uninstall`, `codegraph uninit`, `codegraph index`, `codegraph sync`, `codegraph unlock`, `codegraph telemetry on|off` or `codegraph prompt-hook` (Phase 2 owns install; no primitive syncs the index).
- Write `Bash(codegraph *)` or `mcp__codegraph__*` in an allowlist.
- Prefix a call with environment variables (`VAR=1 codegraph ...` defeats per-verb allowlist matching; E-3).
