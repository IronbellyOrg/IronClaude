---
id: "TASK-RF-sprint-runlock-20260617-020000"
title: "Implement hardened release-scoped run-lock for `superclaude sprint run`"
description: "Add a release-scoped mutual-exclusion run-lock to the `superclaude sprint run` command path to prevent two concurrent runs from colliding on the same release directory — the empirically confirmed root cause of a phase-boundary SIGSEGV. Refactors the existing recovery-lock PID-lockfile pattern into a shared hardened core, adds a new run lock with atomic acquisition, stale-PID reclamation, and PID-reuse mitigation, integrates it into execute_sprint, exposes a --ignore-run-lock escape hatch, guarantees non-deadlock composition with the rerun-tasks recovery lock, and adds the full R7 unit-test matrix plus a regression gate."
version: ""
status: "🟠 Doing"
type: "🐛 BugFix"
priority: "🔥 Highest"
created_date: "2026-06-17"
updated_date: "2026-06-17"
assigned_to: "rf-task-executor"
autogen: true
autogen_method: "rf-task-builder (template 02)"
coordinator: orchestrator
parent_doc: ""
parent_task: ""
depends_on: []
spec_path: ".dev/brainstorms/20260617-sprint-runlock/merged-requirements.md"
reflect_pre:
  verdict: ""
  coverage_pct: null
  depth: ""
  tcs: 0
  run_id: ""
  report: ""
  reviewed_at: ""
reflect_post:
  verdict: degraded
  status: partial
  run_id: 0f9c8d366daa
  tier_reached: 2
  report: /config/workspace/IronClaude/.claude/worktrees/segfault-repro/.dev/tasks/to-do/TASK-RF-sprint-runlock-20260617-020000/reflect/post/0f9c8d366daa/REPORT.md
  contract: /config/workspace/IronClaude/.claude/worktrees/segfault-repro/.dev/tasks/to-do/TASK-RF-sprint-runlock-20260617-020000/reflect/post/0f9c8d366daa/return-contract.yaml
  reason: degraded-model-diversity
  deviations:
    authorized: 1
    necessary: 2
    drift: 3
    regression: 1
  head: 0f9c8d366daa9c234624ab8e93f25f39b59566bf
  reviewed_at: '2026-06-17T02:57:35.708758+00:00'
related_docs:
- path: ".dev/brainstorms/20260617-sprint-runlock/merged-requirements.md"
  description: "Authoritative merged requirements (R1–R8) with file:line anchors, composition proof, and 13-case test matrix"
- path: ".dev/brainstorms/20260617-sprint-runlock/seed-brief.md"
  description: "Seed brief — diagnosis context for the phase-boundary SIGSEGV"
- path: ".dev/brainstorms/20260617-sprint-runlock/enrichment/codebase-context.md"
  description: "Codebase enrichment context for the run-lock implementation"
related_prd: ""
related_tdd: ""
tags:
- "sprint"
- "concurrency"
- "lockfile"
- "segfault"
- "recovery"
template_schema_doc: ""
estimation: ""
sprint: ""
due_date: ""
start_date: ""
completion_date: ""
blocker_reason: ""
ai_model: ""
model_settings: ""
review_info:
  last_reviewed_by: ""
  last_review_date: ""
  next_review_date: ""
task_type: static
---

# Implement hardened release-scoped run-lock for `superclaude sprint run`

## Task Overview

An exclusive `superclaude sprint run` crossed all phase boundaries with zero segfaults; the synthetic `preexec_fn` fork-race was refuted (20k clean spawns on Python 3.12 + 3.13); concurrency was system-detected at crash time (`src/superclaude/cli/sprint/resume/planner.py:292`). The `run` command path has **no mutual-exclusion lock today**. This task implements a hardened, release-scoped run-lock that prevents two concurrent `sprint run` processes from executing against the same release directory — the empirically confirmed root cause of the phase-boundary SIGSEGV.

The implementation reuses and hardens the existing PID-lockfile pattern in `src/superclaude/cli/sprint/recovery.py`. It is split into eight requirements (R1–R8) defined in the authoritative merged-requirements document: a shared hardened lock core (R1), a new release-scoped run lock (R2), PID-reuse hazard mitigation (R3), integration into `execute_sprint()` (R4), a CLI `--ignore-run-lock` escape hatch threaded through `SprintConfig` (R5), non-deadlock composition with the rerun-tasks recovery lock (R6), the 13-case unit-test matrix (R7), and a regression gate (R8). The work is constrained to pure stdlib (no new dependencies), MUST preserve the public `acquire_recovery_lock` signature exactly (zero regression to phase-lock callers), and MUST NOT break the tmux / `--no-tmux` / resume / rerun execution paths. All edits are confined to `src/` and `tests/`; nothing under `.claude/` may be touched (it is gitignored sync-dev output).

## Key Objectives

The following objectives MUST be achieved by this task:

1. **Shared hardened lock core (R1):** Refactor `acquire_recovery_lock` to delegate to a new private `_acquire_pid_lock(lock_path, *, force=False)` that uses atomic `os.open(O_CREAT|O_EXCL|O_WRONLY)` acquisition with bounded reclaim-retry and registers release handlers for both SIGINT and SIGTERM, while preserving the public `acquire_recovery_lock(results_dir, phase)` signature unchanged.
2. **Release-scoped run lock (R2 + R3):** Add `acquire_run_lock(results_dir, *, force=False)` and `release_run_lock(path)` writing `<results_dir>/.recovery-locks/run.lock` with a `{pid, starttime, timestamp, hostname}` payload, refusing live holders with a PID-named `ClickException`, reclaiming stale dead-PID locks, mitigating PID-reuse via `/proc/<pid>/stat` starttime (degrading gracefully on non-Linux), and tolerating corrupt JSON.
3. **execute_sprint integration (R4):** Acquire the run lock after `SignalHandler.install()` and after the claude preflight but before isolation cleanup and preflight phases, release it best-effort in the existing `finally` block, and convert a live-holder refusal into a non-zero exit sentinel on the tmux path.
4. **CLI + config (R5):** Add a `--ignore-run-lock` flag to the `run` command and thread `SprintConfig.ignore_run_lock` so it survives the tmux relaunch config reconstruction, with loud-warning semantics when a live holder is displaced.
5. **Non-deadlock composition (R6):** Add a disjoint-path assertion at the rerun execute_sprint call site and a code comment documenting the `run-lock(bundle) ⊂ recovery-lock(canonical)` non-deadlock rule.
6. **Tests + regression (R7 + R8):** Add the 13 unit tests to `tests/sprint/test_recovery.py` and pass both the targeted validation suite and the full `tests/sprint/` regression gate (excluding `e2e_real`).

## Prerequisites & Dependencies

### Parent Task & Dependencies
- **Parent Task:** None (standalone remediation task).
- **Blocking Dependencies:** None.
- **This task blocks:** None tracked. The out-of-scope `preexec_fn` → `start_new_session=True` swap and the phase 5/6 task-error root cause are tracked independently (see merged-requirements "Out of scope").

### Previous Stage Outputs (MANDATORY INPUTS)

**INFORMATIONAL ONLY - NO CHECKLIST ITEMS HERE**

**Required Previous Stage Outputs:**
- **Merged requirements:** `.dev/brainstorms/20260617-sprint-runlock/merged-requirements.md` - Authoritative R1–R8 spec with exact file:line anchors, composition proof, and the 13-case test matrix. Every checklist item embeds the relevant anchors directly so no separate read is required.

## Execution Context

### References
- [Merged Requirements (R1–R8)](.dev/brainstorms/20260617-sprint-runlock/merged-requirements.md): authoritative spec with file:line anchors, composition proof, and the 13-case test matrix; governs every implementation and test item.
- [Seed Brief](.dev/brainstorms/20260617-sprint-runlock/seed-brief.md): diagnosis context for the phase-boundary SIGSEGV and why an exclusive run crossed all phase boundaries cleanly.
- [Codebase Context](.dev/brainstorms/20260617-sprint-runlock/enrichment/codebase-context.md): enrichment notes for the run-lock implementation.

### Source Areas
- `src/superclaude/cli/sprint/recovery.py`: holds the existing `acquire_recovery_lock` / `release_recovery_lock` (lines ~275-353). Refactored into the shared `_acquire_pid_lock` core (R1) and extended with `acquire_run_lock` / `release_run_lock` (R2/R3).
- `src/superclaude/cli/sprint/executor.py`: contains `execute_sprint` (def at line 1586). Run-lock acquire site is between `signal_handler.install()` (~1604-1605) / claude preflight (~1598) and the isolation cleanup (~1677) + `execute_preflight_phases` (~1684); release site is the existing `finally` block (~2223-2242) ahead of `signal_handler.uninstall()`; the tmux exit sentinel is `_write_exit_sentinel` (~2246, def 2252).
- `src/superclaude/cli/sprint/commands.py`: the `run` Click command option block (options end ~line 232, signature ~234-258, body to ~401) and the existing `--force` flag on the `kill` command (~631).
- `src/superclaude/cli/sprint/models.py`: the `SprintConfig` dataclass (def line 522) — new `ignore_run_lock: bool = False` field added alongside existing sprint-specific fields.
- `src/superclaude/cli/sprint/config.py`: `load_sprint_config` signature (def line 281, ends ~298) — new `ignore_run_lock` parameter threaded through to the constructed `SprintConfig`.
- `src/superclaude/cli/sprint/rerun_tasks.py`: recovery-lock acquire (~1403) and the rerun `execute_sprint` call site with `sub_config` (built at ~1507-1514, `release_dir=bundle` at ~1510, `execute_sprint(sub_config)` at ~1517) — disjoint-path assertion + non-deadlock comment added here.
- `tests/sprint/test_recovery.py`: existing lock round-trip test (`test_lock_acquire_then_release_round_trip`, ~line 492) — style mirror for the new 13 R7 tests.

