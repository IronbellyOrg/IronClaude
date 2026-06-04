# Code Review: PR #120 — Sprint CLI per-task execution wire-up

**Target**: PR #120 (`SprintCLIWireDead` → `master`)
**Reviewer**: /sc:auggie-review (depth=standard, focus=all, scope=code+tests)
**Generated**: 2026-06-04 01:30 UTC
**Source PR**: https://github.com/IronbellyOrg/IronClaude/pull/120
**Base ↔ Head**: `master` ↔ `SprintCLIWireDead` (`ea0eba80`)
**Scope**: `src/superclaude/cli/sprint/` (10 files, +1,097) + `tests/sprint/` (24 files, +1,632). The PR's other ~11,106 lines are `.dev/` pipeline artifacts and were **excluded** from review by user choice.
**Stats**: 34 files reviewed, ~3,884 diff lines, **15 findings kept** (4 Medium · 10 Low · 1 Nit), **7 findings dropped during grounding** (3 provably-false coverage claims + 4 unverifiable/wrong-mechanism — see Audit).

---

## Summary

**Recommendation: Approve with comments.** No Critical or High findings. The core change is carefully engineered: the `TurnLedger.try_launch` TOCTOU fix is correct and genuinely tested, the handoff schema is forward-compatible, the K=1 sequential path is preserved byte-for-byte, and the parallel path routes shared mutations through real locks. The three highest-value items are all **robustness-on-failure-paths**, not correctness-on-happy-path: (1) a subprocess file-handle leak when an exception interrupts the per-task wait, (2) the per-task stall watchdog can wait **unbounded** in its *default* `warn` mode, and (3) a corrupted handoff file raises an unhandled exception on resume. One real test-coverage gap exists (the `scheduler` module has no dedicated test).

**A note on this report's confidence**: Auggie's `src/` findings were accurate (every cited line verified). Its `tests/` findings were not — line numbers were systematically fabricated (e.g., line 653 cited in an 81-line file) and **four of six coverage-gap claims were provably false** (the tests they said were missing exist in this very PR). Those were dropped at the grounding gate. The kept test findings below were re-grounded by hand against real code.

---

## Findings

### 🟠 High (should fix before merge)

_None._

### 🟡 Medium (fix in this PR if cheap, otherwise file follow-up)

#### M1. Subprocess file handles leak when an exception interrupts the per-task wait
- **File**: `src/superclaude/cli/sprint/executor.py:1493`–`1520`
- **Category**: resource-leak · **Source**: auggie (verified)
- **Evidence**:
  ```python
  proc = ClaudeProcess.__new__(ClaudeProcess)
  proc.config = config
  proc.phase = phase
  _Base.__init__(proc, prompt=prompt, output_file=..., env_vars=_task_env(task, config, phase))
  proc.start()                          # opens _stdout_fh / _stderr_fh
  _poll_with_stall_watchdog(proc, config, output_path=config.task_output_file(phase, task))
  ```
- **Why this matters**: `start()` opens stdout/stderr file handles; they are closed only by `wait() → _close_handles()` (`pipeline/process.py:170`). There is no `try/finally` around `start()` + `_poll_with_stall_watchdog`. If the poll raises (KeyboardInterrupt during `time.sleep`, or `_size()` raising an uncaught error), `wait()` is never reached and the handles leak. Under K>1 each leaked task compounds the descriptor pressure before the exception unwinds the pool.
- **Recommendation**: Wrap `start()` + poll in `try/finally` that calls `proc.terminate()` (which closes handles) on exception. The sequential legacy path avoided this because it used the `ClaudeProcess.__init__` + inherited `run()`; the new manual `__new__`/`__init__` path bypasses that safety.

#### M2. Per-task stall watchdog waits unbounded in its default `warn` mode
- **File**: `src/superclaude/cli/sprint/executor.py:1422`–`1465`
- **Category**: correctness / liveness · **Source**: auggie (location verified; **mechanism corrected below**)
- **Evidence**:
  ```python
  while underlying.poll() is None:
      time.sleep(poll_interval)
      cur = _size()
      if cur != last_size:
          last_size = cur; last_progress = time.monotonic(); acted = False
      elif not acted and (time.monotonic() - last_progress) > timeout:
          acted = True
          _stall_logger.warning(...)
          if getattr(config, "stall_action", "warn") == "kill":
              underlying.terminate(); break
  proc.wait()   # bounded by timeout_seconds — but only reached if the loop exits
  ```
- **Why this matters**: Defaults are `startup_stall_timeout=300` (**enabled**) and `stall_action="warn"` (`models.py:544-545`). In `warn` mode, when a child wedges — produces no output **and** never exits — the watchdog warns once (`acted=True`) and then loops `while poll() is None: sleep(0.5)` **forever**. The bounded `proc.wait(timeout=timeout_seconds)` on the next line is never reached because the loop never breaks. (Auggie reported the cause as "`proc.wait()` has no timeout"; that is wrong — the base `wait()` *does* pass `timeout=self.timeout_seconds` and escalates SIGTERM→SIGKILL. The real unbounded path is this poll loop under `warn`.) This undercuts the feature's own stated goal ("Previously a hung per-task process was never detected").
- **Recommendation**: In `warn` mode, also enforce an absolute ceiling — e.g., break out of the loop after `config.timeout_seconds` of wall-clock so control falls through to the bounded `proc.wait()`, or always `terminate()` after the stall warning regardless of `stall_action` (downgrading `warn` to "log loudly, then still bound the wait").

