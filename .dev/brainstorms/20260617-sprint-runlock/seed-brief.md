---
topic: "Release-level run-lock for `superclaude sprint run` to prevent concurrent runs on the same release directory"
domain: code
strategy: systematic
depth: standard
proposals_target: 3
handoff_target: task
created: 2026-06-17T01:45:00Z
---

# Seed Brief: sprint-runlock

## Problem Statement

`superclaude sprint run` has **no mutual-exclusion lock**. Two concurrent `sprint run`
invocations against the same release directory execute simultaneously and collide on
shared mutable state, which produces a hard `SIGSEGV` ("Segmentation fault (core dumped)")
at phase/task subprocess-spawn boundaries. This was confirmed empirically: an **exclusive**
run crossed every phase boundary (4→5→6) cleanly with zero segfaults over 2h35m, whereas
the user's crashing runs were detected as overlapping (`resume/planner.py:292` →
"2 phase_start events, 0 closes (concurrent runs?)").

## Known Context (grounded in code)

- `execute_sprint()` (`src/superclaude/cli/sprint/executor.py:1586`) has no lock acquisition at startup.
- A reusable PID-lockfile pattern already exists: `acquire_recovery_lock` / `release_recovery_lock`
  (`src/superclaude/cli/sprint/recovery.py:275-353`):
  - Lockfile `<results_dir>/.recovery-locks/phase-{phase}.lock`, JSON `{"pid", "timestamp"}`.
  - Liveness via `os.kill(pid, 0)`: `ProcessLookupError` → dead → reclaim stale lock; `PermissionError` → treat as alive.
  - Auto-release via `atexit` + a `SIGTERM` handler; raises `click.ClickException` when held by a live PID.
  - **Known weaknesses to improve for the run lock:** (a) check-then-write TOCTOU race (`exists()` then `write_text()`); (b) only `SIGTERM` is handled (not `SIGINT`); (c) `atexit`/signal handlers do NOT run on `SIGKILL`/`SIGSEGV`, so a crashed run leaves a stale lock — stale-PID reclamation is the only recovery.
- Passive concurrent-run detection exists but only guards **auto-resume**, not fresh `--start` runs
  (`commands.py:307` and `commands.py:862`).
- `rerun-tasks` already acquires the **phase-scoped** recovery lock (`rerun_tasks.py` step 1).
  The new run lock is **release-scoped** and must compose with it without deadlock.
- The shared state that gets corrupted: `results/.isolation/phase-N/`, `results/handoff/`,
  `execution-log.jsonl`, tasklist checkbox mutations, and per-phase claude isolation dirs
  (`CLAUDE_SETTINGS_DIR`/`CLAUDE_PLUGIN_DIR`).

## Constraints

- Reuse the existing `recovery.py` lock pattern; do not invent a parallel mechanism.
- Must not break: `--no-tmux` and tmux launch paths, auto-resume, explicit `--start/--end`, `rerun-tasks`.
- Lock must be acquired by the process that actually runs `execute_sprint()` (inside tmux when tmux is used), not the launcher shim.
- Acquisition must be **atomic** (no TOCTOU) — two simultaneous starts must not both win.
- Stale lock from a crashed run (SIGSEGV/SIGKILL, where handlers don't fire) must be auto-reclaimable on next start.
- Clear, actionable error naming the holding PID + timestamp + remediation, plus an explicit override escape hatch.
- Pure-stdlib; no new dependencies. Lives in `recovery.py` next to the sibling lock.

## Success Criteria

- A second `sprint run` on a release with a live run **refuses to start** with a clear PID-named error.
- A `sprint run` after a crashed run (stale lock, dead PID) **reclaims and proceeds**.
- Lock is released on normal exit, `SIGTERM`, and `SIGINT`; reclaimed-on-stale covers `SIGKILL`/`SIGSEGV`.
- `rerun-tasks` and `run` cannot deadlock against each other (documented lock ordering / scope separation).
- New unit tests cover: live-holder refusal, stale reclamation, atomic-acquisition race, release-on-exit, signal release, override flag.
- Existing sprint tests still pass; no regression to resume/tmux/rerun paths.

## Open Questions (for adversarial debate)

1. Atomic acquisition mechanism: `os.open(O_CREAT|O_EXCL)` vs `fcntl.flock` vs `O_EXCL` + PID file — which best handles stale reclamation AND atomicity AND NFS/container filesystems?
2. Should `rerun-tasks` also acquire/respect the **run** lock, or stay on its phase recovery lock only? If both, what acquisition order prevents deadlock?
3. Override escape hatch: a `--force`/`--ignore-run-lock` flag vs. "delete the lockfile" instruction only?
4. Where exactly in `execute_sprint()` to acquire (before/after TUI start, before/after preflight python-mode phases) and where to release?
5. tmux path: does the lock get acquired in the tmux-inner process correctly, and is the error surfaced to the user who ran the outer command?

## Enrichment Context

Codebase enrichment performed inline (Auggie + direct reads during the preceding diagnosis).
Authoritative anchors: `recovery.py:275-353` (lock pattern to reuse), `executor.py:1586`
(`execute_sprint` entry), `commands.py:307,862` (passive detection), `resume/planner.py:292`
(concurrent-run detector). Full enrichment artifact: `enrichment/codebase-context.md`.