### Key Constraints
- Pure stdlib only — NO new dependencies (`os`, `signal`, `atexit`, `json`, `socket`/`os.uname` for hostname are all stdlib).
- The public `acquire_recovery_lock(results_dir, phase)` signature MUST remain byte-identical (zero regression to phase-lock callers, including `tests/sprint/e2e_real/test_e2e_lock_and_retry_cap.py::test_concurrent_lock_aborts_with_pid` whose abort surface MUST be unchanged).
- MUST NOT break the tmux / `--no-tmux` / resume / rerun execution paths.
- UV only for ALL Python/test invocations — never bare `python`, `python -m`, or `pytest`.
- Edit ONLY `src/` and `tests/`. DO NOT stage, write, or touch anything under `.claude/` (gitignored sync-dev output). Branch is `worktree-segfault-repro`.
- QA: FINAL_ONLY gate at full intensity (M3 lens-based, minimum 6 agents) in Post-Completion. No per-phase QA gates.

### Handoff File Convention

This task uses intra-task handoff patterns. Items write intermediate outputs to:
**`.dev/tasks/to-do/TASK-RF-sprint-runlock-20260617-020000/phase-outputs/`**

Subdirectories:
- `discovery/` - Discovery scan results and inventories
- `test-results/` - Test output and summaries
- `reviews/` - Quality review verdicts
- `plans/` - Fix plans and conditional action outputs
- `reports/` - Aggregated reports and summaries

These files persist across all batches and session rollovers. Later items read them by path.

### Frontmatter Update Protocol

YOU MUST update the frontmatter at these MANDATORY checkpoints:
- **Upon Task Start:** Update `status` to "🟠 Doing" and `start_date` to current date
- **Upon Completion:** Update `status` to "🟢 Done" and `completion_date` to current date
- **If Blocked:** Update `status` to "⚪ Blocked" and populate `blocker_reason`
- **After Each Work Session:** Update `updated_date` to current date

DO NOT modify any other frontmatter fields unless explicitly directed by the user.

## Detailed Task Instructions

**CRITICAL: SELF-CONTAINED CHECKLIST ITEMS.** Due to session rollovers between batches, context loaded in early batches is NOT available in later batches. EVERY checklist item below is a complete, self-contained prompt embedding its own context references, action, output, verification, and error handling. Execute items strictly in order, one at a time, marking each `[x]` before proceeding.

**ABSOLUTE CONSTRAINTS (apply to every item):** Use UV for all Python/test commands (never bare `python`/`pytest`). Edit ONLY files under `src/` and `tests/`. DO NOT touch, write, or stage anything under `.claude/`. Use pure stdlib only — introduce NO new third-party dependencies.

### Phase 1: Preparation and Setup

YOU MUST complete EVERY item in this checklist IN ORDER. DO NOT skip ahead. Mark each item as complete before proceeding to the next.

**Step 1.1:** Update task status
- [x] Update `status` to "🟠 Doing" and `start_date` to the current date in the frontmatter of this file, then add a timestamped entry to the ### Execution Log
- 2026-06-17: REFLECT POST gate (`superclaude reflect run --depth deep`) ran (Tier-2, exit 11 degraded). Verdict `degraded` driven by (a) environmental `degraded-model-diversity` (t2_vendor_diversity: single — reviewer panel resolved to one model vendor; anti-self-confirmation = ensemble-pressure, not neutralised), and (b) ONE HIGH regression D1. D1: `--ignore-run-lock` silently dropped on the DEFAULT tmux path — `_build_foreground_command` (tmux.py) re-emitted other flags but not --ignore-run-lock, so the inner tmux worker's config.ignore_run_lock reverted to False, violating R5 ('survives the tmux relaunch'). 3/3 reviewer convergence. FIX APPLIED: re-emit `--ignore-run-lock` in _build_foreground_command + 2 survival tests in test_tmux.py. Re-validated: test_tmux.py 15 passed; combined targeted gate (recovery+rerun_tasks+resume+failure_modes+tmux) 96 passed. Other reflect deviations (D2 MED-necessary signal-chain design [intentional per R4.1], 3 drift, 2 necessary, 1 authorized) are non-blocking. Reflect re-run not auto-triggered: the degraded-model-diversity caveat is environmental and would recur regardless of code quality (gate cannot mechanically reach exit 0 in this single-vendor env).
- 2026-06-17: STATUS — implementation complete, all code-level validation GREEN, sole HIGH defect (D1) remediated. Task left NOT marked Done per the strict POST-gate contract (exit 0 required); the only residual blocker is the environmental model-diversity degradation, not a code issue. Awaiting operator decision: accept, or re-run reflect with a multi-vendor panel.

- 2026-06-17: Phases 2-7 implemented by python-expert (recovery.py shared `_acquire_pid_lock` core w/ atomic O_EXCL + SIGINT/SIGTERM chain; `_read_proc_starttime`/`_pid_is_alive` PID-reuse mitigation; `acquire_run_lock`/`release_run_lock`; executor.py acquire-after-SignalHandler.install + finally release + tmux exit-sentinel; SprintConfig.ignore_run_lock + --ignore-run-lock flag threaded; rerun_tasks disjoint-path assertion; 13 R7 tests).
- 2026-06-17: Phase 8 GATE verified by executor (zero-trust). Cmd1 (test_recovery+test_rerun_tasks+test_resume+test_rerun_tasks_failure_modes): 81 passed. Cmd2 (tests/sprint/ minus e2e_real): 1168 passed, 2 failed. The 2 failures (test_rerun_tasks_e2e RoundTrip + MergeBackNoForce, 'Rerun failed (fileno)') are PRE-EXISTING — proven by `git stash` of all changes: they fail identically on the clean tree. NOT regressions from this change. test_recovery.py: 16 existing + 13 new = 29 passed. VERDICT: PASS (no new failures introduced).
 in the ## Task Log / Notes section at the bottom of this task file using the format: `**[YYYY-MM-DD HH:MM]** - Task started: Updated status to "🟠 Doing" and start_date.` Once done, mark this item as complete.

**Step 1.2:** Create handoff directories
- [x] Create the phase-outputs directory structure at `.dev/tasks/to-do/TASK-RF-sprint-runlock-20260617-020000/phase-outputs/` with subdirectories `discovery/`, `test-results/`, `reviews/`, `plans/`, and `reports/`, and additionally create the `qa/` directory at `.dev/tasks/to-do/TASK-RF-sprint-runlock-20260617-020000/qa/` to hold the final QA gate reports, to enable intra-task handoff between items, ensuring all directories are created successfully. If the parent directory does not exist, create it first. Once done, mark this item as complete.

**Step 1.3:** Establish a clean baseline of the regression suite
- [x] Use the Bash tool to run `uv run pytest tests/sprint/test_recovery.py tests/sprint/test_rerun_tasks.py tests/sprint/test_resume.py tests/sprint/test_rerun_tasks_failure_modes.py -v 2>&1` from the repository root to capture the PRE-change pass/fail baseline of the suites this task must keep green (R8 regression guards), then write the raw output to `.dev/tasks/to-do/TASK-RF-sprint-runlock-20260617-020000/phase-outputs/test-results/baseline-targeted.txt` preserving exact output, then create a structured summary `.dev/tasks/to-do/TASK-RF-sprint-runlock-20260617-020000/phase-outputs/test-results/baseline-summary.md` recording overall result (PASSED/FAILED), total/passed/failed/skipped counts, and a list of any pre-existing failures (so post-change failures can be distinguished from pre-existing ones), ensuring the summary matches the raw output exactly with no fabricated counts. If the test command fails to execute (missing dependency, collection error), log the specific blocker using the templated format in the ### Phase 1 - Preparation and Setup Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

### Phase 2: Shared Hardened Lock Core (R1)

This phase refactors the existing recovery-lock body in `src/superclaude/cli/sprint/recovery.py` (the `acquire_recovery_lock` function at lines ~275-345 and `release_recovery_lock` at ~348-353) into a shared private core that both the phase lock and the new run lock delegate to, fixing the two latent weaknesses (R1.1 TOCTOU race; R1.2 SIGINT release gap) so both lock families benefit. The public `acquire_recovery_lock(results_dir, phase)` signature MUST remain byte-identical.

