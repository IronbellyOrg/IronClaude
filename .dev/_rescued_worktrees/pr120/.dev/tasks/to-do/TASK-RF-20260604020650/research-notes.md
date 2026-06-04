# Research Notes: Fix M1–M4 from PR #120 auggie-review (REVIEW.md)

**Date:** 2026-06-04
**Scenario:** A (explicit — findings + files known from the review)
**Depth Tier:** Standard
**Track Count:** 1
**Source of truth for the 4 fixes:** `.dev/reviews/pr-120-20260604014836/REVIEW.md` (+ `audit.log`)

---

## EXISTING_FILES

The 4 Medium findings touch three source files in `src/superclaude/cli/sprint/` plus one new test file. Line anchors confirmed at HEAD `ea0eba80` (branch `SprintCLIWireDead`):

- **`src/superclaude/cli/sprint/executor.py`** (2791 lines) — holds M1 + M2.
  - `_run_task_subprocess` @ **L1468–1529** (M1): builds a `ClaudeProcess` via `__new__` + `_Base.__init__`, calls `proc.start()` @ **L1514**, then `_poll_with_stall_watchdog(...)` @ **L1518** with NO `try/finally`. Handles opened by `start()` are closed only by `wait()→_close_handles()`.
  - `_poll_with_stall_watchdog` @ **L1402–1465** (M2): `timeout = getattr(config,"startup_stall_timeout",0) or 0` @ L1422; if `underlying is None or timeout<=0` → plain `proc.wait()` @ L1425 (bounded). Otherwise `while underlying.poll() is None:` @ **L1439** sleeps `poll_interval` (0.5). On stall it warns (sets `acted=True`); only `stall_action=="kill"` breaks. Final `proc.wait()` @ **L1465**.
- **`src/superclaude/cli/sprint/handoff.py`** (72 lines) — holds M3.
  - `FileHandoffStore.read` @ **L62–71**: returns `None` if `not path.exists()`; otherwise `HandoffRecord.from_dict(json.loads(path.read_text()))` @ **L71** — `json.loads` (and `from_dict`) are NOT wrapped, so a corrupt file raises and aborts resume.
  - `write` @ L49–60 uses atomic temp+replace (`tmp.write_text(...)`; `tmp.replace(path)`).
- **`src/superclaude/cli/sprint/scheduler.py`** (120 lines) — target of M4 (no dedicated test).
  - `topological_launch_order(tasks, result_by_id=None)` @ **L74–104**: wave grouping; raises `CycleError(remaining)` @ L99 when a wave is empty but tasks remain.
  - `dependencies_of(task_id, entry_by_id, result_by_id=None)` @ **L41–71**: order-preserving de-duped union of declared + recorded deps; drops self-edges and deps not in `entry_by_id` (`_add` @ L57–60).
  - `is_task_satisfied(task_id, result_by_id)` @ **L107–119**: returns `True`/`False`/`None`.
  - `CycleError(ValueError)` @ L27–38 with `.unresolved` list.
- **`src/superclaude/cli/pipeline/process.py`** (reference, not edited): `ClaudeProcess.wait()` @ L159–171 does `self._process.wait(timeout=self.timeout_seconds)`, on `TimeoutExpired` calls `terminate()` (SIGTERM→10s→SIGKILL @ L173–203) and returns 124. `_close_handles()` @ L238. This is why M2's final `proc.wait()` IS bounded — the unbounded path is the poll loop, not `wait()`.

**Config defaults (`models.py:544-545`)**: `startup_stall_timeout: int = 300` (ENABLED by default), `stall_action: str = "warn"` (default) → the M2 unbounded-warn path is reachable under default config.

**Test surface (`tests/sprint/`)**: `conftest.py` present; existing relevant tests: `test_process.py` (subprocess + `_poll_with_stall_watchdog`?), `test_handoff_store.py` (FileHandoffStore read/write), `test_executor.py` (1965 lines, `_subprocess_factory` seam, `_make_config` helper). Markers in use: `@pytest.mark.unit`, `@pytest.mark.integration`, `@pytest.mark.slow`. No `test_scheduler.py` exists.

