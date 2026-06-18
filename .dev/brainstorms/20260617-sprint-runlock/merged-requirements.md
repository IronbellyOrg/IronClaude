---
topic: "Release-level run-lock for `superclaude sprint run`"
domain: code
adversarial_status: pass
convergence_score: 0.88
created: 2026-06-17T01:50:00Z
source_seed_brief: .dev/brainstorms/20260617-sprint-runlock/seed-brief.md
target_branch: worktree-segfault-repro
---

# Merged Requirements: Sprint `run` Release-Level Run-Lock

## Goal

Prevent two concurrent `superclaude sprint run` processes from executing against the same
release directory — the empirically confirmed root cause of the phase-boundary SIGSEGV.
Reuse and harden the existing PID-lockfile pattern in `recovery.py`.

## R1 — Shared, hardened lock core (refactor, not copy-paste)

Extract a private `_acquire_pid_lock(lock_path: Path, *, force: bool = False) -> Path` in
`src/superclaude/cli/sprint/recovery.py` holding the liveness + stale-reclaim + register-release
body. Re-point the existing `acquire_recovery_lock(results_dir, phase)` at it (public signature
**unchanged** → zero regression to phase callers). The shared core MUST fix the two latent
weaknesses so both the phase lock and the new run lock benefit:

- **R1.1 Atomic acquisition (kills TOCTOU):** replace `lock_path.exists()` → `write_text()`
  (`recovery.py:295,331`) with `fd = os.open(lock_path, os.O_CREAT|os.O_EXCL|os.O_WRONLY, 0o644)`;
  write the JSON payload into that fd and `os.close(fd)`. On `FileExistsError`, run the
  liveness/reclaim branch, then **retry the exclusive create** (bounded, max 3 attempts) so two
  simultaneous reclaimers cannot livelock; if still `EEXIST` after the bound → a live holder exists → refuse.
- **R1.2 Broaden signal release:** register the release handler for **SIGINT and SIGTERM**
  (current code handles only SIGTERM at `recovery.py:335-339`); SIGHUP optional for detached
  `--no-tmux`. Handler releases then restores default disposition and re-raises so exit codes stay correct.
  Keep `atexit` for normal-return / unhandled-exception paths.

## R2 — New release-scoped run lock

Add `acquire_run_lock(results_dir, *, force=False) -> Path` and `release_run_lock(path)` in
`recovery.py` delegating to `_acquire_pid_lock`.

- **R2.1 Lockfile:** `<results_dir>/.recovery-locks/run.lock` (same dir as phase locks, distinct
  filename so the two lock families never collide). JSON payload `{"pid", "starttime", "timestamp", "hostname"}`.
- **R2.2 Live-holder refusal:** if held by a live PID and `force=False`, raise `click.ClickException`
  naming the holder PID + timestamp + remediation ("re-run with `--ignore-run-lock` if that process crashed").
- **R2.3 Stale reclamation (the SIGKILL/SIGSEGV safety net):** atexit/signal handlers do NOT run on
  SIGKILL/SIGSEGV, so a crashed run leaves a dead-PID lock. Acquisition MUST reclaim it: read holder,
  test liveness, if dead `unlink` + retry exclusive create.

## R3 — PID-reuse hazard mitigation (Linux)

`os.kill(pid, 0)` alone reports a recycled PID as "alive" → false lock-held. Store
`starttime` from `/proc/<pid>/stat` field 22 at acquisition; liveness =
`os.kill(pid,0)` succeeds **AND** recorded `starttime` == current `/proc/<pid>/stat` starttime.
Mismatch ⇒ recycled PID ⇒ treat as dead → reclaim. Where `/proc` is absent (non-Linux/minimal
container), `starttime=None` → degrade to PID-only and rely on `--ignore-run-lock`. Corrupt/partial
lockfile JSON ⇒ treat holder as dead → reclaim (must not wedge on a torn write).

## R4 — Integration into `execute_sprint()`

- **R4.1 Acquire site:** in `execute_sprint()` (`executor.py:1586`), **after** `SignalHandler().install()`
  (~`executor.py:1604`) and after the `shutil.which("claude")` preflight (~1602), but **before** the
  orphan-isolation cleanup (~1677) and `execute_preflight_phases` (~1684) — i.e. before any shared-state
  mutation. Acquiring after `SignalHandler.install()` ensures the sprint's coordinated shutdown owns
  signals; the lock's own signal handlers must **chain to** (not clobber) the sprint SignalHandler, OR
  the sprint SignalHandler must call `release_run_lock`. The `finally` block is the authoritative release.
