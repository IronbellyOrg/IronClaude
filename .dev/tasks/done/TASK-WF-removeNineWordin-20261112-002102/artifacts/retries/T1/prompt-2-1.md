55cb1afbedc5de3eadad0ad35adfdd1a97914451
Review one task for spec compliance.

Task brief: ## Task 1: Edit the shared guide in src/superclaude/core/CODEGRAPH.md

In section 2, step 3, add the wait on the MCP path: before the single `codegraph_status` call, if `pgrep -f 'codegraph\.js (init|index)'` prints a line, wait for it to end (poll up to 60 s) and then make the one check; if it is still running after 60 s, record `index_state: stale` with `graph:stale` and make no status call; still exactly one status call per run (item 1). Rewrite the tail of section 5 rule 7, "MCP `codegraph_status` needs no guard", so it no longer contradicts this: the CLI `status` stays guarded and skipped while an init runs, the MCP `status` waits as step 3 says. In step 7, say that `checked_at` is taken with one `date -u +%Y-%m-%dT%H:%M:%SZ` (Bash) immediately after the status call (item 4). In the section 4 row "Overview", change the MCP form to `codegraph_files {format:"grouped", maxDepth:2, path?}` and add that `path` set to the target's directory is recommended when the target is narrower than the repo (item 2). For item 7, section 3 already defines `graph:empty`, `graph:truncated` and `graph:unresolved`: add one clause to section 3 saying a single failed or empty lookup records the matching one of these tokens in the host's `degraded` list, and that no new token is added.

Acceptance criteria:
- `src/superclaude/core/CODEGRAPH.md` contains the pgrep-then-wait-up-to-60-s clause in section 2 with the `graph:stale` outcome and still states one status call per run; rule 7 no longer says the MCP status "needs no guard".
- The same file names the `date -u +%Y-%m-%dT%H:%M:%SZ` source for `checked_at` and a `path` argument on the `codegraph_files` row, and the section 3 clause about single failed or empty lookups.
- `uv run pytest tests/core/test_codegraph_guide.py -q` passes: at most 120 lines, tokens inside the closed list, banned names only in Never, no `src/superclaude/` text.

AC ids:
T1.AC1: `src/superclaude/core/CODEGRAPH.md` contains the pgrep-then-wait-up-to-60-s clause in section 2 with the `graph:stale` outcome and still states one status call per run; rule 7 no longer says the MCP status "needs no guard".
T1.AC2: The same file names the `date -u +%Y-%m-%dT%H:%M:%SZ` source for `checked_at` and a `path` argument on the `codegraph_files` row, and the section 3 clause about single failed or empty lookups.
T1.AC3: `uv run pytest tests/core/test_codegraph_guide.py -q` passes: at most 120 lines, tokens inside the closed list, banned names only in Never, no `src/superclaude/` text.
Global constraints: - Edit only `src/superclaude/commands/analyze.md`, `src/superclaude/commands/design.md`, `src/superclaude/core/CODEGRAPH.md`, `plugins/superclaude/core/CODEGRAPH.md` (a test pins it byte-identical to the source), `tests/skills/test_codegraph_adoption.py` and `tests/core/test_codegraph_guide.py`. The plugin twins of analyze.md and design.md already differ from the source (no codegraph text, `mcp-servers: []`) and no test pins them, so they stay untouched. `scripts/eval_workflow_vs_task_builder.py` pins skill tool lists, which this plan does not change, so it stays untouched unless a test run shows otherwise.
- Do not change behaviour, flags, the one-check-per-run rule, the fresh-and-`access: mcp` rule, the Grep/Read floor or the never-halt rule. Every fix is a clause or one sentence.
- `src/superclaude/core/CODEGRAPH.md` is shared by every primitive: additive clarifications only; it stays at 120 lines or fewer, names no `src/superclaude/` path, adds no `graph:*` token outside the closed list of its section 3 (which already holds `graph:empty` and `graph:truncated`), and names `explore` and the mutating verbs only in its Never section. Each phrase changed is grepped across `src/superclaude` first so no other primitive contradicts it.
- Reference the smoke report only through `./source.md`; never add a `src/superclaude` read path to an installed primitive. Never stage `.claude/`; no commit, no push, no PR.
- All nine report quotes were re-verified against the worktree before planning: the quotes sit at the stated lines of analyze.md (30, 32, 36, 63, 67), design.md (55, 57, 61, 65, 74) and CODEGRAPH.md (13, 22, 50, 74). None is rebutted.
Start sha: 55cb1afbedc5de3eadad0ad35adfdd1a97914451
Diff against the start snapshot: 
diff --git a/src/superclaude/core/CODEGRAPH.md b/src/superclaude/core/CODEGRAPH.md
index f7d3cca79..9af6be2e4 100644
--- a/src/superclaude/core/CODEGRAPH.md
+++ b/src/superclaude/core/CODEGRAPH.md
@@ -10,7 +10,7 @@ codegraph is a read-only code graph of the current git worktree: symbols, call e
 
 1. Switch: `printenv SUPERCLAUDE_CODEGRAPH_PRIMITIVES` prints `off` → `index_state: disabled`, `access: none`, token `graph:disabled`; use the Phase 1 floor (Grep, Glob, Read) and stop the check.
 2. Worktree: `worktree_root` = realpath of `git rev-parse --show-toplevel`; pass it as `projectPath` on every MCP call.