#### M3. Corrupted handoff file raises an unhandled exception on resume
- **File**: `src/superclaude/cli/sprint/handoff.py:62`–`71`
- **Category**: error-handling · **Source**: auggie (verified)
- **Evidence**:
  ```python
  def read(self, *, phase, task) -> HandoffRecord | None:
      path = self.config.handoff_file(phase, task)
      if not path.exists():
          return None
      return HandoffRecord.from_dict(json.loads(path.read_text()))
  ```
- **Why this matters**: `read()` degrades gracefully on **absence** (returns `None`), and the docstring promises resume "degrades gracefully." But a **corrupt** handoff file (truncated/garbled JSON) makes `json.loads` raise `JSONDecodeError`, which propagates up through the resume-skip check (`executor.py:1277` sequential, `1103` parallel) and aborts the whole sprint. The atomic temp+replace write makes corruption unlikely from this process, but external tampering or a non-atomic crash on some filesystems can produce it — and crash-recovery robustness is the entire point of this subsystem.
- **Recommendation**: Wrap the parse in `try/except (json.JSONDecodeError, ValueError)` inside `FileHandoffStore.read` and treat a corrupt file as absent (`return None`), so a damaged record re-runs the task instead of crashing resume.

#### M4. The `scheduler` module has no dedicated test (cycles, diamonds, multi-wave)
- **File**: `src/superclaude/cli/sprint/scheduler.py:74`–`104` (the untested unit)
- **Category**: tests / coverage · **Source**: auggie (verified — `grep` finds zero references to `topological_launch_order` / `CycleError` / `dependencies_of` anywhere in `tests/`)
- **Why this matters**: `topological_launch_order` is the correctness foundation for K>1 parallelism — it groups tasks into dependency waves and raises `CycleError` on cycles. It is exercised only *indirectly* by `test_handoff_performance.py` with trivial 2–4-task graphs. There is no test for diamond dependencies (`A→B, A→C, B→D, C→D` ⇒ `[[A],[B,C],[D]]`), the cycle path (`CycleError.unresolved` contents), self-edge dropping (`dependencies_of:58`), or cross-set dep filtering. A regression here could deadlock or mis-order parallel waves silently.
- **Recommendation**: Add `tests/sprint/test_scheduler.py` parametrized over: diamond graph, multi-wave chain, cycle detection (assert `CycleError` + correct `unresolved`), self-edge drop, and missing/cross-phase dep filtering.

### 🟢 Low (nice-to-have)