- **R4.2 Release site:** in the existing `finally` block (~`executor.py:2223-2242`) as an isolated
  best-effort step (`try/except`) before `signal_handler.uninstall()`. Covers normal return and the
  `raise SystemExit(_exitcode)` path. atexit/signal handlers are the backstop.
- **R4.3 tmux correctness:** the lock is acquired inside the process that runs `execute_sprint`
  (the tmux-inner worker, or the `--no-tmux` foreground process) — never the launcher shim. A live-holder
  refusal inside tmux MUST convert to a non-zero exit sentinel (existing `_write_exit_sentinel` path,
  ~`executor.py:2246`) so the outer command reports the failure.

## R5 — Override escape hatch

Add `--ignore-run-lock` flag to the `run` Click command (`commands.py`, option block ~233).
Name avoids collision with the existing `--force` on the `kill` command (`commands.py:631`) and the
`--force-fidelity` family. Semantics: reclaim even a **live** holder (loud warning naming the displaced
PID); does NOT kill the other process. Thread it through `SprintConfig` (new `ignore_run_lock: bool = False`)
so it survives the tmux relaunch config reconstruction — NOT as a separate param.

## R6 — Composition with the rerun-tasks recovery lock (no deadlock)

**Rule (must be documented in code):** the run lock is release-scoped and keyed on `results_dir`;
`rerun-tasks` keeps ONLY its phase-scoped recovery lock and runs its inner `execute_sprint` against
`sub_config.release_dir = bundle` (`rerun_tasks.py:1510`), so the inner run lock lands on the **bundle dir**,
not the canonical release dir. The only nesting is `recovery-lock(canonical/phase-N)` ⊃ `run-lock(bundle)`
— disjoint paths, no wait-for cycle. `rerun-tasks` must NOT acquire the canonical run lock. Add an assertion
at the rerun call site that `sub_config.results_dir != config.results_dir` to prevent a future mis-scope.

## R7 — Tests (pytest, UV) in `tests/sprint/test_recovery.py`

Mirror existing style (`test_recovery.py:492`, `test_rerun_tasks.py:502`). Required cases:
1. acquire creates lockfile with pid+payload; 2. live-holder → ClickException naming PID+timestamp;
3. stale dead-PID → reclaim+proceed (`monkeypatch os.kill → ProcessLookupError`); 4. PermissionError → alive;
5. atomic acquisition — `O_EXCL` loser refused, never overwrites (`monkeypatch os.open → FileExistsError`);
6. release on atexit; 7. release on SIGTERM; 8. release on SIGINT (closes weakness b);
9. `--ignore-run-lock`/force bypasses live holder; 10. corrupt JSON tolerated → reclaim;
11. idempotent double-release; 12. run lock + recovery lock coexist (distinct paths, no deadlock);
13. PID-reuse: live PID but starttime mismatch → treated dead → reclaim.

## R8 — Regression guards (must still pass)

`tests/sprint/test_recovery.py` (lock round-trip `:492`), `tests/sprint/test_rerun_tasks.py`
(`:502`,`:525`), `tests/sprint/test_rerun_tasks_failure_modes.py`, `tests/sprint/test_resume.py`
(`:580`,`:603`,`:655`), `tests/sprint/e2e_real/test_e2e_lock_and_retry_cap.py::test_concurrent_lock_aborts_with_pid`
(`:110` — byte-exact phase-lock abort surface MUST be unchanged). Add new assertions in resume/tmux
launch tests that the run lock is acquired at `execute_sprint` entry and released on exit.

## Validation commands

```
uv run pytest tests/sprint/test_recovery.py tests/sprint/test_rerun_tasks.py tests/sprint/test_resume.py tests/sprint/test_rerun_tasks_failure_modes.py -v
uv run pytest tests/sprint/ -v --deselect tests/sprint/e2e_real
```

## Out of scope

- The `preexec_fn=os.setpgrp` → `start_new_session=True` swap (`process.py:190`) — separate, low-risk,
  defense-in-depth; track independently.
- The phase 5/6 task-error root cause (`output_bytes=0` / `turns=0`) — separate troubleshoot.

## Acceptance criteria

1. Second `sprint run` on a live release refuses with a PID-named error.
2. `sprint run` after a crashed run (stale dead-PID lock) reclaims and proceeds.
3. Lock released on normal exit, SIGINT, SIGTERM; reclaimed-on-stale covers SIGKILL/SIGSEGV.
4. `rerun-tasks` and `run` cannot deadlock (disjoint-path proof + assertion).
5. R7 tests pass; R8 regression suite green.