-3. MCP detection: read the session's own tool list, never the kind of run. `mcp__codegraph__codegraph_status` listed → call it with `projectPath`. Not listed → CLI `codegraph status` in `worktree_root`, and only when `pgrep -f 'codegraph\.js (init|index)'` prints nothing; when it prints a line, skip `status`, set `index_state: stale` and token `graph:stale` (an init is running; CLI `status` during an init can empty the index).
+3. MCP detection: read the session's own tool list, never the kind of run. `mcp__codegraph__codegraph_status` listed → call it once with `projectPath`; before that call, when the primitive's Bash allowlist permits `pgrep` and `pgrep -f 'codegraph\.js (init|index)'` prints a line, wait for that build to end (poll up to 60 s); if it is still running after 60 s, skip `status`, set `index_state: stale` and token `graph:stale`. Not listed → CLI `codegraph status` in `worktree_root`, and only when `pgrep -f 'codegraph\.js (init|index)'` prints nothing; when it prints a line, skip `status`, set `index_state: stale` and token `graph:stale` (an init is running; CLI `status` during an init can empty the index).
 4. Version: `codegraph --version` must equal the pin below; otherwise CLI access is `none` (`graph:absent` when the command is missing, `graph:version_mismatch` plus `graph:provenance_unproven` when it differs, `graph:provenance_unproven` when it cannot be read). MCP access is not affected.
 5. Classify the status answer into `index_state: fresh|stale|not_initialized|foreign_index|absent|disabled|error`:
    - "belongs to a different git working tree" → `foreign_index`, `graph:foreign_index` (a nested worktree answering from its parent's index);
@@ -19,7 +19,7 @@ codegraph is a read-only code graph of the current git worktree: symbols, call e
    - a CLI "Pending Changes:" list, or non-zero MCP change counts → `stale`, `graph:stale`;
    - no binary and no MCP tool → `absent`, `graph:absent`; anything else → `error`, `graph:parse_failed`.
 6. Access: lookup tools (`codegraph_search`, `codegraph_callers`, ...) listed → `access: mcp`. Only `codegraph_status` listed → token `graph:unlisted`; then `access: cli` for a primitive whose allowlist names the CLI read verbs and whose `codegraph --version` matches the pin, else `access: none` and the Phase 1 floor (or artifacts the orchestrator put in the brief).
-7. Record `checked_at` (UTC, `YYYY-MM-DDTHH:MM:SSZ`). Re-check after any write in the same run: no primitive syncs the index (see Never), so rows about files the run changed are leads only.
+7. Record `checked_at` (UTC, `YYYY-MM-DDTHH:MM:SSZ`) from one `date -u +%Y-%m-%dT%H:%M:%SZ` (Bash) run right after the status call, because the status answer has no timestamp. Re-check after any write in the same run: no primitive syncs the index (see Never), so rows about files the run changed are leads only.
 
 Agents get the run's state in their brief: `index_state`, `checked_at`, `worktree_root` and the `projectPath` to pass; they call codegraph only when `index_state: fresh`.
 
@@ -29,7 +29,7 @@ Who indexes: Phase 2's SessionStart hook starts `codegraph init --yes` in every
 
 `graph:absent`, `graph:unlisted`, `graph:disabled`, `graph:not_initialized`, `graph:foreign_index`, `graph:stale`, `graph:version_mismatch`, `graph:provenance_unproven`, `graph:empty`, `graph:ambiguous`, `graph:truncated`, `graph:parse_failed`, `graph:unresolved`, `graph:telemetry_on`.
 
-Add the matching token to the host primitive's existing `degraded` / `degraded_components` list and continue on the floor; no token stops a run. For `graph:not_initialized` tell the user: run `/sc:graph status`; it reports `next_action: run_graph_init`. `graph:disabled` means the user set `SUPERCLAUDE_CODEGRAPH_PRIMITIVES=off`.
+Add the matching token to the host primitive's existing `degraded` / `degraded_components` list and continue on the floor; no token stops a run. A single lookup that fails or returns nothing records `graph:empty` the same way (`graph:truncated` for a caller list shorter than its total, `graph:unresolved` for a row you could not confirm); no new token is added. For `graph:not_initialized` tell the user: run `/sc:graph status`; it reports `next_action: run_graph_init`. `graph:disabled` means the user set `SUPERCLAUDE_CODEGRAPH_PRIMITIVES=off`.
 
 Pinned codegraph version: 1.6.2
 Freshness experiment E-1: outcome-A
@@ -47,7 +47,7 @@ E-1 outcome A: CLI `status` lists pending files right after a write even with no
 | Who calls X | `codegraph_callers {symbol, file?, limit}` | `codegraph callers <name> --json --limit <n>` |
 | What X calls | `codegraph_callees {symbol, file?, limit}` | `codegraph callees <name> --json --limit <n>` |
 | Impact before an edit | `codegraph_impact {symbol, file?, depth}` | `codegraph impact <name> --depth <n> --json` |
-| Overview | `codegraph_files {format:"grouped", maxDepth:2}` | none |
+| Overview (set `path` to the target's directory when the target is narrower than the repo) | `codegraph_files {format:"grouped", maxDepth:2, path?}` | none |
 | Readiness | `codegraph_status {projectPath}` | guarded `codegraph status` (section 2) |
 | Tests affected by changed files | none | `codegraph affected <files...> --json --quiet` (files as arguments; advisory) |
 
@@ -71,7 +71,7 @@ Rules for every primitive:
 4. Agents get exact names (`mcp__codegraph__codegraph_<tool>`, never a wildcard) and the run's state in the brief (section 2).
 5. No mutating verb in a skill or agent, and no wildcard allowlist (see Never).
 6. Both tool-list branches: the same primitive text works whether Phase 2 registered seven tools or only `codegraph_status` (section 4).
-7. Guard every CLI `status` with `pgrep -f 'codegraph\.js (init|index)'`; MCP `codegraph_status` needs no guard.
+7. Guard every CLI `status` with `pgrep -f 'codegraph\.js (init|index)'` (skip it while one runs); the MCP `codegraph_status` takes the bounded wait of section 2 step 3 instead.
 8. Call the CLI as bare `codegraph` (what exact allowlist patterns match); Phase 2's pointer `~/.codegraph/.superclaude-bin` is for the hook and the main session.
 9. Tier above the floor: a codegraph step goes before the existing Grep/Read step, which stays unchanged; never "skip" where a floor exists.
 
diff --git a/plugins/superclaude/core/CODEGRAPH.md b/plugins/superclaude/core/CODEGRAPH.md
index f7d3cca79..9af6be2e4 100644
--- a/plugins/superclaude/core/CODEGRAPH.md
+++ b/plugins/superclaude/core/CODEGRAPH.md
@@ -10,7 +10,7 @@ codegraph is a read-only code graph of the current git worktree: symbols, call e
 
 1. Switch: `printenv SUPERCLAUDE_CODEGRAPH_PRIMITIVES` prints `off` → `index_state: disabled`, `access: none`, token `graph:disabled`; use the Phase 1 floor (Grep, Glob, Read) and stop the check.
 2. Worktree: `worktree_root` = realpath of `git rev-parse --show-toplevel`; pass it as `projectPath` on every MCP call.
-3. MCP detection: read the session's own tool list, never the kind of run. `mcp__codegraph__codegraph_status` listed → call it with `projectPath`. Not listed → CLI `codegraph status` in `worktree_root`, and only when `pgrep -f 'codegraph\.js (init|index)'` prints nothing; when it prints a line, skip `status`, set `index_state: stale` and token `graph:stale` (an init is running; CLI `status` during an init can empty the index).
+3. MCP detection: read the session's own tool list, never the kind of run. `mcp__codegraph__codegraph_status` listed → call it once with `projectPath`; before that call, when the primitive's Bash allowlist permits `pgrep` and `pgrep -f 'codegraph\.js (init|index)'` prints a line, wait for that build to end (poll up to 60 s); if it is still running after 60 s, skip `status`, set `index_state: stale` and token `graph:stale`. Not listed → CLI `codegraph status` in `worktree_root`, and only when `pgrep -f 'codegraph\.js (init|index)'` prints nothing; when it prints a line, skip `status`, set `index_state: stale` and token `graph:stale` (an init is running; CLI `status` during an init can empty the index).
 4. Version: `codegraph --version` must equal the pin below; otherwise CLI access is `none` (`graph:absent` when the command is missing, `graph:version_mismatch` plus `graph:provenance_unproven` when it differs, `graph:provenance_unproven` when it cannot be read). MCP access is not affected.
 5. Classify the status answer into `index_state: fresh|stale|not_initialized|foreign_index|absent|disabled|error`:
    - "belongs to a different git working tree" → `foreign_index`, `graph:foreign_index` (a nested worktree answering from its parent's index);
@@ -19,7 +19,7 @@ codegraph is a read-only code graph of the current git worktree: symbols, call e
    - a CLI "Pending Changes:" list, or non-zero MCP change counts → `stale`, `graph:stale`;
    - no binary and no MCP tool → `absent`, `graph:absent`; anything else → `error`, `graph:parse_failed`.
 6. Access: lookup tools (`codegraph_search`, `codegraph_callers`, ...) listed → `access: mcp`. Only `codegraph_status` listed → token `graph:unlisted`; then `access: cli` for a primitive whose allowlist names the CLI read verbs and whose `codegraph --version` matches the pin, else `access: none` and the Phase 1 floor (or artifacts the orchestrator put in the brief).
-7. Record `checked_at` (UTC, `YYYY-MM-DDTHH:MM:SSZ`). Re-check after any write in the same run: no primitive syncs the index (see Never), so rows about files the run changed are leads only.
+7. Record `checked_at` (UTC, `YYYY-MM-DDTHH:MM:SSZ`) from one `date -u +%Y-%m-%dT%H:%M:%SZ` (Bash) run right after the status call, because the status answer has no timestamp. Re-check after any write in the same run: no primitive syncs the index (see Never), so rows about files the run changed are leads only.
 
 Agents get the run's state in their brief: `index_state`, `checked_at`, `worktree_root` and the `projectPath` to pass; they call codegraph only when `index_state: fresh`.
 
@@ -29,7 +29,7 @@ Who indexes: Phase 2's SessionStart hook starts `codegraph init --yes` in every
 
 `graph:absent`, `graph:unlisted`, `graph:disabled`, `graph:not_initialized`, `graph:foreign_index`, `graph:stale`, `graph:version_mismatch`, `graph:provenance_unproven`, `graph:empty`, `graph:ambiguous`, `graph:truncated`, `graph:parse_failed`, `graph:unresolved`, `graph:telemetry_on`.
 
-Add the matching token to the host primitive's existing `degraded` / `degraded_components` list and continue on the floor; no token stops a run. For `graph:not_initialized` tell the user: run `/sc:graph status`; it reports `next_action: run_graph_init`. `graph:disabled` means the user set `SUPERCLAUDE_CODEGRAPH_PRIMITIVES=off`.
+Add the matching token to the host primitive's existing `degraded` / `degraded_components` list and continue on the floor; no token stops a run. A single lookup that fails or returns nothing records `graph:empty` the same way (`graph:truncated` for a caller list shorter than its total, `graph:unresolved` for a row you could not confirm); no new token is added. For `graph:not_initialized` tell the user: run `/sc:graph status`; it reports `next_action: run_graph_init`. `graph:disabled` means the user set `SUPERCLAUDE_CODEGRAPH_PRIMITIVES=off`.
 
 Pinned codegraph version: 1.6.2
 Freshness experiment E-1: outcome-A
@@ -47,7 +47,7 @@ E-1 outcome A: CLI `status` lists pending files right after a write even with no
 | Who calls X | `codegraph_callers {symbol, file?, limit}` | `codegraph callers <name> --json --limit <n>` |
 | What X calls | `codegraph_callees {symbol, file?, limit}` | `codegraph callees <name> --json --limit <n>` |
 | Impact before an edit | `codegraph_impact {symbol, file?, depth}` | `codegraph impact <name> --depth <n> --json` |
-| Overview | `codegraph_files {format:"grouped", maxDepth:2}` | none |
+| Overview (set `path` to the target's directory when the target is narrower than the repo) | `codegraph_files {format:"grouped", maxDepth:2, path?}` | none |
 | Readiness | `codegraph_status {projectPath}` | guarded `codegraph status` (section 2) |
 | Tests affected by changed files | none | `codegraph affected <files...> --json --quiet` (files as arguments; advisory) |
 
@@ -71,7 +71,7 @@ Rules for every primitive:
 4. Agents get exact names (`mcp__codegraph__codegraph_<tool>`, never a wildcard) and the run's state in the brief (section 2).
 5. No mutating verb in a skill or agent, and no wildcard allowlist (see Never).
 6. Both tool-list branches: the same primitive text works whether Phase 2 registered seven tools or only `codegraph_status` (section 4).
-7. Guard every CLI `status` with `pgrep -f 'codegraph\.js (init|index)'`; MCP `codegraph_status` needs no guard.
+7. Guard every CLI `status` with `pgrep -f 'codegraph\.js (init|index)'` (skip it while one runs); the MCP `codegraph_status` takes the bounded wait of section 2 step 3 instead.
 8. Call the CLI as bare `codegraph` (what exact allowlist patterns match); Phase 2's pointer `~/.codegraph/.superclaude-bin` is for the hook and the main session.
 9. Tier above the floor: a codegraph step goes before the existing Grep/Read step, which stays unchanged; never "skip" where a floor exists.
 

Delta diff from the previous reviewed tree (empty on the first review): 
diff --git a/plugins/superclaude/core/CODEGRAPH.md b/plugins/superclaude/core/CODEGRAPH.md
index f7d3cca79..9af6be2e4 100644
--- a/plugins/superclaude/core/CODEGRAPH.md
+++ b/plugins/superclaude/core/CODEGRAPH.md
@@ -10,7 +10,7 @@ codegraph is a read-only code graph of the current git worktree: symbols, call e
 
 1. Switch: `printenv SUPERCLAUDE_CODEGRAPH_PRIMITIVES` prints `off` → `index_state: disabled`, `access: none`, token `graph:disabled`; use the Phase 1 floor (Grep, Glob, Read) and stop the check.
 2. Worktree: `worktree_root` = realpath of `git rev-parse --show-toplevel`; pass it as `projectPath` on every MCP call.
-3. MCP detection: read the session's own tool list, never the kind of run. `mcp__codegraph__codegraph_status` listed → call it with `projectPath`. Not listed → CLI `codegraph status` in `worktree_root`, and only when `pgrep -f 'codegraph\.js (init|index)'` prints nothing; when it prints a line, skip `status`, set `index_state: stale` and token `graph:stale` (an init is running; CLI `status` during an init can empty the index).
+3. MCP detection: read the session's own tool list, never the kind of run. `mcp__codegraph__codegraph_status` listed → call it once with `projectPath`; before that call, when the primitive's Bash allowlist permits `pgrep` and `pgrep -f 'codegraph\.js (init|index)'` prints a line, wait for that build to end (poll up to 60 s); if it is still running after 60 s, skip `status`, set `index_state: stale` and token `graph:stale`. Not listed → CLI `codegraph status` in `worktree_root`, and only when `pgrep -f 'codegraph\.js (init|index)'` prints nothing; when it prints a line, skip `status`, set `index_state: stale` and token `graph:stale` (an init is running; CLI `status` during an init can empty the index).
 4. Version: `codegraph --version` must equal the pin below; otherwise CLI access is `none` (`graph:absent` when the command is missing, `graph:version_mismatch` plus `graph:provenance_unproven` when it differs, `graph:provenance_unproven` when it cannot be read). MCP access is not affected.
 5. Classify the status answer into `index_state: fresh|stale|not_initialized|foreign_index|absent|disabled|error`:
    - "belongs to a different git working tree" → `foreign_index`, `graph:foreign_index` (a nested worktree answering from its parent's index);
@@ -19,7 +19,7 @@ codegraph is a read-only code graph of the current git worktree: symbols, call e
    - a CLI "Pending Changes:" list, or non-zero MCP change counts → `stale`, `graph:stale`;
    - no binary and no MCP tool → `absent`, `graph:absent`; anything else → `error`, `graph:parse_failed`.
 6. Access: lookup tools (`codegraph_search`, `codegraph_callers`, ...) listed → `access: mcp`. Only `codegraph_status` listed → token `graph:unlisted`; then `access: cli` for a primitive whose allowlist names the CLI read verbs and whose `codegraph --version` matches the pin, else `access: none` and the Phase 1 floor (or artifacts the orchestrator put in the brief).
-7. Record `checked_at` (UTC, `YYYY-MM-DDTHH:MM:SSZ`). Re-check after any write in the same run: no primitive syncs the index (see Never), so rows about files the run changed are leads only.
+7. Record `checked_at` (UTC, `YYYY-MM-DDTHH:MM:SSZ`) from one `date -u +%Y-%m-%dT%H:%M:%SZ` (Bash) run right after the status call, because the status answer has no timestamp. Re-check after any write in the same run: no primitive syncs the index (see Never), so rows about files the run changed are leads only.
 
 Agents get the run's state in their brief: `index_state`, `checked_at`, `worktree_root` and the `projectPath` to pass; they call codegraph only when `index_state: fresh`.
 
@@ -29,7 +29,7 @@ Who indexes: Phase 2's SessionStart hook starts `codegraph init --yes` in every
 
 `graph:absent`, `graph:unlisted`, `graph:disabled`, `graph:not_initialized`, `graph:foreign_index`, `graph:stale`, `graph:version_mismatch`, `graph:provenance_unproven`, `graph:empty`, `graph:ambiguous`, `graph:truncated`, `graph:parse_failed`, `graph:unresolved`, `graph:telemetry_on`.
 
-Add the matching token to the host primitive's existing `degraded` / `degraded_components` list and continue on the floor; no token stops a run. For `graph:not_initialized` tell the user: run `/sc:graph status`; it reports `next_action: run_graph_init`. `graph:disabled` means the user set `SUPERCLAUDE_CODEGRAPH_PRIMITIVES=off`.
+Add the matching token to the host primitive's existing `degraded` / `degraded_components` list and continue on the floor; no token stops a run. A single lookup that fails or returns nothing records `graph:empty` the same way (`graph:truncated` for a caller list shorter than its total, `graph:unresolved` for a row you could not confirm); no new token is added. For `graph:not_initialized` tell the user: run `/sc:graph status`; it reports `next_action: run_graph_init`. `graph:disabled` means the user set `SUPERCLAUDE_CODEGRAPH_PRIMITIVES=off`.
 
 Pinned codegraph version: 1.6.2
 Freshness experiment E-1: outcome-A
@@ -47,7 +47,7 @@ E-1 outcome A: CLI `status` lists pending files right after a write even with no
 | Who calls X | `codegraph_callers {symbol, file?, limit}` | `codegraph callers <name> --json --limit <n>` |
 | What X calls | `codegraph_callees {symbol, file?, limit}` | `codegraph callees <name> --json --limit <n>` |
 | Impact before an edit | `codegraph_impact {symbol, file?, depth}` | `codegraph impact <name> --depth <n> --json` |
-| Overview | `codegraph_files {format:"grouped", maxDepth:2}` | none |
+| Overview (set `path` to the target's directory when the target is narrower than the repo) | `codegraph_files {format:"grouped", maxDepth:2, path?}` | none |
 | Readiness | `codegraph_status {projectPath}` | guarded `codegraph status` (section 2) |
 | Tests affected by changed files | none | `codegraph affected <files...> --json --quiet` (files as arguments; advisory) |
 
@@ -71,7 +71,7 @@ Rules for every primitive:
 4. Agents get exact names (`mcp__codegraph__codegraph_<tool>`, never a wildcard) and the run's state in the brief (section 2).
 5. No mutating verb in a skill or agent, and no wildcard allowlist (see Never).
 6. Both tool-list branches: the same primitive text works whether Phase 2 registered seven tools or only `codegraph_status` (section 4).
-7. Guard every CLI `status` with `pgrep -f 'codegraph\.js (init|index)'`; MCP `codegraph_status` needs no guard.
+7. Guard every CLI `status` with `pgrep -f 'codegraph\.js (init|index)'` (skip it while one runs); the MCP `codegraph_status` takes the bounded wait of section 2 step 3 instead.
 8. Call the CLI as bare `codegraph` (what exact allowlist patterns match); Phase 2's pointer `~/.codegraph/.superclaude-bin` is for the hook and the main session.
 9. Tier above the floor: a codegraph step goes before the existing Grep/Read step, which stays unchanged; never "skip" where a floor exists.
 

Earlier blocking findings of this start (empty on the first review): F1.1 sev=blocking trigger=B1 ac=T1.AC3 at=tests/core/test_codegraph_guide.py:134 anchor="`uv run pytest tests/core/test_codegraph_guide.py -q` passes" chk=y,n,n,n family=plugin-twin-sync fix=copy src/superclaude/core/CODEGRAPH.md byte for byte to plugins/superclaude/core/CODEGRAPH.md and rerun the test file covers="`uv run pytest tests/core/test_codegraph_guide.py -q` passes" first=A1 origin=new: the source guide was edited, but the plugin twin plugins/superclaude/core/CODEGRAPH.md was not updated, so the byte-identity test fails and the test file does not pass.

Saved-probe re-check hit locations (may be empty): plugins/superclaude/core/CODEGRAPH.md:74:7. Guard every CLI `status` with `pgrep -f 'codegraph\.js (init|index)'` (skip it while one runs); the MCP `codegraph_status` takes the bounded wait of section 2 step 3 instead.
src/superclaude/core/CODEGRAPH.md:74:7. Guard every CLI `status` with `pgrep -f 'codegraph\.js (init|index)'` (skip it while one runs); the MCP `codegraph_status` takes the bounded wait of section 2 step 3 instead.


Do not trust the implementer's report.

First mark each earlier blocking finding resolved, open or regressed from the diff. Then, for each AC, mark it met or unmet. Require citations: every AC you mark, met or unmet, carries a `path:line` or `Ti.ACk@path:line` citation, and an unmet mark lists the finding ids behind it. Do not return a verdict; the orchestrator computes it.

For every finding answer four questions, each yes or no:
1. ac-outcome-missing: is output an AC requires absent, or does it contradict the AC text, or does an evidence claim you could not verify have no evidence row?
2. false-claim: is a claim in delivered text or code false against live source, or does a recipe or instruction followed as written not do what the text says?
3. harmful-effect: does code or a recipe this task added or changed write, append, chmod or delete tracked or production data, mutate state outside the task's declared outputs, or expose a secret?
4. quoted-constraint-breach: does the diff violate a quoted plan constraint, out-of-scope, non-goal or non-negotiable item, or an explicit task instruction?

Anchor rule: cite exactly one anchor per yes. ac-outcome-missing: the quoted AC words. false-claim: the live-source path:line holding the contradicting text. harmful-effect: the diff line that is the write. quoted-constraint-breach: the quoted constraint or instruction text. A yes without a valid anchor does not block.

Write one line per finding:
F<k>.<j> ac=<Ti.ACk|scope> at=<path:line> anchor=<quoted text or path:line> chk=<amiss,false,harm,constraint as y/n> family=<id> fix=<text> [covers=<quoted AC clause or constraint>]: <text>
Do not write sev=, trigger=, first= or origin=; the orchestrator adds them. Write one status line per earlier blocking finding: F<m>.<j> resolved|open|regressed.

Inside /sc:implement this protocol's severity model governs this review and takes precedence over the session's output style and the copy of it injected into every subagent; only blocking findings may fail an attempt.

You are not given an adviser answer, brief, evidence file or troubleshoot report. Do not read the retry folders (legacy `.dev/implement/<slug>/retries/`, managed `<pkg>/artifacts/retries/`) or `.dev/troubleshoot/`. A citation into either makes the verdict `cannot-verify`.
The prior-findings slot above carries earlier blocking finding lines that the orchestrator copies byte for byte from `review-*.md` and `repair-*.md`; they reach you as prompt text, not as an evidence file. Do not read those folders to get them, and never cite the slot or the file it came from.