## PATTERNS_AND_CONVENTIONS

- **UV-only**: tests run via `uv run pytest tests/sprint/...`. Never `python -m`/bare `pytest`.
- **Source-of-truth**: `src/superclaude/` is canonical; the executor/handoff/scheduler edits are pure `src/` Python (no `.claude/` sync needed — these are CLI modules, not skills/agents/commands).
- **Subprocess lifecycle**: the base `ClaudeProcess` (pipeline) owns `start()/wait()/terminate()/_close_handles()`. The sprint per-task path bypasses the normal `run()` by doing manual `__new__`+`__init__` — that's why M1's leak exists.
- **Test seams**: `execute_phase_tasks(..., _subprocess_factory=...)` injects a fake `(task,config,phase)->(exit,turns,bytes)` so tests avoid real subprocesses. `_poll_with_stall_watchdog` takes a `proc` duck-typed on `_process` (with `.poll()`) + `proc.wait()` — a fake proc can drive the watchdog deterministically.
- **Atomic write idiom**: temp+replace (handoff.py, checkpoints.write_manifest). M3's fix should keep that idiom and only harden the READ path.
- **Test style**: pure-unit where possible; `test_handoff_store.py` constructs a `SprintConfig` in a tmp_path and exercises read/write directly. `test_turn_ledger_concurrency.py` is the model for a focused new unit-test file (threads + asserts).

## GAPS_AND_QUESTIONS

- **M1 fix shape**: `try/finally` around `start()`+poll calling `proc.terminate()` (which closes handles via `_close_handles()`) on exception. Confirm `terminate()` is safe to call when the process already exited (process.py:175 guards `poll() is not None → _close_handles(); return`). Researcher must confirm the exact cleanup call (`terminate()` vs a direct `_close_handles()`).
- **M2 fix shape**: in `warn` mode, bound the total loop by wall-clock so it falls through to the bounded `proc.wait()`. Options: track loop start time and `break` after `config.timeout_seconds` (or `proc.timeout_seconds`); or after the stall warning in warn mode, still fall through to `proc.wait()` (which enforces `timeout_seconds`). Researcher must determine the cleanest option that does NOT change `kill`-mode behavior and does NOT regress the existing `_poll_with_stall_watchdog` tests. Identify which existing tests in `test_process.py` exercise the watchdog so the fix preserves them.
- **M3 fix shape**: wrap `json.loads(...)`+`from_dict(...)` in `try/except (json.JSONDecodeError, ValueError)` inside `FileHandoffStore.read`, returning `None` (corrupt == absent). Researcher must confirm callers (executor.py:1103 parallel, 1277 sequential resume-skip) treat `None` as "no skip → re-run", which is the desired degrade.
- **M4 test design**: new `tests/sprint/test_scheduler.py`. Cases (from REVIEW.md M4): diamond (`A→B,A→C,B→D,C→D` ⇒ `[[A],[B,C],[D]]`), multi-wave chain, cycle (`A→B→C→A` ⇒ `CycleError` with correct `.unresolved`), self-edge drop, cross-set/unknown dep filtering. Researcher must confirm `TaskEntry` construction signature (`task_id,title,description="",dependencies=[]`) and how `topological_launch_order` consumes `TaskEntry.dependencies`.
- **Verification command**: `uv run pytest tests/sprint/test_scheduler.py tests/sprint/test_process.py tests/sprint/test_handoff_store.py -v` + full `uv run pytest tests/sprint/ -q` for regression. Plus `uv run ruff format --check src/ tests/` and `make lint` (CI runs `ruff format --check` separately — see memory).

## RECOMMENDED_OUTPUTS

