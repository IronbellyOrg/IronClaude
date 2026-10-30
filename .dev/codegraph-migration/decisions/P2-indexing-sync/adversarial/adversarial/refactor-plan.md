# Refactoring Plan

## Overview
- Base: Variant 2 (option-b, SessionStart hook), combined score 0.886
- Incorporated: Variant 1 (option-a) changes 2, 4, 5, 6; Variant 3 (option-c) change 7
- Planned changes: 7. Rejected alternatives: 4.
- Overall risk: Low to Medium. It is a planning document, and the one behavioural change (#2) is retry-safe.
- Output: `../P2-indexing-sync-merged.md` (under 50 lines; a final recommendation, not a copy of the base)

## Planned Changes

### Change 1: Fix the garbled log sentence and make detachment portable
- Source: base clarity defect (base-selection Clarity-1); V2 advocate, Recommended shape
- Target: base step 4
- Approach: replace. Use `nohup sh -c '…' _ "$top" </dev/null >>"$log" 2>&1 &` with `log=${XDG_STATE_HOME:-$HOME/.local/state}/superclaude/codegraph-init.log`. Every file descriptor is redirected so Claude Code does not wait for the child. No `setsid`, which macOS lacks. Amendment (orchestrator, after the merge-executor flagged it): create the log directory first with `mkdir -p "${log%/*}" || exit 0`. Otherwise a missing directory makes the redirect fail and init never starts.
- Risk: Low

### Change 2: Use a completion marker for the fast path instead of DB existence (A-003)
- Source: V1 Weakness 1; V2 Concession 1 (A-003 REJECT); debate A-003 won by V1 at 80%
- Target: base step 3
- Approach: replace. Fast path: exit 0 if `$top/.codegraph/.superclaude-init-ok` exists. Otherwise the detached shell runs `codegraph init --yes "$top" && touch "$top/.codegraph/.superclaude-init-ok"`. A failed or killed init writes no marker, so the next session retries. An index Coder already built makes init a ~125 ms no-op, after which the marker is written. The marker sits inside `.codegraph/`, so `codegraph uninit` clears it with the index. Do not `rm -rf` on failure: a concurrent Coder init could be deleted.
- Risk: Medium. Whether `init --yes` repairs a partial index is UNVERIFIED. Pre-ship probe: if it does not, the detached command becomes `codegraph index --force` when the DB exists without the marker.

### Change 3: Drop the `mkdir` lock
- Source: V1 C-009 (smallest code); V2 Concession 2 (a stale lock after a kill blocks init forever)
- Target: base step 4
- Approach: remove. Rely on codegraph's own single-writer lock. A losing concurrent init exits non-zero, writes no marker, and retries next session.
- Risk: Medium. Concurrent-init behaviour is UNVERIFIED. Pre-ship probe: run two `init --yes` together on one checkout and confirm one fails cleanly with an intact index. Re-add a lock only if this probe fails.

### Change 4: Exact core CLAUDE.md guidance text
- Source: V1 bullet 2 and U-008; V1 and V2 advocates on A-006 (cover any codegraph error, not one phrase)
- Target: base "Core CLAUDE.md rule" bullet
- Approach: replace it with the exact text in the merged file. `codegraph index --force` is the manual repair (evaluation §4: "rebuilds from scratch").
- Risk: Low

### Change 5: Docs page with cost and opt-out (A-005)
- Source: V1 U-007; debate A-005 won by V1 at 90%
- Target: new bullet
- Approach: append. The docs page lists `init --yes`, `uninit`, `index --force`, `codegraph.json` excludes, the cost (~70 KB per file on disk, ~1 GB peak RSS during init), and `SUPERCLAUDE_CODEGRAPH_AUTOINIT=0`.
- Risk: Low

### Change 6: State the MCP-registration dependency (A-004)
- Source: V1 Recommended shape; all three advocates QUALIFY on A-004
- Target: new line
- Approach: append. Freshness relies on the upstream watcher, which runs only while codegraph is registered and connected, a separate decision.
- Risk: Low

### Change 7: The V3 idea as a docs-only opt-in recipe
- Source: V3 U-006; V3 advocate, Recommended shape and Concessions
- Target: docs bullet
- Approach: append. A user-installed `post-checkout` hook runs `codegraph init --yes` backgrounded with `|| true`, and never `sync`. The installer never writes global git config.
- Risk: Low

## Changes NOT Being Made
| Diff point | Non-base approach | Why rejected |
|---|---|---|
| C-001 / X-002 | V1: ship no hook; B later as opt-in, default off | 2 of 3 advocates and all three per-point verdicts on C-001, C-003 and C-007 favour the hook. A-005 is mitigated by the opt-out and the cost disclosure in the docs. |
| C-004 | V3: global `init.templateDir` written by the installer | A new class of global side effect; misses `core.hooksPath` users; does nothing for existing clones (debate C-004 at 95%). |
| C-002 / X-001 | V3: `codegraph sync --quiet` in git hooks | Fights the daemon's writer lock; a hook's exit status can fail `git checkout`; V3 conceded. |
| C-006 | V2 advocate: PID-file lock with a `kill -0` liveness check | More code than the marker plus codegraph's own lock. Keep it only as the fallback if the Change 3 probe fails. |

## Risk Summary
| Change | Risk | Impact if wrong | Rollback |
|---|---|---|---|
| 2 | Medium | A partial index is trusted, the same as the base | Switch the detached command to `index --force` (probe-gated) |
| 3 | Medium | Two inits collide | Re-add a lock (rejected alternative C-006) |
| 1, 4, 5, 6, 7 | Low | Text only | Edit text |

## Review Status
- Approval: auto-approved (non-interactive)
- Timestamp: 2026-10-29T16:45:00Z
