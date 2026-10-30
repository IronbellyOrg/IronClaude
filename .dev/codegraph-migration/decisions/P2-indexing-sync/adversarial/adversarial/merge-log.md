# Merge Log

## Metadata
- Base: Variant 2 (option-b, SessionStart hook), `variant-2-original.md`, combined score 0.886
- Plan: `refactor-plan.md` (7 planned changes, 4 rejected alternatives; auto-approved 2026-10-29T16:45:00Z)
- Executor: merge-executor (sc:adversarial Step 5)
- Changes applied: 7/7 (0 skipped, 0 escalated as blocked)
- Output: `../P2-indexing-sync-merged.md`
- Status: COMPLETE, validation passed with one observation (below)
- Timestamp: 2026-10-29

## Changes Applied

| # | Status | Before (base) | After (merged) | Provenance tag |
|---|---|---|---|---|
| 1 | applied | Step 4: garbled sentence (`nohup … >"$top/.codegraph-init.log" 2>&1 &` is avoided; log goes to …) | Step 5: one exact `nohup sh -c '…' _ "$top" </dev/null >>"$log" 2>&1 &` with `log=${XDG_STATE_HOME:-$HOME/.local/state}/superclaude/codegraph-init.log`; no `setsid` | Base modified — Change 1 |
| 2 | applied | Step 3: exit if `$top/.codegraph/codegraph.db` exists | Step 4: exit if `$top/.codegraph/.superclaude-init-ok` exists; detached run is `init --yes && touch` marker; no `rm` on failure | Base modified — Change 2 |
| 3 | applied | Step 4: guarded by a `mkdir` lock | Step 6: no IronClaude lock; codegraph's own writer lock; lock re-add is probe-gated | Base modified — Change 3 |
| 4 | applied | "Core CLAUDE.md rule from Option A is kept as the fallback" | Quoted guidance: any codegraph error / not initialized / different working tree, then `init --yes` at `git rev-parse --show-toplevel` and retry; `index --force` after interrupted init; never `sync` while a session is open | Base modified — Change 4, from Variant 1 |
| 5 | applied | No docs page | Docs page bullet: `init --yes`, `uninit`, `index --force`, `codegraph.json` excludes, ~70 KB/file, ~1 GB peak RSS, opt-out env var | Variant 1, Change 5 |
| 6 | applied | No statement of the MCP-registration dependency | Dependency (A-004) bullet: watcher runs only while codegraph is registered and connected; separate decision | Variant 1, Change 6 |
| 7 | applied | No V3 content | Docs-only opt-in `post-checkout` recipe (`init --yes`, backgrounded, `|| true`, never `sync`); installer never writes global git config | Variant 3, Change 7 |

Rejected alternatives honoured: V1 no-hook default (C-001/X-002), V3 global `init.templateDir` (C-004), V3 `sync --quiet` in git hooks (C-002/X-001), PID-file lock (C-006; kept only as the probe-2 fallback, as the plan states).

## Post-Merge Validation

### Structural integrity: PASS
- One H1, six H2 sections in order: What ships, Hook behaviour, Core CLAUDE.md guidance, Docs page and dependency, Pre-ship probes, Evidence. No skipped heading levels.
- Provenance header present (3 lines); 7 `<!-- Source: ... -->` tags, one before the verdict and one before each H2.
- Hook steps numbered 1-6 in execution order; the per-worktree base bullet kept after them.

### Internal references: PASS
- Every path named (`src/superclaude/hooks/scripts/codegraph-session-start.sh`, `src/superclaude/hooks/hooks.json`, `src/superclaude/cli/install_hooks.py`, `plugins/superclaude/hooks/hooks.json`, `tests/unit/test_cli_install.py`, `src/superclaude/core/CLAUDE.md`) matches `context.md` "IronClaude facts".
- Marker path is identical in step 4 and the step 5 command; opt-out variable spelled identically in step 2 and the docs bullet.
- Debate IDs cited (A-003, A-004, A-006) exist in `debate-transcript.md`.

### New-contradiction rescan: PASS (0 contradictions)
- vs `context.md`: `init --yes` ~125 ms no-op on an indexed checkout (matches); home/root skip (consistent with init's refusal); never `sync` while the daemon runs (matches the lock-error fact); ~70 KB/file is consistent with 34 MB for 500 files; ~1 GB peak RSS matches; no global git config (matches). Nested worktrees get their own index via `--show-toplevel`, which avoids the parent-index fallback rather than contradicting it.
- vs plan: no `codegraph.db` fast path remains; no `mkdir` lock remains; no `rm` on failure; no `setsid`; no global git config; `sync` appears only in "never" statements.
- vs base: the base claim that a DB-existence check is a valid fast path is the only removed claim, removed by Change 2 as planned.

### Observation for the orchestrator (not applied; outside plan scope)
- Step 5 appends to `$log`, but neither the base nor the plan creates the log directory. If `${XDG_STATE_HOME:-$HOME/.local/state}/superclaude/` does not exist, the redirect fails, the background init never starts, and the shell may print an error on stderr. A `mkdir -p` of the log directory before the `nohup` line would close this. Not added, because the executor adds no unplanned content.
- Resolution (orchestrator): the plan's Change 1 was amended, and step 5 of the merged file now runs `mkdir -p "${log%/*}" || exit 0` before `nohup`. The line count is unchanged.

### Line count
- `wc -l P2-indexing-sync-merged.md`: 46 (limit: fewer than 50). PASS.

## Summary
All 7 planned changes were applied in order to the Variant 2 base, with provenance tags on every section. The merged recommendation is 46 lines, structurally sound, references resolve, and the rescan found no new contradictions against `context.md` or the plan. One out-of-scope observation (missing log-directory creation) is raised for the orchestrator to decide on.