- **L1 — `task_id` is interpolated into file paths without a guard** (`models.py:698`–`710`, `handoff_file`/`task_output_file`/`task_error_file`). Defense-in-depth only: the parser (`config.py:387`, `_TASK_HEADING_RE`) constrains `task_id` to `T\d{2}\.\d{2}`, so `/`/`..` cannot reach these via the normal path. Add an explicit `assert`/validation in `TaskEntry.__post_init__` to harden against programmatically-constructed entries (e.g., from persisted results).
- **L2 — `TurnLedger.try_launch(allocation=…)` checks `can_launch()` (vs `minimum_allocation`) but debits `allocation`** (`models.py:956`–`971`). Currently unreachable — both call sites (`executor.py:1120`, `1300`) pass no argument — but a future caller passing a large `allocation` would pass the gate yet overdraw. Validate `available() >= debit_amount` instead.
- **L3 — `_size()` returns `0` on any `OSError`** (`executor.py:1428`–`1434`), so a permission error reads as "no growth" and can spuriously trip the stall path. Log the `OSError` rather than silently flattening it to `0`. (The `exists()`+`stat()` TOCTOU itself is harmless — `FileNotFoundError` is an `OSError` subclass and is caught.)
- **L4 — `scheduler.dependencies_of` silently drops deps not in the task set** (`scheduler.py:57`–`71`). Intentional for cross-phase deps, but a typo'd intra-phase dep is dropped with no signal and the task launches early. Emit a debug-log of dropped deps.
- **L5 — `completed_results.append(result)` runs outside the lock** in `_execute_phase_tasks_parallel` (`executor.py:1180`). Safe today because `pool.map` is a per-wave barrier and the merge is single-threaded, but it's the one shared-list mutation not under `lock` — a future refactor to pipeline waves would make it race. Move it inside the lock or add a comment pinning the invariant.
- **L6 — Handoff write has no `fsync`** (`handoff.py:49`–`60`). temp+replace is atomic w.r.t. readers and safe against *process* death mid-write (the target is never partially written), so the docstring is defensible — but it is not power-loss durable. Either add `os.fsync(tmp.fileno())` before `replace`, or narrow the docstring to "atomic w.r.t. concurrent readers."
- **L7 — `test_handoff_concurrency` doesn't force aligned starts** (`tests/sprint/test_handoff_concurrency.py:46`–`60`; Auggie's cited line 653 was fabricated). The 4×300 tight-loop writes do create real lock contention, but a `threading.Barrier(4)` before the loop would maximize collision probability and make the stress test deterministic.
- **L8 — `test_handoff_performance` wall-clock speedup test uses `time.sleep`** as the mock task duration. Real-time ratio assertions are CI-flaky under load; prefer a concurrency counter (max simultaneous active tasks) or add margin + a warmup run.
- **L9 — `fake_claude` defaults `FAKE_CLAUDE_NUM_TURNS` to `0`** (`tests/sprint/e2e_real/fake_claude.py:90`; Auggie's cited line 13 was the docstring). The regression *is* covered by `test_e2e_turn_count` (asserts `turns_consumed == known_n` exactly), so this is hardening, not a hole: a non-zero default sentinel would make any future e2e test that forgets to set it still diverge from the old hard-coded `0`.
- **L10 — `HandoffRecord.from_task_result` edge cases are thinly tested** (`test_handoff_record.py`). Happy path is covered; add cases for `FAIL_TERMINAL`+`GateOutcome.FAIL`, `INCOMPLETE`, and empty `dependencies`.

### 💬 Nits

- **N1** — `test_executor.py` backward-compat check asserts `"with ThreadPoolExecutor" in source`; the static string scan could miss whitespace/alias variants (`Thread (`, `from threading import Thread as T`). A runtime `threading.active_count()` before/after assertion (as `test_handoff_backward_compat` already does) is stronger than string matching.

## Architectural / Cross-Cutting Observations

The design is sound. The dual-lock model (`TurnLedger._lock` RLock for atomic budget ops + the executor's `threading.Lock` serializing per-task reconcile/hooks/TUI) is correct and the spawn deliberately runs *unlocked* to preserve the wall-clock win. The `_run_one_task` helper genuinely unifies the K=1 and K>1 paths so they classify and reconcile identically — a good call that avoids drift. The handoff schema's `from_dict` forward-compat (`data.get` for every field, tolerating unknown keys) is the right pattern for a versioned on-disk record. No layering violations were found between executor/scheduler/handoff/process.

## Audit

- **Auggie passes**: 2 chunks (src, tests), both exit 0, both JSON-unwrapped cleanly. Claude orchestration + grounding only.
- **Findings dropped during grounding (7)**:
  1. *"No TurnLedger.try_launch atomicity test"* — **FALSE**. `tests/sprint/test_turn_ledger_concurrency.py::test_try_launch_grants_exactly_n_under_concurrency` runs 400 concurrent attempts against a 20-launch budget and asserts exactly 20 granted + `consumed == 100`. This is precisely the test Auggie said to add.
  2. *"SHA-guard mechanism untested"* — **FALSE**. `test_e2e_sha_guard_real_edit.py` has paired tests: `test_real_operator_edit_mid_flight_aborts` (real edit → exit≠0 + abort markers) and `test_no_false_trip_engine_provenance_write` (engine's own write → no trip). Together they pin the mechanism (always-pass fails the positive; always-fail fails the negative).
  3. *"Per-task subprocess env never verified"* — **FALSE**. `fake_claude.py:162-167` records the real spawned child's `CLAUDE_SETTINGS_DIR`/`CLAUDE_PLUGIN_DIR`/`CLAUDE_WORK_DIR` into `env_log`, which the e2e isolation tests assert on.
  4. *"No rerun+handoff resume coverage"* — **unverifiable absence**; six resume/handoff test files exist (`test_resume_{semantics,contract,backward_compat}`, `test_handoff_{store,crash_consistency,performance}`). Not included as a gap.
  5. *"Unbounded ThreadPoolExecutor queue exhausts FDs"* (executor.py:1174) — **wrong mechanism**. `_worker` (which spawns the subprocess) only runs in one of `k` pool threads, so at most `k` subprocesses exist at once. Queued items are inert closures; no FD pressure.
  6. *"test_write_preliminary patches os.open but doesn't verify sentinel"* (executor.py:1376) — **ungrounded**; the cited line is a different test (`test_integration_subprocess_five_tasks_mixed_outcomes`).
  7. *"backward_compat allows threads+1"* (test_handoff_backward_compat.py:542) — **ungrounded**; cited line 542 exceeds the file's 157 lines.
- **Citation reliability**: `src/` chunk = all cited lines verified accurate. `tests/` chunk = line numbers systematically fabricated; kept test findings were re-grounded by hand.

<!-- SC:AUGGIE-REVIEW:SUMMARY
status: success
critical: 0 high: 0 medium: 4 low: 10 nit: 1
dropped: 7
auggie_chunks: 2
-->