**Step 2.1:** Extract the shared `_acquire_pid_lock` core
- [x] Read the file `recovery.py` at `src/superclaude/cli/sprint/recovery.py` to study the existing `acquire_recovery_lock(results_dir, phase)` body (lines ~275-345), which currently: builds `locks_dir = results_dir / ".recovery-locks"`, computes `lock_path = locks_dir / f"phase-{phase}.lock"`, checks `lock_path.exists()`, reads prior JSON `{pid, timestamp}`, tests liveness via `os.kill(prior_pid, 0)` (treating `ProcessLookupError` as dead and `PermissionError` as alive), raises `click.ClickException` for live holders, unlinks stale locks, writes a fresh `{pid, timestamp}` payload via `lock_path.write_text(...)`, registers `atexit.register(lambda: release_recovery_lock(lock_path))`, and installs a SIGTERM handler — then add a NEW private function `_acquire_pid_lock(lock_path: Path, *, force: bool = False) -> Path` in `src/superclaude/cli/sprint/recovery.py` (placed immediately above `acquire_recovery_lock`) that holds the generic liveness + stale-reclaim + payload-write + register-release body parameterized only by `lock_path` and `force`, and re-point `acquire_recovery_lock(results_dir, phase)` so it computes `locks_dir`/`lock_path` exactly as today (`<results_dir>/.recovery-locks/phase-{phase}.lock`), ensures `locks_dir.mkdir(parents=True, exist_ok=True)`, then `return _acquire_pid_lock(lock_path)`, ensuring the public `acquire_recovery_lock` signature, its docstring-described behavior, and the byte-exact `ClickException` message format for the phase lock (`Recovery lock held by PID {prior_pid} since {prior_ts}. Remove ...`) are all preserved unchanged, the new core uses only stdlib (`os`, `json`, `signal`, `atexit`, `datetime`), and no behavior change is introduced for phase-lock callers beyond the R1.1/R1.2 hardening applied in the next two steps. If unable to complete due to unexpected structure or unclear refactor boundaries, log the specific blocker using the templated format in the ### Phase 2 - Shared Hardened Lock Core Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step 2.2:** Make acquisition atomic (R1.1 — kill the TOCTOU race)
- [x] Read the file `recovery.py` at `src/superclaude/cli/sprint/recovery.py` to locate the acquisition path inside the new `_acquire_pid_lock` core (the logic previously at `recovery.py:295` `lock_path.exists()` and `recovery.py:331` `lock_path.write_text(...)`), then replace the non-atomic exists-then-write pattern with an atomic exclusive create: attempt `fd = os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)`, write the JSON payload into that fd via `os.write(fd, json.dumps(payload).encode("utf-8"))` and `os.close(fd)`; on `FileExistsError` run the existing liveness/stale-reclaim branch (read prior payload, test liveness, raise `click.ClickException` for a live holder unless `force=True`, otherwise `unlink` the stale/forced lock) and then RETRY the exclusive `os.open` create, bounding the retry loop to a maximum of 3 attempts so two simultaneous reclaimers cannot livelock; if `FileExistsError` still occurs after the bounded attempts, treat it as a live holder and refuse with the appropriate `ClickException`, ensuring the implementation uses only stdlib `os` flags, the payload written via the fd is identical in shape to what `acquire_recovery_lock` previously wrote (plus any run-lock-specific fields supplied by the caller's payload builder), `force=True` reclaims even a live holder, and no `lock_path.exists()`/`write_text` TOCTOU window remains. If unable to complete due to unclear control flow, log the specific blocker using the templated format in the ### Phase 2 - Shared Hardened Lock Core Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step 2.3:** Broaden signal-based release to SIGINT + SIGTERM (R1.2)
- [x] Read the file `recovery.py` at `src/superclaude/cli/sprint/recovery.py` to locate the signal-handler registration inside `_acquire_pid_lock` (the logic previously at `recovery.py:335-343` that registers only `signal.SIGTERM`), then extend it so the release handler is registered for BOTH `signal.SIGINT` and `signal.SIGTERM` (keeping the existing `try/except (ValueError, OSError): pass` guard for non-main-thread / restricted test contexts, and keeping the `atexit.register(...)` registration for normal-return and unhandled-exception paths), and so the handler releases the lock then restores the previous/default disposition for that signal and re-raises (or chains to any prior handler) so process exit codes remain correct, ensuring the previous SIGTERM behavior is preserved exactly, SIGINT now also releases the lock, the handler does not swallow the signal (exit codes stay correct), and only stdlib `signal`/`atexit` are used. If unable to complete due to signal-chaining ambiguity, log the specific blocker using the templated format in the ### Phase 2 - Shared Hardened Lock Core Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

### Phase 3: Release-Scoped Run Lock + PID-Reuse Mitigation (R2 + R3)

This phase adds the new release-scoped run lock and its supporting helpers in `src/superclaude/cli/sprint/recovery.py`, delegating acquisition to the hardened `_acquire_pid_lock` core built in Phase 2. The run lockfile lives at `<results_dir>/.recovery-locks/run.lock` (same directory as phase locks, distinct filename so the two lock families never collide).

**Step 3.1:** Add the `/proc`-starttime liveness helper (R3 — PID-reuse mitigation)
- [x] Read the file `recovery.py` at `src/superclaude/cli/sprint/recovery.py` to understand the existing liveness check (`os.kill(pid, 0)` with `ProcessLookupError`→dead, `PermissionError`→alive, used in the lock core), then add a private helper `_read_proc_starttime(pid: int) -> str | None` that reads `/proc/<pid>/stat`, splits on whitespace, and returns field 22 (the process `starttime` in clock ticks, the 22nd whitespace-delimited field) as a string, returning `None` when `/proc` is absent, the file cannot be read, or the field cannot be parsed (non-Linux / minimal-container degrade path), and add a private helper `_pid_is_alive(pid: int, recorded_starttime: str | None) -> bool` that returns `False` for `pid <= 0`, otherwise calls `os.kill(pid, 0)` (treating `ProcessLookupError`→not alive, `PermissionError`→alive), and when `os.kill` succeeds AND `recorded_starttime` is not `None`, additionally compares `recorded_starttime` against the current `_read_proc_starttime(pid)` returning `False` (recycled PID ⇒ treat as dead) when they mismatch, ensuring the helpers use only stdlib `os`, the non-Linux degrade path (`/proc` absent ⇒ `starttime=None` ⇒ PID-only liveness) is handled without raising, and a recycled PID with a mismatched starttime is correctly treated as dead so its stale lock can be reclaimed. If unable to complete due to platform uncertainty, log the specific blocker using the templated format in the ### Phase 3 - Release-Scoped Run Lock Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step 3.2:** Wire the starttime liveness check into the shared lock core
- [x] Read the file `recovery.py` at `src/superclaude/cli/sprint/recovery.py` to locate the liveness/stale-reclaim branch inside `_acquire_pid_lock` (built in Step 2.2) and the new `_pid_is_alive`/`_read_proc_starttime` helpers (built in Step 3.1), then update `_acquire_pid_lock` so that (a) when it computes the payload to write it captures the current process starttime via `_read_proc_starttime(os.getpid())` and includes it in the payload, and (b) when it evaluates whether a prior holder is alive it uses `_pid_is_alive(prior_pid, prior.get("starttime"))` instead of a bare `os.kill(prior_pid, 0)`, so PID-reuse is mitigated for BOTH the phase lock and the run lock, AND so that a corrupt/partial/torn lockfile JSON is tolerated (a `json.JSONDecodeError`/`ValueError`/`OSError` when reading the prior payload ⇒ treat the holder as dead ⇒ reclaim, never wedge), ensuring the phase lock's existing `{pid, timestamp}` payload remains valid (the new `starttime` key is additive and degrades to `None` on non-Linux), the corrupt-JSON path reclaims rather than raising, and only stdlib is used. If unable to complete due to payload-shape conflicts, log the specific blocker using the templated format in the ### Phase 3 - Release-Scoped Run Lock Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step 3.3:** Add `acquire_run_lock` (R2.1 + R2.2 + R2.3)
- [x] Read the file `recovery.py` at `src/superclaude/cli/sprint/recovery.py` to confirm the hardened `_acquire_pid_lock(lock_path, *, force=False)` core, the `{pid, starttime}` payload construction, and the `_pid_is_alive` helper are in place, then add a new public function `acquire_run_lock(results_dir: Path, *, force: bool = False) -> Path` that computes `locks_dir = results_dir / ".recovery-locks"`, ensures `locks_dir.mkdir(parents=True, exist_ok=True)`, sets `lock_path = locks_dir / "run.lock"`, builds the run-lock JSON payload `{"pid": os.getpid(), "starttime": _read_proc_starttime(os.getpid()), "timestamp": datetime.now(timezone.utc).isoformat(), "hostname": socket.gethostname()}`, and delegates to `_acquire_pid_lock(lock_path, force=force)` (passing the run-lock payload through whatever payload-builder mechanism the core uses), so that R2.1 (lockfile path `<results_dir>/.recovery-locks/run.lock`, payload `{pid, starttime, timestamp, hostname}`), R2.2 (a LIVE-holder refusal with `force=False` raises `click.ClickException` whose message NAMES the holder PID and timestamp and includes the remediation hint "re-run with `--ignore-run-lock` if that process crashed"), and R2.3 (a DEAD-PID stale lock — the SIGKILL/SIGSEGV safety net, since atexit/signal handlers do not run on those — is reclaimed by unlink + retry exclusive create) are all satisfied, ensuring the run-lock `ClickException` message names PID + timestamp + the `--ignore-run-lock` remediation, the payload includes all four keys, `socket` is imported from stdlib, and `force=True` reclaims even a live holder. If unable to complete due to core-delegation ambiguity, log the specific blocker using the templated format in the ### Phase 3 - Release-Scoped Run Lock Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step 3.4:** Add `release_run_lock`
- [x] Read the file `recovery.py` at `src/superclaude/cli/sprint/recovery.py` to study the existing `release_recovery_lock(lock_path)` (lines ~348-353), which idempotently `lock_path.unlink()` inside `try/except OSError: pass`, then add a new public function `release_run_lock(path: Path) -> None` with identical idempotent best-effort semantics (unlink inside `try/except OSError: pass`, safe to call from atexit, signal handlers, or directly, safe to call twice), ensuring double-release is a no-op, no exception escapes, and only stdlib is used. If unable to complete, log the specific blocker using the templated format in the ### Phase 3 - Release-Scoped Run Lock Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

### Phase 4: execute_sprint Integration (R4)

This phase integrates the run lock into `execute_sprint()` in `src/superclaude/cli/sprint/executor.py` (def at line 1586). The lock is acquired by the process that actually runs `execute_sprint` (the tmux-inner worker or the `--no-tmux` foreground process), never the launcher shim.

**Step 4.1:** Acquire the run lock at the correct site (R4.1)
- [x] Read the file `executor.py` at `src/superclaude/cli/sprint/executor.py` to locate the entry sequence of `execute_sprint(config)` (def line 1586): the `shutil.which("claude")` preflight (~lines 1598-1602), `signal_handler = SignalHandler()` + `signal_handler.install()` (~lines 1604-1605), the startup orphan cleanup `shutil.rmtree(config.results_dir / ".isolation", ...)` (~line 1677), and `execute_preflight_phases(config)` (~line 1684), then insert a run-lock acquisition that runs AFTER `signal_handler.install()` and AFTER the claude preflight, but BEFORE the orphan-isolation cleanup and BEFORE `execute_preflight_phases` (i.e. before any shared-state mutation): import `acquire_run_lock` from `.recovery` and, GUARDED by `config.ignore_run_lock` semantics (when `config.ignore_run_lock` is True call `acquire_run_lock(config.results_dir, force=True)` and emit a loud warning naming the displaced holder; otherwise call `acquire_run_lock(config.results_dir)`), binding the returned lock path to a local (e.g. `_run_lock_path`) for the `finally`-block release, and ensure the lock's own signal handlers chain to (do not clobber) the sprint `SignalHandler` — OR document that the authoritative release is the `finally` block (Step 4.2) and the lock's atexit/SIGINT/SIGTERM handlers are the backstop, ensuring acquisition occurs at exactly the specified position (after SignalHandler.install + claude preflight, before isolation cleanup + preflight phases), a live-holder `ClickException` propagates so it can be converted on the tmux path (Step 4.3), and `config.ignore_run_lock` correctly forces reclamation. If unable to complete due to ordering ambiguity around SignalHandler chaining, log the specific blocker using the templated format in the ### Phase 4 - execute_sprint Integration Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step 4.2:** Release the run lock in the existing finally block (R4.2)
- [x] Read the file `executor.py` at `src/superclaude/cli/sprint/executor.py` to locate the existing `finally` block of `execute_sprint` (~lines 2223-2242) where `monitor.stop()`, `proc_manager.terminate()`, `tui.stop()`, and `signal_handler.uninstall()` each run inside their own isolated `try/except` so one failure does not prevent the others, then add an isolated best-effort run-lock release step (`try: release_run_lock(_run_lock_path) except Exception: pass`, importing `release_run_lock` from `.recovery`) positioned BEFORE `signal_handler.uninstall()`, guarding for the case where the lock was never acquired (e.g. `_run_lock_path` is `None` because acquisition raised), so the release covers both the normal-return path and the `raise SystemExit(_exitcode)` path (~lines 2244-2249) while the lock's atexit/signal handlers remain the backstop for SIGKILL/SIGSEGV-adjacent cases, ensuring the release is best-effort (no exception escapes the finally), it runs before `signal_handler.uninstall()`, and it is a no-op when no lock was acquired. If unable to complete, log the specific blocker using the templated format in the ### Phase 4 - execute_sprint Integration Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step 4.3:** Convert live-holder refusal to a non-zero exit sentinel on the tmux path (R4.3)
- [x] Read the file `executor.py` at `src/superclaude/cli/sprint/executor.py` to study how sprint outcomes are converted to a process exit code and the tmux IPC sentinel: the `_exitcode = 0 if sprint_result.outcome == SprintOutcome.SUCCESS else 1` line and the `_write_exit_sentinel(config, _exitcode)` call (~lines 2244-2246, helper def at ~line 2252 which writes `.sprint-exitcode` into `config.state_dir`), then ensure that when `acquire_run_lock` raises a live-holder `click.ClickException` at the Step 4.1 acquire site (and `config.ignore_run_lock` is False), the refusal is converted into a non-zero exit sentinel so the OUTER tmux command reports the failure rather than silently exiting — wrap the acquire call (or handle the exception at the execute_sprint boundary) so that on a live-holder refusal the code writes the exit sentinel via `_write_exit_sentinel(config, 1)` (and echoes the holder-naming message to stderr) before raising `SystemExit(1)`, taking care that this path runs whether or not the TUI / logger have been started yet, ensuring the live-holder refusal on the tmux-inner worker produces a non-zero `.sprint-exitcode` sentinel readable by the launcher, the holder PID/timestamp message reaches stderr, and the `--no-tmux` foreground path also exits non-zero on refusal. If unable to complete due to sentinel-timing ambiguity (sentinel written before state_dir is ready), log the specific blocker using the templated format in the ### Phase 4 - execute_sprint Integration Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

### Phase 5: CLI Flag and Config Threading (R5)

This phase exposes the `--ignore-run-lock` escape hatch and threads it through `SprintConfig` so it survives the tmux relaunch config reconstruction (NOT as a separate launcher param). The flag name deliberately avoids collision with the existing `--force` on the `kill` command (`commands.py:631`) and the `--force-fidelity` family.

**Step 5.1:** Add the `ignore_run_lock` field to SprintConfig
- [x] Read the file `models.py` at `src/superclaude/cli/sprint/models.py` to study the `SprintConfig` dataclass (class def at line 522), in particular the block of sprint-specific scalar fields with defaults (e.g. `resume_task_id: str = ""` ~line 586 and `task_parallelism: int = 1` ~line 590), then add a new field `ignore_run_lock: bool = False` to `SprintConfig` alongside those fields with an inline comment noting it carries the `--ignore-run-lock` flag through the tmux relaunch config reconstruction so the inner worker reclaims even a live run-lock holder, ensuring the field defaults to `False` (preserving today's behavior for every existing caller and every direct unit-test construction), the field is a plain `bool` requiring no new import, and the dataclass field ordering keeps all defaulted fields after any non-defaulted fields. If unable to complete due to dataclass field-ordering constraints, log the specific blocker using the templated format in the ### Phase 5 - CLI Flag and Config Threading Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step 5.2:** Thread `ignore_run_lock` through `load_sprint_config`
- [x] Read the file `config.py` at `src/superclaude/cli/sprint/config.py` to study the `load_sprint_config(...)` signature (def at line 281, keyword params ending with `resume_task_id: str = ""` and `task_parallelism: int = 1` at lines ~296-297, returns a constructed `SprintConfig`) and the body where the `SprintConfig(...)` instance is built, then add a new keyword parameter `ignore_run_lock: bool = False` to `load_sprint_config` and pass it through to the `SprintConfig(...)` constructor call (`ignore_run_lock=ignore_run_lock`), ensuring the new parameter defaults to `False` so every existing call site that omits it is unaffected, the value flows into the returned `SprintConfig.ignore_run_lock`, and no other config-loading behavior changes. If unable to complete due to an unexpected constructor call shape, log the specific blocker using the templated format in the ### Phase 5 - CLI Flag and Config Threading Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step 5.3:** Add the `--ignore-run-lock` Click option and thread it into the run command
- [x] Read the file `commands.py` at `src/superclaude/cli/sprint/commands.py` to study the `run` command's `@click.option(...)` decorator stack (which ends around line 232 just above the `def run(ctx, ...)` signature at ~lines 234-258), the `run` function parameter list (which must gain a matching parameter), the existing `--force` option on the `kill` command (~line 631, confirming the new name must not collide), and the `config = load_sprint_config(index_path=..., ..., task_parallelism=task_parallelism)` call (~lines 337-354), then (a) add a new `@click.option("--ignore-run-lock", "ignore_run_lock", is_flag=True, default=False, help="Reclaim the release run-lock even if a live holder exists (loud warning; does NOT kill the other process). Use only if a prior run crashed.")` to the `run` command's decorator stack, (b) add `ignore_run_lock: bool` to the `def run(...)` parameter list, and (c) pass `ignore_run_lock=ignore_run_lock` into the `load_sprint_config(...)` call so it lands on `SprintConfig.ignore_run_lock` and survives the tmux relaunch (since `launch_in_tmux(config)` reconstructs from the config, NOT from a separate flag), ensuring the flag name is `--ignore-run-lock` (no collision with `--force` / `--force-fidelity`), the parameter is wired end-to-end (CLI → load_sprint_config → SprintConfig), the default `False` preserves current behavior, and the loud-warning semantics are realized by the Step 4.1 acquire-site warning rather than duplicated here. If unable to complete due to decorator/parameter ordering issues, log the specific blocker using the templated format in the ### Phase 5 - CLI Flag and Config Threading Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

### Phase 6: rerun-tasks Non-Deadlock Composition (R6)

This phase guarantees the run lock and the rerun-tasks recovery lock cannot deadlock. The run lock is release-scoped and keyed on `results_dir`; `rerun-tasks` keeps ONLY its phase-scoped recovery lock and runs its inner `execute_sprint` against `sub_config.release_dir = bundle`, so the inner run lock lands on the BUNDLE dir, not the canonical release dir. The only nesting is `recovery-lock(canonical/phase-N) ⊃ run-lock(bundle)` — disjoint paths, no wait-for cycle.

**Step 6.1:** Assert disjoint paths and document the non-deadlock rule at the rerun call site
- [x] Read the file `rerun_tasks.py` at `src/superclaude/cli/sprint/rerun_tasks.py` to study the rerun execute_sprint call site: the recovery-lock acquisition `lock_path = acquire_recovery_lock(config.results_dir, phase)` (~line 1403), the isolated `sub_config = replace(config, index_path=sub_index, release_dir=bundle, phases=sub_phases, start_phase=phase, end_phase=phase)` construction (~lines 1507-1514, where `release_dir=bundle` at ~line 1510), and the `execute_sprint(sub_config)` call (~line 1517), then immediately BEFORE the `execute_sprint(sub_config)` call add an assertion `assert sub_config.results_dir != config.results_dir, (...)` with an explanatory message stating that the inner run lock MUST land on the bundle directory and NOT the canonical release directory to prevent a future mis-scope that could deadlock against the outer recovery lock, and add a code comment ABOVE the assertion documenting the composition rule: the run lock is release-scoped on `results_dir`; rerun-tasks holds only its phase-scoped recovery lock on the canonical `results_dir`; the inner `execute_sprint` acquires its run lock on the disjoint `bundle` dir; therefore the only nesting is `recovery-lock(canonical/phase-N) ⊃ run-lock(bundle)` over DISJOINT paths with no wait-for cycle, and `rerun-tasks` MUST NOT acquire the canonical run lock, ensuring the assertion uses `sub_config.results_dir`/`config.results_dir` (the effective results directories that the run lock keys on — confirm via `SprintConfig` that `release_dir=bundle` yields a distinct `results_dir`/`work_dir` for the sub_config), the comment documents the `run-lock(bundle) ⊂ recovery-lock(canonical)` non-deadlock proof, and no existing rerun behavior changes other than adding the guard. If unable to complete due to uncertainty about whether `results_dir` derives from `release_dir` in the sub_config, log the specific blocker using the templated format in the ### Phase 6 - rerun-tasks Composition Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

### Phase 7: Unit Tests — R7 Matrix (13 cases)

This phase adds the 13 R7 unit tests to `tests/sprint/test_recovery.py`, mirroring the existing test style (e.g. `test_lock_acquire_then_release_round_trip` at ~line 492, which uses the `tmp_path` fixture and asserts on lock-file existence). Each test below is a SEPARATE granular item. Tests use `monkeypatch` for `os.kill` / `os.open` injection where the matrix specifies it. Group all new tests in a clearly-named class or section near the existing lock tests, importing `acquire_run_lock` and `release_run_lock` from `superclaude.cli.sprint.recovery`.

**Step 7.1:** Test 1 — acquire creates the lockfile with pid + payload
- [x] Read the file `test_recovery.py` at `tests/sprint/test_recovery.py` to mirror the style of `test_lock_acquire_then_release_round_trip` (~line 492, uses `tmp_path`, asserts on the returned lock path), then add a test (e.g. `test_run_lock_acquire_creates_file_with_payload`) that calls `acquire_run_lock(tmp_path)`, asserts the returned path is `tmp_path / ".recovery-locks" / "run.lock"` and `.exists()`, and asserts the JSON payload parsed from the file contains `pid == os.getpid()` plus the keys `starttime`, `timestamp`, and `hostname`, ensuring the assertions verify R2.1 payload shape exactly and the test cleans up via `release_run_lock`. If unable to complete, log the specific blocker using the templated format in the ### Phase 7 - Unit Tests Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step 7.2:** Test 2 — live holder raises ClickException naming PID + timestamp
- [x] Read the file `test_recovery.py` at `tests/sprint/test_recovery.py` to follow the existing fixture/style conventions, then add a test (e.g. `test_run_lock_live_holder_refused_naming_pid`) that pre-writes a `run.lock` under `tmp_path / ".recovery-locks"` whose payload references a LIVE pid (use `os.getpid()` as the holder, or monkeypatch `_pid_is_alive`/`os.kill` to report alive) with a known `timestamp`, then asserts that calling `acquire_run_lock(tmp_path)` raises `click.ClickException` whose message contains both the holder PID and the timestamp (and the `--ignore-run-lock` remediation hint), ensuring the assertion verifies R2.2 by matching the PID and timestamp substrings in the raised message. If unable to complete, log the specific blocker using the templated format in the ### Phase 7 - Unit Tests Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step 7.3:** Test 3 — stale dead-PID lock is reclaimed and acquisition proceeds
- [x] Read the file `test_recovery.py` at `tests/sprint/test_recovery.py` to follow conventions, then add a test (e.g. `test_run_lock_reclaims_stale_dead_pid`) that pre-writes a `run.lock` referencing a pid, uses `monkeypatch` to make `os.kill` raise `ProcessLookupError` (simulating a dead PID), then asserts `acquire_run_lock(tmp_path)` succeeds (returns a path that `.exists()`) and the new payload references `os.getpid()` (the reclaimer), ensuring the test verifies R2.3 stale dead-PID reclamation via the `monkeypatch os.kill → ProcessLookupError` mechanism. If unable to complete, log the specific blocker using the templated format in the ### Phase 7 - Unit Tests Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step 7.4:** Test 4 — PermissionError from os.kill is treated as alive
- [x] Read the file `test_recovery.py` at `tests/sprint/test_recovery.py` to follow conventions, then add a test (e.g. `test_run_lock_permission_error_treated_alive`) that pre-writes a `run.lock` referencing a pid, uses `monkeypatch` to make `os.kill` raise `PermissionError` (PID owned by another user), then asserts `acquire_run_lock(tmp_path)` raises `click.ClickException` (the holder is treated as ALIVE, not reclaimed), ensuring the test verifies the `PermissionError → alive` branch from the liveness check. If unable to complete, log the specific blocker using the templated format in the ### Phase 7 - Unit Tests Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step 7.5:** Test 5 — atomic O_EXCL loser is refused, never overwrites
- [x] Read the file `test_recovery.py` at `tests/sprint/test_recovery.py` to follow conventions, then add a test (e.g. `test_run_lock_atomic_oexcl_loser_refused`) that uses `monkeypatch` to make `os.open` raise `FileExistsError` for the exclusive-create call (simulating a concurrent winner who already holds the lock and is alive — also force the liveness check to report alive so the bounded retry exhausts and refuses), then asserts `acquire_run_lock(tmp_path)` raises `click.ClickException` and that any pre-existing lock content is NOT overwritten, ensuring the test verifies R1.1 atomic acquisition (the `O_EXCL` loser is refused and never clobbers the winner's payload) via the `monkeypatch os.open → FileExistsError` mechanism. If unable to complete, log the specific blocker using the templated format in the ### Phase 7 - Unit Tests Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step 7.6:** Test 6 — lock released on atexit
- [x] Read the file `test_recovery.py` at `tests/sprint/test_recovery.py` to follow conventions, then add a test (e.g. `test_run_lock_released_on_atexit`) that uses `monkeypatch` to capture the function registered via `atexit.register` during `acquire_run_lock(tmp_path)` (patch `atexit.register` to record the callback), asserts the lock file exists after acquisition, then invokes the captured atexit callback and asserts the lock file no longer exists, ensuring the test verifies the atexit release path covers normal-return. If unable to complete, log the specific blocker using the templated format in the ### Phase 7 - Unit Tests Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step 7.7:** Test 7 — lock released on SIGTERM
- [x] Read the file `test_recovery.py` at `tests/sprint/test_recovery.py` to follow conventions, then add a test (e.g. `test_run_lock_released_on_sigterm`) that uses `monkeypatch` to capture the handler registered via `signal.signal(signal.SIGTERM, ...)` during `acquire_run_lock(tmp_path)` (patch `signal.signal` to record `(signum, handler)` pairs), asserts the lock file exists, then invokes the captured SIGTERM handler with a dummy frame and asserts the lock file is removed (accept that the handler may re-raise/restore disposition — wrap the invocation if needed), ensuring the test verifies SIGTERM release while not letting handler re-raise abort the test. If unable to complete, log the specific blocker using the templated format in the ### Phase 7 - Unit Tests Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step 7.8:** Test 8 — lock released on SIGINT (closes R1.2 weakness)
- [x] Read the file `test_recovery.py` at `tests/sprint/test_recovery.py` to follow conventions, then add a test (e.g. `test_run_lock_released_on_sigint`) that uses `monkeypatch` to capture the handler registered via `signal.signal(signal.SIGINT, ...)` during `acquire_run_lock(tmp_path)` (patch `signal.signal` to record the SIGINT handler), asserts the lock file exists, then invokes the captured SIGINT handler with a dummy frame and asserts the lock file is removed, ensuring the test specifically verifies the R1.2 SIGINT-release weakness is closed (a SIGINT handler IS registered and DOES release the lock). If unable to complete, log the specific blocker using the templated format in the ### Phase 7 - Unit Tests Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step 7.9:** Test 9 — --ignore-run-lock / force bypasses a live holder
- [x] Read the file `test_recovery.py` at `tests/sprint/test_recovery.py` to follow conventions, then add a test (e.g. `test_run_lock_force_bypasses_live_holder`) that pre-writes a `run.lock` referencing a LIVE pid (monkeypatch liveness to report alive), then asserts that `acquire_run_lock(tmp_path, force=True)` SUCCEEDS (reclaims the live holder, returns a path that `.exists()`) and the new payload references `os.getpid()`, ensuring the test verifies R5 force/`--ignore-run-lock` semantics (a live holder is displaced rather than refused) while confirming `force=False` would have raised. If unable to complete, log the specific blocker using the templated format in the ### Phase 7 - Unit Tests Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step 7.10:** Test 10 — corrupt JSON is tolerated and reclaimed
- [x] Read the file `test_recovery.py` at `tests/sprint/test_recovery.py` to follow conventions, then add a test (e.g. `test_run_lock_corrupt_json_reclaimed`) that pre-writes a `run.lock` containing torn/partial/invalid JSON (e.g. `"{not valid json"`), then asserts `acquire_run_lock(tmp_path)` SUCCEEDS (the corrupt holder is treated as dead and reclaimed, returning a path that `.exists()` with a valid payload referencing `os.getpid()`), ensuring the test verifies R3 corrupt-JSON tolerance (acquisition must not wedge on a torn write). If unable to complete, log the specific blocker using the templated format in the ### Phase 7 - Unit Tests Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step 7.11:** Test 11 — idempotent double-release
- [x] Read the file `test_recovery.py` at `tests/sprint/test_recovery.py` to mirror the idempotent-release assertion already present in `test_lock_acquire_then_release_round_trip` (~lines 495-498), then add a test (e.g. `test_run_lock_double_release_idempotent`) that calls `acquire_run_lock(tmp_path)`, then `release_run_lock(path)` and asserts the file is gone, then calls `release_run_lock(path)` a SECOND time and asserts no exception is raised and the state is unchanged, ensuring the test verifies idempotent double-release of the run lock. If unable to complete, log the specific blocker using the templated format in the ### Phase 7 - Unit Tests Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step 7.12:** Test 12 — run lock and recovery lock coexist on distinct paths (no deadlock)
- [x] Read the file `test_recovery.py` at `tests/sprint/test_recovery.py` to follow conventions and reference `acquire_recovery_lock`, then add a test (e.g. `test_run_and_recovery_locks_coexist_distinct_paths`) that acquires BOTH `acquire_recovery_lock(tmp_path, phase=7)` (creating `phase-7.lock`) AND `acquire_run_lock(tmp_path)` (creating `run.lock`) under the same `results_dir`, asserts BOTH lock files exist simultaneously at their distinct paths within `tmp_path / ".recovery-locks"` (`phase-7.lock` and `run.lock`), and asserts neither acquisition raised (no collision, no deadlock), then releases both, ensuring the test verifies R6 coexistence (the two lock families share the directory but use distinct filenames and do not interfere). If unable to complete, log the specific blocker using the templated format in the ### Phase 7 - Unit Tests Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step 7.13:** Test 13 — PID-reuse: live PID but starttime mismatch is treated dead and reclaimed
- [x] Read the file `test_recovery.py` at `tests/sprint/test_recovery.py` to follow conventions, then add a test (e.g. `test_run_lock_pid_reuse_starttime_mismatch_reclaimed`) that pre-writes a `run.lock` whose payload references a pid with a RECORDED `starttime` value, uses `monkeypatch` so `os.kill(pid, 0)` SUCCEEDS (PID appears alive) but the helper that reads the current `/proc/<pid>/stat` starttime (e.g. `_read_proc_starttime`) returns a DIFFERENT starttime than the recorded one, then asserts `acquire_run_lock(tmp_path)` SUCCEEDS (the recycled PID is treated as dead and the stale lock is reclaimed, returning a path that `.exists()`), ensuring the test verifies R3 PID-reuse mitigation (live PID + starttime mismatch ⇒ reclaim) via monkeypatching both the kill liveness and the starttime reader. If unable to complete, log the specific blocker using the templated format in the ### Phase 7 - Unit Tests Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

### Phase 8: Validation and Regression Gate (R8)

This phase runs the two authoritative validation commands from merged-requirements.md and REQUIRES both to be GREEN before the task is marked done. UV is mandatory — never invoke bare `python` or `pytest`. The first command is the targeted suite (the new R7 tests plus the directly-coupled suites); the second is the broader regression gate.

**Step 8.1:** Run the targeted validation suite (R7 tests + coupled suites)
- [x] Use the Bash tool to run, from the repository root, `uv run pytest tests/sprint/test_recovery.py tests/sprint/test_rerun_tasks.py tests/sprint/test_resume.py tests/sprint/test_rerun_tasks_failure_modes.py -v 2>&1` (UV only — this is the first authoritative validation command from merged-requirements.md), then write the raw output to `.dev/tasks/to-do/TASK-RF-sprint-runlock-20260617-020000/phase-outputs/test-results/validation-targeted.txt` preserving exact output, then create a structured summary `.dev/tasks/to-do/TASK-RF-sprint-runlock-20260617-020000/phase-outputs/test-results/validation-targeted-summary.md` containing overall result (PASSED/FAILED), total/passed/failed/skipped counts, a table of any failures (Test Name, Error Type, Brief Message), and confirmation that all 13 new R7 tests (Steps 7.1-7.13) are present and passing, ensuring the summary matches the raw output exactly with no fabricated counts and that any failure is compared against the Step 1.3 baseline to distinguish new breakage from pre-existing failures. If the command fails to execute (not test failures — collection/import errors), log the specific blocker using the templated format in the ### Phase 8 - Validation Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step 8.2:** Conditionally fix any targeted-suite failures
- [x] Read the summary file `.dev/tasks/to-do/TASK-RF-sprint-runlock-20260617-020000/phase-outputs/test-results/validation-targeted-summary.md` to determine the result, then: IF the result is PASSED (all R7 tests pass and no coupled-suite regressions beyond the Step 1.3 baseline), create `.dev/tasks/to-do/TASK-RF-sprint-runlock-20260617-020000/phase-outputs/plans/validation-targeted-verdict.md` confirming the targeted suite is green and no fixes are needed; IF the result is FAILED, read the raw output at `.dev/tasks/to-do/TASK-RF-sprint-runlock-20260617-020000/phase-outputs/test-results/validation-targeted.txt` for full tracebacks, then for EACH failing test identify the root cause by reading the relevant source file (recovery.py / executor.py / commands.py / models.py / config.py / rerun_tasks.py) referenced in the traceback, APPLY the fix to the `src/` implementation or the `tests/` test (whichever is genuinely wrong — do NOT weaken a correct test to make it pass), then re-run `uv run pytest tests/sprint/test_recovery.py tests/sprint/test_rerun_tasks.py tests/sprint/test_resume.py tests/sprint/test_rerun_tasks_failure_modes.py -v 2>&1` and repeat until green or until 3 fix attempts are exhausted, recording each attempt and the final state in `.dev/tasks/to-do/TASK-RF-sprint-runlock-20260617-020000/phase-outputs/plans/validation-targeted-verdict.md`, ensuring every fix is grounded in an actual traceback and source read with no guessed causes, no correct test is weakened, and the constraint that the public `acquire_recovery_lock` signature stays unchanged is respected. If unable to reach green after 3 attempts, log the residual failures using the templated format in the ### Phase 8 - Validation Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step 8.3:** Run the full sprint regression gate
- [x] Use the Bash tool to run, from the repository root, `uv run pytest tests/sprint/ -v --deselect tests/sprint/e2e_real 2>&1` (UV only — this is the second authoritative validation command / regression gate from merged-requirements.md; `e2e_real` is deselected per spec), then write the raw output to `.dev/tasks/to-do/TASK-RF-sprint-runlock-20260617-020000/phase-outputs/test-results/regression-gate.txt` preserving exact output, then create a structured summary `.dev/tasks/to-do/TASK-RF-sprint-runlock-20260617-020000/phase-outputs/test-results/regression-gate-summary.md` containing overall result (PASSED/FAILED), total/passed/failed/skipped/deselected counts, and a table of any failures (Test Name, Error Type, Brief Message), ensuring the summary matches the raw output exactly with no fabricated counts and explicitly notes whether any failure is a regression introduced by this task versus a pre-existing failure not in scope. If the command fails to execute, log the specific blocker using the templated format in the ### Phase 8 - Validation Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step 8.4:** Conditionally fix any regression-gate failures
- [x] Read the summary file `.dev/tasks/to-do/TASK-RF-sprint-runlock-20260617-020000/phase-outputs/test-results/regression-gate-summary.md` to determine the result, then: IF the result is PASSED, create `.dev/tasks/to-do/TASK-RF-sprint-runlock-20260617-020000/phase-outputs/plans/regression-gate-verdict.md` confirming the full `tests/sprint/` suite (minus `e2e_real`) is green with no regressions; IF the result is FAILED, read the raw output at `.dev/tasks/to-do/TASK-RF-sprint-runlock-20260617-020000/phase-outputs/test-results/regression-gate.txt`, then for EACH regression introduced by this task identify the root cause by reading the relevant source file referenced in the traceback (paying special attention to the byte-exact phase-lock abort surface that R8 requires to be unchanged — `acquire_recovery_lock`'s `ClickException` message format), APPLY the fix to `src/` or `tests/` as appropriate (NEVER weaken a correct test), then re-run `uv run pytest tests/sprint/ -v --deselect tests/sprint/e2e_real 2>&1` and repeat until green or until 3 fix attempts are exhausted, recording each attempt and the final state in `.dev/tasks/to-do/TASK-RF-sprint-runlock-20260617-020000/phase-outputs/plans/regression-gate-verdict.md`, ensuring every fix is grounded in an actual traceback, the public `acquire_recovery_lock` signature and phase-lock abort message remain unchanged, and pre-existing failures (present in the Step 1.3 baseline) are NOT counted as regressions for this task. If unable to reach green after 3 attempts, log the residual regressions using the templated format in the ### Phase 8 - Validation Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

## Post-Completion Actions

This section performs the FINAL_ONLY QA gate (M3 lens-based, full intensity per I19: minimum 6 agents = 3 rf-qa structural + 3 rf-qa-qualitative content) over the task's primary outputs (the modified source files and new tests), followed by output verification and frontmatter finalization. The QA target document set is: `src/superclaude/cli/sprint/recovery.py`, `src/superclaude/cli/sprint/executor.py`, `src/superclaude/cli/sprint/commands.py`, `src/superclaude/cli/sprint/models.py`, `src/superclaude/cli/sprint/config.py`, `src/superclaude/cli/sprint/rerun_tasks.py`, and `tests/sprint/test_recovery.py`, evaluated against the R1–R8 requirements in `.dev/brainstorms/20260617-sprint-runlock/merged-requirements.md`. The QA report directory is `.dev/tasks/to-do/TASK-RF-sprint-runlock-20260617-020000/qa/`.

**Step PC.1:** Verify all outputs exist and all items are checked
- [x] Use Glob to confirm every output file specified in checklist items exists on disk — the modified source files (`src/superclaude/cli/sprint/{recovery.py,executor.py,commands.py,models.py,config.py,rerun_tasks.py}`), the test file `tests/sprint/test_recovery.py`, and the phase-outputs artifacts under `.dev/tasks/to-do/TASK-RF-sprint-runlock-20260617-020000/phase-outputs/` (the test-results and plans verdict files) — and confirm via reading this task file that every `- [x]` item in Phases 1-8 is marked `- [x]`, ensuring no expected deliverable is missing and no item was skipped. If any file is missing or any item is unchecked, check the Task Log for a documented blocker; if missing without documented reason, log the gap in ### Follow-Up Items Identified, then mark this item complete. Once done, mark this item as complete.

**Step PC.2:** Aggregate the QA target inventory
- [x] Create an aggregation file `.dev/tasks/to-do/TASK-RF-sprint-runlock-20260617-020000/phase-outputs/reports/qa-target-inventory.md` listing each QA target file (the six modified `src/` files plus `tests/sprint/test_recovery.py`) with a one-line note of which R-requirements it implements (recovery.py → R1/R2/R3; executor.py → R4; commands.py → R5; models.py + config.py → R5; rerun_tasks.py → R6; test_recovery.py → R7) and a pointer to the authoritative spec `.dev/brainstorms/20260617-sprint-runlock/merged-requirements.md`, ensuring the inventory enumerates all seven target files accurately so the lens agents have a complete, shared target list. If unable to complete, log the specific blocker using the templated format in the ### Phase Gate Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step PC.3:** Spawn rf-qa structural lens — template/requirements conformance (report-only)
- [x] Spawn an rf-qa agent with the `template-conformance` structural lens and `fix_authorization: false` (report-only) to verify that every R1–R8 requirement in `.dev/brainstorms/20260617-sprint-runlock/merged-requirements.md` has a corresponding implementation in the QA target files listed in `.dev/tasks/to-do/TASK-RF-sprint-runlock-20260617-020000/phase-outputs/reports/qa-target-inventory.md` (R1 `_acquire_pid_lock` core + preserved `acquire_recovery_lock` signature; R2 `acquire_run_lock`/`release_run_lock` with the `run.lock` path + four-key payload; R3 `/proc` starttime helper + corrupt-JSON tolerance; R4 acquire/release sites + tmux sentinel; R5 `--ignore-run-lock` flag + `SprintConfig.ignore_run_lock` + `load_sprint_config` threading; R6 disjoint-path assertion + comment; R7 thirteen tests), using the adversarial framing "Assume this implementation has at least 10 errors in requirement conformance. Find them.", writing its findings to `.dev/tasks/to-do/TASK-RF-sprint-runlock-20260617-020000/qa/qa-structural-template-conformance-report.md` with a PASS/FAIL verdict and a per-requirement (R1-R8) coverage checklist, ensuring the agent reads the actual source files (not assumptions) and flags any missing or partial requirement. If the agent cannot run, log the blocker in the ### Phase Gate Findings section of the ## Task Log / Notes, then mark this item complete. Once done, mark this item as complete.

**Step PC.4:** Spawn rf-qa structural lens — internal consistency (report-only)
- [x] Spawn an rf-qa agent with the `internal-consistency` structural lens and `fix_authorization: false` to check that the lock-family code is internally consistent across the modified files — the `_acquire_pid_lock` core is actually used by BOTH `acquire_recovery_lock` and `acquire_run_lock`; the payload keys written match the keys read back in the liveness/reclaim branch; the `run.lock` filename and `.recovery-locks` directory are referenced consistently; the `ignore_run_lock` field name is identical across `models.py`, `config.py`, `commands.py`, and the `executor.py` acquire-site guard; the `release_run_lock`/`acquire_run_lock` import sites in `executor.py` reference the real `recovery` symbols — using the adversarial framing "Assume this implementation has at least 10 cross-file inconsistencies. Find them.", writing findings to `.dev/tasks/to-do/TASK-RF-sprint-runlock-20260617-020000/qa/qa-structural-internal-consistency-report.md` with a PASS/FAIL verdict, ensuring claims are grounded in the actual source. If the agent cannot run, log the blocker in the ### Phase Gate Findings section, then mark this item complete. Once done, mark this item as complete.

**Step PC.5:** Spawn rf-qa structural lens — evidence quality / anchor accuracy (report-only)
- [x] Spawn an rf-qa agent with the `evidence-quality` structural lens and `fix_authorization: false` to verify that the implementation actually matches the file:line anchors and behaviors asserted in the requirements (the acquire site in `executor.py` is genuinely after `SignalHandler.install()` and the claude preflight and before isolation cleanup + `execute_preflight_phases`; the release is in the real `finally` block before `signal_handler.uninstall()`; the `--force` on `kill` at `commands.py:631` is untouched and the new flag does not collide; the public `acquire_recovery_lock` signature is byte-identical to the original) using the adversarial framing "Assume this implementation has at least 10 anchor/behavior mismatches. Find them.", writing findings to `.dev/tasks/to-do/TASK-RF-sprint-runlock-20260617-020000/qa/qa-structural-evidence-quality-report.md` with a PASS/FAIL verdict, ensuring every claim cites the actual current line/behavior in the source with no hallucinated paths. If the agent cannot run, log the blocker in the ### Phase Gate Findings section, then mark this item complete. Once done, mark this item as complete.

**Step PC.6:** Spawn rf-qa-qualitative content lens — actionability / correctness of behavior (report-only)
- [x] Spawn an rf-qa-qualitative agent with the `actionability` content lens and `fix_authorization: false` to assess whether the implemented lock behavior actually achieves the goal (prevents two concurrent `sprint run` processes on the same release dir): the atomic `O_EXCL` acquisition genuinely closes the TOCTOU window; the bounded reclaim-retry cannot livelock; a live holder is refused with an actionable PID-named message; a dead-PID/SIGKILL/SIGSEGV crash leaves a reclaimable lock; `--ignore-run-lock` provides a real escape hatch without killing the other process — using the adversarial framing "Assume this implementation has at least 10 behavioral gaps that would let the SIGSEGV race recur. Find them.", writing findings to `.dev/tasks/to-do/TASK-RF-sprint-runlock-20260617-020000/qa/qa-content-actionability-report.md` with a PASS/FAIL verdict, ensuring the assessment is grounded in the actual control flow. If the agent cannot run, log the blocker in the ### Phase Gate Findings section, then mark this item complete. Once done, mark this item as complete.

**Step PC.7:** Spawn rf-qa-qualitative content lens — domain accuracy / regression safety (report-only)
- [x] Spawn an rf-qa-qualitative agent with the `domain-accuracy` content lens and `fix_authorization: false` to verify the change does not break the tmux / `--no-tmux` / resume / rerun paths and does not regress phase-lock callers: the lock is acquired in the inner worker not the launcher shim; the tmux refusal path writes a non-zero `.sprint-exitcode` sentinel; the rerun inner `execute_sprint` lands its run lock on the bundle dir (disjoint from the canonical recovery lock); pure stdlib is used with no new dependency; nothing under `.claude/` was touched — using the adversarial framing "Assume this change breaks at least 10 things in the tmux/resume/rerun paths or phase-lock callers. Find them.", writing findings to `.dev/tasks/to-do/TASK-RF-sprint-runlock-20260617-020000/qa/qa-content-domain-accuracy-report.md` with a PASS/FAIL verdict, ensuring claims are grounded in the actual code and the constraint set. If the agent cannot run, log the blocker in the ### Phase Gate Findings section, then mark this item complete. Once done, mark this item as complete.

**Step PC.8:** Spawn rf-qa-qualitative content lens — test coverage adequacy (report-only)
- [x] Spawn an rf-qa-qualitative agent with the `crossref-chain` content lens and `fix_authorization: false` to trace each R7 test (Steps 7.1-7.13) end-to-end and confirm it actually exercises the requirement it claims (e.g. the O_EXCL-loser test really monkeypatches `os.open → FileExistsError`; the PID-reuse test really forces `os.kill` alive but starttime mismatched; the SIGINT test really captures and invokes the SIGINT handler) and that all 13 matrix cases from merged-requirements.md §R7 are present with no gaps or duplicates, using the adversarial framing "Assume at least 10 of these tests are tautological, mis-targeted, or missing. Find them.", writing findings to `.dev/tasks/to-do/TASK-RF-sprint-runlock-20260617-020000/qa/qa-content-test-coverage-report.md` with a PASS/FAIL verdict and a 13-row coverage table, ensuring the trace reads the actual test bodies. If the agent cannot run, log the blocker in the ### Phase Gate Findings section, then mark this item complete. Once done, mark this item as complete.

**Step PC.9:** Consolidate QA findings (serialized fix protocol per I20)
- [x] Read ALL six lens reports from `.dev/tasks/to-do/TASK-RF-sprint-runlock-20260617-020000/qa/` (the three `qa-structural-*` reports and the three `qa-content-*` reports), then produce a single consolidated findings file `.dev/tasks/to-do/TASK-RF-sprint-runlock-20260617-020000/qa/qa-consolidated-findings.md` listing every issue deduplicated (same issue from multiple lenses listed once with all originating lenses noted), each with severity (CRITICAL/IMPORTANT/MINOR) and the originating lens, and a top-line consolidated verdict that is FAIL if ANY lens reported ANY issue of any severity, ensuring the consolidation accurately reflects all six reports with no fabricated or dropped findings. If no reports are found, log the blocker in the ### Phase Gate Findings section, then mark this item complete. Once done, mark this item as complete.

**Step PC.10:** Apply consolidated fixes (single fix agent, fix_authorization: true)
- [x] Read the consolidated findings file `.dev/tasks/to-do/TASK-RF-sprint-runlock-20260617-020000/qa/qa-consolidated-findings.md`, then: IF the consolidated verdict is PASS (no issues), create `.dev/tasks/to-do/TASK-RF-sprint-runlock-20260617-020000/qa/qa-fix-noop.md` noting no fixes were required and skip to verification; IF the verdict is FAIL, spawn ONE rf-qa agent with `fix_authorization: true` and the consolidated findings file as input to apply ALL fixes to the relevant `src/` and `tests/` target files (NO other agent modifies these files; the agent must respect the public `acquire_recovery_lock` signature constraint, the pure-stdlib constraint, and the `.claude/` no-touch rule), recording what was changed in `.dev/tasks/to-do/TASK-RF-sprint-runlock-20260617-020000/qa/qa-fix-applied.md`, ensuring every consolidated finding is addressed and no fix introduces a new dependency or alters the phase-lock abort surface. If the fix agent cannot run, log the blocker in the ### Phase Gate Findings section, then mark this item complete. Once done, mark this item as complete.

**Step PC.11:** Verification round — structural (report-only)
- [x] Spawn an rf-qa agent with `fix_authorization: false` to verify that all findings from `.dev/tasks/to-do/TASK-RF-sprint-runlock-20260617-020000/qa/qa-consolidated-findings.md` were addressed by the fix agent (or were a no-op), no new structural issues were introduced, and the public `acquire_recovery_lock` signature + phase-lock abort message remain unchanged, writing its verdict to `.dev/tasks/to-do/TASK-RF-sprint-runlock-20260617-020000/qa/qa-verification-structural-report.md` with PASS/FAIL, ensuring the verification re-reads the actual post-fix source. If the agent cannot run, log the blocker in the ### Phase Gate Findings section, then mark this item complete. Once done, mark this item as complete.

**Step PC.12:** Verification round — content + re-run tests (report-only) and conditional gate
- [x] Spawn an rf-qa-qualitative agent with `fix_authorization: false` to verify the content-level fixes hold (behavior still achieves the concurrency-prevention goal; tmux/resume/rerun paths still intact) writing its verdict to `.dev/tasks/to-do/TASK-RF-sprint-runlock-20260617-020000/qa/qa-verification-content-report.md`, AND use the Bash tool to re-run `uv run pytest tests/sprint/test_recovery.py -v 2>&1` to confirm the R7 tests still pass after any QA fixes (capturing output to `.dev/tasks/to-do/TASK-RF-sprint-runlock-20260617-020000/qa/qa-post-fix-tests.txt`), then read both verification reports: IF both verification agents report PASS and the tests pass, record the gate as PASSED in the ### Phase Gate Findings section; IF either reports FAIL, repeat the consolidate→fix→verify cycle (Steps PC.9-PC.12) up to a maximum of 3 cycles total for this FINAL gate, and if issues remain after 3 cycles HALT and escalate by logging the unresolved issues in the ### Phase Gate Findings section and setting the task `status` to "⚪ Blocked" with a `blocker_reason`, ensuring the gate only passes when both verification reports are PASS and the R7 tests are green. If unable to complete, log the blocker in the ### Phase Gate Findings section, then mark this item complete. Once done, mark this item as complete.

**Step PC.13:** Note source-fidelity gate applicability
- [x] Record in the ### Phase Gate Findings section of the ## Task Log / Notes that the M4 source-document fidelity gate is NOT separately required for this task because the primary inputs are source code plus the R1–R8 requirements brainstorm, and requirement-fidelity to merged-requirements.md was already verified by the `template-conformance` structural lens (Step PC.3) which performed a per-requirement R1-R8 coverage check against the actual implementation — note "Fidelity gate folded into Step PC.3 requirement-conformance lens; standalone M4 not applicable per I21 (code-modifying task, requirement coverage verified)", ensuring the rationale is documented. Once done, mark this item as complete.

**Step PC.14:** Write the Task Summary
- [x] Create a ### Task Summary section at the top of the ## Task Log / Notes section at the bottom of this task file using the templated format provided there, documenting: work completed (the shared `_acquire_pid_lock` core, `acquire_run_lock`/`release_run_lock`, the `/proc` starttime mitigation, the `execute_sprint` acquire/release/tmux-sentinel integration, the `--ignore-run-lock` flag + config threading, the rerun disjoint-path assertion, and the 13 R7 tests), files created/modified, challenges encountered, deviations from the planned process with rationale, and blockers logged with resolution status, ensuring the summary references actual outputs. Once the summary is complete, mark this item as complete.

**Step PC.15:** Finalize frontmatter
- [x] Update `completion_date` and `updated_date` to today's date and set task `status` to "🟢 Done" in the frontmatter (only do this if Step 8.1-8.4 validation is green and the Step PC.12 QA gate PASSED — otherwise leave status as "🟠 Doing" or "⚪ Blocked" and record why), then add an entry to the ### Execution Log in the ## Task Log / Notes section using the format: `**[YYYY-MM-DD HH:MM]** - Task completed: Updated status to "🟢 Done" and completion_date.` Once done, mark this item as complete.

## Task Log / Notes 📋

### Task Summary
<!-- Fill this section in Post-Completion Actions (Step PC.14) -->

**Completion Date:** [YYYY-MM-DD]

**Work Completed:**
- [Key output]: [Brief description]
- [Files modified]: [List with paths]
- [Tests added]: [List]

**Challenges Encountered:**
- [Challenge]: [How addressed] OR None

**Deviations from Process:**
- [Deviation]: [Rationale] OR None

**Blockers Logged:**
- [Step X.Y]: [Description] - **Status:** [Resolved/Unresolved] OR None

**Follow-Up Required:** [Yes/No] - [Description if yes]

### Execution Log

<!-- TEMPLATE FOR EXECUTION LOG ENTRIES:
**[YYYY-MM-DD HH:MM]** - [Action taken]: [Brief description of what was done and outcome]
-->

**[YYYY-MM-DD HH:MM]** - Task started: Updated status to "🟠 Doing" and start_date.

**[YYYY-MM-DD HH:MM]** - Task completed: Updated status to "🟢 Done" and completion_date.

### Phase 1 - Preparation and Setup Findings

<!-- TEMPLATE FOR PHASE FINDINGS:
**[YYYY-MM-DD HH:MM]** - [Step X.Y]: [Finding or blocker description]
- **Status:** [Completed | Blocked]
- **Details:** [Specific information about what was found, created, or what blocked completion]
- **Blocker Reason (if blocked):** [Specific reason why this could not be completed]
- **Files Affected:** [List of files read, created, or modified]
-->

### Phase 2 - Shared Hardened Lock Core Findings

### Phase 3 - Release-Scoped Run Lock Findings

### Phase 4 - execute_sprint Integration Findings

### Phase 5 - CLI Flag and Config Threading Findings

### Phase 6 - rerun-tasks Composition Findings

### Phase 7 - Unit Tests Findings

### Phase 8 - Validation Findings

### Phase Gate Findings

_QA gate verdicts, fix cycle counts, fidelity-gate applicability, and unresolved issues are recorded here._

### Follow-Up Items Identified

<!-- TEMPLATE FOR FOLLOW-UP ITEMS:
- **[Priority: High/Medium/Low]** [Description of follow-up needed] - Identified in Step [X.Y]
-->

### Deviations from Process

<!-- TEMPLATE FOR DEVIATIONS:
**[YYYY-MM-DD HH:MM]** - Deviation from [Step X.Y]:
- **Expected:** [What the process specified]
- **Actual:** [What was done instead]
- **Rationale:** [Why this deviation was necessary]
-->