Research files (3 researchers, no web — all internal):
- `research/01-source-fix-points.md` — exact edit points + fix shapes for M1, M2, M3 in executor.py + handoff.py, with line-anchored evidence and the base-class lifecycle contract.
- `research/02-test-patterns-and-seams.md` — existing test patterns in tests/sprint/ (conftest fixtures, `_make_config`, `_subprocess_factory`, fake-proc patterns for the watchdog, FileHandoffStore test setup), so the builder can specify exact test additions for M1/M2/M3 + the new M4 file.
- `research/03-scheduler-and-template.md` — scheduler.py public API + dependency semantics for M4 test design, the diamond/cycle/self-edge expected outputs, AND the MDTM template-02 read (PART 1 rules A3/A4/B2, L1–L6 handoff) the builder must follow.

## SUGGESTED_PHASES

- **Researcher 1 (File Inventory + Patterns)** → `01-source-fix-points.md`. Scope: `executor.py` (`_run_task_subprocess` L1468–1529, `_poll_with_stall_watchdog` L1402–1465), `handoff.py` (L43–72), `pipeline/process.py` (wait/terminate/_close_handles L159–238). Produce: per-finding (M1/M2/M3) exact current code, the minimal fix shape, and the lifecycle/contract facts that make the fix safe. Covers source; does NOT cover tests or scheduler.
- **Researcher 2 (Test & Verification)** → `02-test-patterns-and-seams.md`. Scope: `tests/sprint/conftest.py`, `test_process.py`, `test_handoff_store.py`, `test_executor.py` (helpers only), `test_turn_ledger_concurrency.py` (as a new-file model). Produce: how to write unit tests that (a) assert handles are closed on an exception during poll [M1], (b) drive the watchdog with a fake proc that never exits in warn mode and assert bounded return [M2], (c) feed a corrupt handoff file and assert `read()→None` [M3]. Document existing watchdog tests so the fix doesn't regress them. Covers tests; does NOT cover source fix shapes or scheduler API.
- **Researcher 3 (Integration + Template & Examples)** → `03-scheduler-and-template.md`. Scope: `scheduler.py` (full), `models.py` `TaskEntry`/`TaskResult`/`TaskStatus` for test construction, and the MDTM template-02 file. Produce: scheduler API + dependency semantics + expected wave outputs for the 5 M4 cases, plus template-02 PART 1 rules the builder must follow. Covers scheduler + template; does NOT cover executor/handoff fix shapes or test-infra.

## TEMPLATE_NOTES

- **Template 02 (complex task)** — the task involves surgical fixes + new tests + verification gates across multiple files; not a simple known-input/known-output transform. Phases: (1) M3 handoff read hardening + test, (2) M1 handle-leak fix + test, (3) M2 watchdog bound + test, (4) M4 scheduler test file, (5) verification gate (`uv run pytest tests/sprint/`, ruff format check, make lint), (6) completion. Each fix gets its own granular phase with its own test item (per A3 granularity).
- **Tier Standard** — 3 source files + ~4 test additions; non-trivial (concurrency/resource lifecycle) but tightly scoped and already grounded.
- **QA_GATE_REQUIREMENTS**: FINAL_ONLY (one verification phase before completion is sufficient; PER_PHASE would be overkill for 4 surgical fixes — but each fix item carries its own `uv run pytest <file>` verification).
- **TESTING_REQUIREMENTS**: UNIT (every fix M1/M2/M3 gets a regression-proving unit test; M4 IS a unit-test file).
- **VALIDATION_REQUIREMENTS**: `uv run pytest tests/sprint/ -q` must pass; `uv run ruff format --check src/ tests/` clean; `make lint` clean.

## AMBIGUITIES_FOR_USER

None blocking — intent is clear (fix the 4 Medium findings from the review). One design choice the builder should encode as the recommended approach (not a halt): **M2's exact bounding strategy** (wall-clock ceiling that falls through to the bounded `proc.wait()`, preserving `kill`-mode behavior). The researchers will determine the cleanest shape; if a genuinely load-bearing choice remains, it goes in the task file's Open Questions, not auto-applied.
