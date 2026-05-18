# Research Notes: Sprint Runner — 6 Phase-Duration Fixes

**Date:** 2026-05-18
**Scenario:** A (Explicit — fixes specified with file:line targets)
**Depth Tier:** Standard
**Track Count:** 1 (all fixes touch the same `src/superclaude/cli/sprint/` + `src/superclaude/cli/pipeline/` subsystem and need to be reconciled together)
**Source signal:** Audit of `superclaude sprint run .dev/releases/current/task-builder-merge/tasklist-index.md` across 6 phases (see `.dev/releases/current/task-builder-merge/results/phase-{1..6}-output.txt`).

---

## EXISTING_FILES

### Sprint runner core (target for ALL 6 fixes)
- `src/superclaude/cli/sprint/config.py` — `SprintConfig` dataclass + `load_config()`. **L284:** `stall_timeout: int = 0`, `stall_action: str = "warn"` (FIX #1 target).
- `src/superclaude/cli/sprint/executor.py` (~1700 lines) — main sprint orchestrator.
  - **L82-87:** Remediation path — `timeout_seconds=self._config.max_turns * 60` (FIX #5 latent foot-gun; inconsistent with main path).
  - **L1086-1115:** `_run_task_subprocess` — uses `config.output_file(phase)` / `config.error_file(phase)` (FIX #2 collision target).
  - **L1100-1108:** Main per-phase `ClaudeProcess()` construction — `timeout_seconds=config.max_turns * 120 + 300`.
  - **L1320-1335:** Phase-start block — `proc_manager.start()`, `started_at`, `logger.write_phase_start(phase, started_at)` (FIX #6 — function IS called here).
  - **L1360-1395:** Watchdog block — gated on `stall_timeout > 0 AND events_received > 0 AND not _stall_acted`. The `events_received > 0` clause is the explicit startup-stall exclusion (FIX #1 watchdog-split target).
  - **L1417:** Only `time.sleep(0.5)` in the poll loop.
  - **L1422-1423:** Timeout-path exit code → 124.
- `src/superclaude/cli/sprint/process.py` — `ClaudeProcess` sprint subclass.
  - **L108-122:** `super().__init__(... timeout_seconds=config.max_turns * 120 + 300, ...)` (FIX #5 reconcile target).
  - **L115:** Identical formula to executor.py:1106 → keep authoritative.
- `src/superclaude/cli/sprint/logging_.py` — JSONL/MD log writer.
  - **L59-69:** `write_phase_start()` writes `{"event":"phase_start", ...}` to JSONL via `_jsonl()`. **VERIFIED CALLED** at `executor.py:1330` but `phase_start` events are **ABSENT** from the produced `execution-log.jsonl` (only `sprint_start` + `phase_complete` events present). **This is a real bug beyond what the synthesis said** — FIX #6 must investigate root cause, not just "add the write call."
  - **L31-49:** `write_header()` writes `sprint_start`.
  - **L92+:** `write_phase_result()` writes `phase_complete`.
  - **L210-212:** `_jsonl()` — `with open(... "a") as f: f.write(json.dumps(data) + "\n")`. Append mode confirmed — so writes that DO get called should land.
- `src/superclaude/cli/sprint/monitor.py` — `OutputMonitor`.
  - **L33-44:** `error_max_turns` detection.
  - **L312-326:** `_poll_loop` updates `output_bytes` via `output_path.stat().st_size`.
  - **L334:** `growth_rate_bps` computed.
  - **L555-571:** `files_changed` regex extractor — reads live `phase-N-output.txt` stream.

### Pipeline (shared with roadmap/audit CLIs — FIX #2/#3 risk surface)
- `src/superclaude/cli/pipeline/process.py` — base `ClaudeProcess`.
  - **L79-95:** `build_command()` hard-codes `--no-session-persistence` at line 84 (FIX #3 target).
  - **L120-122:** `start()` opens stdout with `open(self.output_file, "w")` (FIX #2 truncate target). Also opens `.log` variant when `tool_write_mode=True` — same truncate behavior.
  - **L123:** `open(self.error_file, "w")` — same problem.
  - **L114-130:** `start()` body.
  - **L134:** `Popen()` returns immediately — no instrumentation on spawn.

### Phase task subprocess (FIX #2 path B — per-task output paths)
- `src/superclaude/cli/sprint/executor.py:1086-1115` — `_run_task_subprocess`. Each per-task subprocess writes to the SAME `config.output_file(phase)` → 18 tasks × overwrite cycle on Phase 5.
- `src/superclaude/cli/sprint/config.py` — `output_file()` / `error_file()` methods (need to check for existing per-task overloads).

### Tests (FIX #1 and #2 must add regression tests)
- `tests/cli/sprint/` directory — confirm test framework and patterns.
- `tests/cli/pipeline/` — base ClaudeProcess tests.
- Look for existing `stall_timeout` / `start()` truncation tests as patterns to follow.

### Recent execution evidence (READ-ONLY — for context, NOT modified by this task)
- `.dev/releases/current/task-builder-merge/execution-log.jsonl` — 5 events: `sprint_start` + 4 `phase_complete` (P2-P5). Missing: phase_1 complete, all `phase_start` events.
- `.dev/releases/current/task-builder-merge/execution-log.md` — 4 phase rows in the markdown table.
- `.dev/releases/current/task-builder-merge/results/phase-{1..6}-output.txt` — JSONL session streams; sizes 154-351KB. Phase 6 still in flight as of 2026-05-18T01:42:22Z.

---

## PATTERNS_AND_CONVENTIONS

### Pythonic patterns observed in sprint runner
- Dataclass-driven config (`SprintConfig`) with defaults set on the dataclass itself (FIX #1 simplest: edit the default in `config.py:284`).
- Subprocess management via `subprocess.Popen` + `with open(...) as fh` for file handles.
- All datetimes are `datetime.now(timezone.utc)` (UTC, naive=False).
- Deadline enforcement uses `time.monotonic()` (immune to NTP — explicit comment at executor.py:1328-1329).
- Debug logging via `debug_log(_dbg, "<event_name>", **kwargs)` — used throughout poll loop.
- JSONL events use snake_case event names (`sprint_start`, `phase_start`, `phase_complete`, `phase_interrupt`).
- Watchdog state via local flags (`_stall_acted`, `_timed_out`) inside the poll loop.

### File handling pattern (relevant to FIX #2)
- `open(..., "w")` is used pervasively — likely intentional original design. Switching to `"a"` is a behavioral change with side effects (subsequent reads see prior content). Per-task suffixed files is the safer fix.

### Naming conventions
- Files: snake_case (`logging_.py` has trailing underscore to avoid stdlib collision).
- Methods: snake_case; private = leading underscore.
- Tests: `tests/cli/sprint/test_<module>.py`.

### Code-quality gates
- UV for all Python ops (per CLAUDE.md).
- `make lint` / `make format` (ruff).
- `make test` (pytest).
- Per CLAUDE.md: "src/superclaude/ is source of truth. make sync-dev copies src/ → .claude/. make verify-sync fails if .claude/ has dirs with no src/ counterpart."

---

## GAPS_AND_QUESTIONS

1. **Does `_run_task_subprocess` write to a different output file per task?** Need to confirm — synthesis says no, but worth verifying by reading L1086-1115 in full.
2. **Does `config.output_file(phase)` accept a task_id parameter or only phase?** Need to check `SprintConfig.output_file()` signature.
3. **Why are `phase_start` events missing from the JSONL despite the function being called?** Three hypotheses to test:
   - The JSONL file was rotated between `phase_start` writes (unlikely — append mode).
   - There's a separate truncation step that clears it (need to grep for `execution_log_jsonl.write_text` or `.unlink`).
   - The actual `executor.py:1330` call is in a code path that doesn't execute for some reason.
4. **Is the remediation path at `executor.py:82-87` ever triggered in current sprints?** Need to find its callers — if dead code, fix is trivial; if live, fix needs coordination.
5. **What is the test framework convention for testing subprocess starts?** Need to look at existing `tests/cli/pipeline/` for fixtures + patterns.
6. **Does anything else in the codebase rely on `--no-session-persistence`?** Search `--no-session-persistence` usage — may be required for sprint isolation invariants.
7. **Does the watchdog action `"warn"` (default) at config.py:285 emit anywhere?** Per the watchdog branch logic at executor.py:1395+, the warn path needs verification — if it silently does nothing, that's a separate observability bug.
8. **Are there existing fixtures for synthetic JSONL streams?** FIX #1 watchdog tests need to simulate stall conditions; existing tests may already have these.

---

## RECOMMENDED_OUTPUTS

The 6 fixes naturally group into 4 implementation clusters (file-shaped, not concern-shaped) so phases can be batched:

| Cluster | Files touched | Fixes covered | Risk |
|---|---|---|---|
| C1: Config + watchdog | `config.py`, `executor.py:1360-1395` | #1 (stall_timeout default + watchdog split) | Medium — changing watchdog gate behavior |
| C2: Output-file collision | `pipeline/process.py:120-122`, `executor.py:1086-1115`, `config.py` (add per-task path helper) | #2 (output overwrite) | High — affects every Claude subprocess in the project |
| C3: Timeout reconciliation | `executor.py:82-87` | #5 (latent foot-gun) | Low — single-formula change |
| C4: Observability | `executor.py:1320-1335`, `logging_.py` | #6 (phase_start in JSONL) + investigate root cause | Low — additive |
| (deferred) C5: `--no-session-persistence` | `pipeline/process.py:84` | #3 (warmed daemon) | **Very High** — fundamentally changes sprint isolation. Per audit Theory: ~5-10 min savings/phase. **Defer** to a separate task — too cross-cutting for this task. |
| (deferred) C6: Fan-out injection | `sprint/process.py:build_prompt()` | #4 (axis-overlay fan-out) | Medium — prompt-engineering change; needs A/B validation. **Defer** — instrumenting Theories #1, #2, #5, #6 first will reveal whether #4 is still the bottleneck. |

**Recommendation:** This task implements C1-C4 (the 4 deterministic code fixes). C5/C6 documented as Open Questions / Follow-Up because their ROI depends on what C1-C4 surface in the next sprint run.

**Deliverables:**
- Code changes to: `config.py`, `executor.py`, `pipeline/process.py`, optionally `logging_.py`.
- Tests for: stall_timeout default behavior, startup-stall watchdog firing on no-event subprocess, output-file non-truncation on relaunch, phase_start JSONL emission.
- `make sync-dev` + `make verify-sync` clean.
- `make lint` + `make test` green.

---

## SUGGESTED_PHASES

(For the BUILDER to construct from — not the orchestrator's phases.)

| Phase | Purpose | Items |
|---|---|---|
| **P1: Preparation** | Confirm refs, branch from `feat/hook-sync-and-matcher-fix`, snapshot failing state | 2-3 items |
| **P2: C3 timeout reconciliation** (smallest, lowest risk → land first to build confidence) | Single-line change at `executor.py:86` | 1 implementation + 1 test + 1 verify |
| **P3: C1 stall_timeout + watchdog split** | Two changes: `config.py:284-285` default + `executor.py:1360-1395` split into startup/mid watchdogs | 2 impl + 2 test + 1 verify |
| **P4: C2 output-file collision** | Per-task output path: add `task_output_file()` method to `SprintConfig`, change `executor.py:1101-1102` to use it. Append mode is the simpler alternative — present both as Open Question. | 3 impl + 2 test + 1 verify |
| **P5: C4 phase_start JSONL** | Investigate root cause; add missing write call(s); test JSONL emission | 1 investigation + 1 impl + 1 test |
| **P6: Integration + QA** | Run `make test`, `make sync-dev`, `make verify-sync`. Spawn rf-qa for code review. Final QA gate. | 3-4 items |
| **P7: Completion** | Update task status to Done; write summary. | 2 items |

Researcher assignments (5 researchers, parallel):

| # | Topic | Scope | Output |
|---|---|---|---|
| 1 | File Inventory | All files in EXISTING_FILES above (sprint runner core + pipeline) | `research/01-file-inventory.md` |
| 2 | Patterns & Conventions | Read existing tests + watchdog impl + datetime/logging patterns | `research/02-patterns.md` |
| 3 | Integration Points | Map callers of `_run_task_subprocess`, `output_file()`, `write_phase_start`, watchdog. Cross-check `--no-session-persistence` usage | `research/03-integration-points.md` |
| 4 | Template & Examples | Read MDTM template 02; scan `.dev/tasks/done/` for prior sprint-runner tasks as examples | `research/04-template-and-examples.md` |
| 5 | Test & Verification | Map existing sprint/pipeline test fixtures; find subprocess-mock patterns; identify how to test stall_timeout, truncate, JSONL emission | `research/05-test-and-verification.md` |

No web research needed in initial pass — codebase is fully self-contained for Python stdlib + ruff + pytest. Quality gate may identify gaps requiring it.

---

## TEMPLATE_NOTES

- **Template selection: 02 (Complex Task)** — Reasoning:
  - Multi-file changes across 3 modules (`config.py`, `executor.py`, `process.py`).
  - 4 distinct fix clusters with sequencing dependencies (C3 → C1 → C2 → C4 keeps cognitive load manageable).
  - Each fix requires impl + test + verify cycle (template 02 supports phased execution).
  - QA gates required per phase (PER_PHASE).

- **QA_GATE_REQUIREMENTS: PER_PHASE** — Each fix cluster (C1-C4) gets its own QA verification because changes are independent and a regression in C2 shouldn't block C1's deliverable.

- **TESTING_REQUIREMENTS: UNIT + INTEGRATION** — Unit tests for config defaults, watchdog split logic, per-task path generation. Integration tests for subprocess relaunch non-truncation and JSONL emission. No E2E required (would need a full sprint run).

- **VALIDATION_REQUIREMENTS:**
  - `uv run pytest tests/cli/sprint/ tests/cli/pipeline/ -v` — passes.
  - `make lint` — passes (ruff clean).
  - `make sync-dev && make verify-sync` — clean.
  - Existing sprint tests (`tests/cli/sprint/test_executor*.py` if present) still pass.

- **EXECUTION_CONTEXT_REQUIREMENTS: AUTO** — Should emit (5+ inferable source areas).

---

## AMBIGUITIES_FOR_USER

1. **Append-mode vs. per-task output paths (FIX #2 sub-choice):** Append mode (`open(..., "a")`) is a 1-line change but produces a less-clean JSONL stream (no clear per-task delimiters; downstream JSONL parsers must handle multi-session). Per-task suffixed files (`phase-N-task-T01.01-output.txt`) preserves clean per-task streams but is a 5-10 line change across `config.py` + `executor.py`. **Recommendation:** per-task suffixed files — better forensics. Builder should treat this as the default; the append-mode alternative goes in Open Questions.

2. **`--no-session-persistence` removal (FIX #3) deferred:** Scoped OUT of this task. The audit estimated 5-10 min/phase savings, but removing it requires reworking the executor's per-phase prompt injection model and prompt-cache state. Document as a separate follow-up task. If the user disagrees and wants it bundled, they can extend the task file before execution.

3. **Fan-out injection (FIX #4) deferred:** Same reason — prompt-engineering changes need their own A/B test cycle and behavioral validation. Document as a follow-up. Builder should NOT include fan-out logic in this task.

4. **Watchdog action default — `"warn"` vs `"kill"`:** Synthesis recommended `"kill"` as default. This is a strong behavioral change that could kill in-progress phases on a flaky network. **Recommendation:** keep `"warn"` as default for `stall_action` even after enabling `stall_timeout`; document `"kill"` as the recommended production value. Builder should flag this in Open Questions and let user choose.

5. **The `phase_start` JSONL bug (FIX #6) is bigger than synthesis claimed:** `write_phase_start` IS being called but the event isn't in the JSONL. This is not just "add a write call" — it's "diagnose why an existing write isn't landing." Builder must include an investigation item before any code change.
