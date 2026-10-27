# Patch Specification: pass_no_report Fix

**Spec ID**: SPEC-PNR-001
**Version**: 1.1.0
**Date**: 2026-03-16
**Status**: REVIEWED — spec-panel critique applied (v1.0.0 → v1.1.0)
**Affected files**:
- `src/superclaude/cli/sprint/executor.py`
- `src/superclaude/cli/sprint/process.py`
- `tests/sprint/test_executor.py` (new tests)
- `tests/sprint/test_phase8_halt_fix.py` (new tests)

**Changelog**:
- v1.1.0 (2026-03-16): Applied spec-panel recommendations — FR-001 signature adds `started_at`,
  FR-007 normative contradiction resolved, stale-file risk promoted and mitigated with mtime guard,
  zero-byte agent file gap closed, OSError logging added, T-002b and T-006 tests added,
  FR-003 content invariant added, NFR-001/002/003 tightened, Change 1/2/3 updated accordingly.

---

## 1. Problem Statement

All phases of the v2.25.5-PreFlightExecutor sprint reported `pass_no_report` instead of `pass` in the execution log. The sprint succeeded (all phases `is_success = True`), but the degraded status obscures telemetry and prevents downstream analytics from distinguishing "agent reported success" from "executor inferred success."

### Root Cause

The agent subprocess never writes `results/phase-N-result.md` because `ClaudeProcess.build_prompt()` contains no instruction to do so. `_determine_phase_status()` falls through to `PASS_NO_REPORT` (line 1045): output exists but no result file exists.

```
exit_code == 0
→ result_file.exists() → FALSE  (agent never wrote it)
→ output_file.exists() and size > 0 → TRUE
→ detect_error_max_turns() → FALSE
→ return PhaseStatus.PASS_NO_REPORT     ← THE BUG
```

### Observed vs Expected

| | Observed | Expected |
|---|---|---|
| Phase 1–5 status in execution-log | `pass_no_report` | `pass` |
| Sprint outcome | `success` | `success` (unchanged) |
| Executor result file source | `executor (not agent self-report)` | `executor (not agent self-report)` for D, `agent` for A |

---

## 2. Solution Architecture: Option D + Option A Layered

### Layer 1 — Option D (Revised): Executor Pre-Write (Primary Fix)

**Principle**: The executor is authoritative (executor.py comment at line 706–707). When `exit_code == 0`, write a minimal preliminary result file containing `EXIT_RECOMMENDATION: CONTINUE` **before** `_determine_phase_status()` runs. The classifier then finds the file and returns `PhaseStatus.PASS` instead of falling through to `PASS_NO_REPORT`.

**Critical constraint**: The preliminary write MUST fire ONLY for `exit_code == 0`. The non-zero exit code paths (`TIMEOUT`, `ERROR`, `INCOMPLETE`, `PASS_RECOVERED`) have specialized logic in `_determine_phase_status()` that would be corrupted if a stale preliminary file were present.

### Layer 2 — Option A: Prompt Injection (Defense-in-Depth)

**Principle**: Instruct the agent to write the result file itself. When the agent complies, `_determine_phase_status()` reads the agent-written file (richer content: per-task outcomes, actual pass/fail signal) before the executor's preliminary write takes effect. When the agent doesn't comply (LLM non-compliance), Option D catches it.

**Injection target**: `ClaudeProcess.build_prompt()` in `process.py` — the `## Important` section at the end of the prompt (line 188–193).

---

## 3. Functional Requirements

### FR-001: _write_preliminary_result() Function

A new module-level function `_write_preliminary_result(config: SprintConfig, phase: Phase, started_at: float) -> None` MUST be added to `executor.py`.

**Signature**:
```python
def _write_preliminary_result(
    config: SprintConfig,
    phase: Phase,
    started_at: float,  # Unix timestamp of subprocess launch (started_at.timestamp())
) -> None:
```

**Behavior**:
- Derives `result_path = config.result_file(phase)`
- Checks whether a **fresh, non-empty** agent-written result file already exists:
  - If `result_path.exists()` AND `result_path.stat().st_size > 0` AND `result_path.stat().st_mtime >= started_at`:
    the file was written by the agent during this run → return immediately (no-op)
  - Otherwise (file absent, empty, or stale from a prior run): proceed with write
- Creates parent directory (`mkdir(parents=True, exist_ok=True)` for safety)
- Writes the following minimal content:
  ```
  EXIT_RECOMMENDATION: CONTINUE
  ```
- Failure is non-fatal: wrap in `try/except OSError` — on `OSError`, emit a WARNING via the module logger before continuing:
  ```python
  except OSError as e:
      logger.warning("preliminary result write failed: %s; phase may report PASS_NO_REPORT", e)
  ```
- Does NOT take `exit_code` as parameter — the caller is responsible for the `exit_code == 0` guard

**Invariants**:
- Content written by this function MUST contain `EXIT_RECOMMENDATION: CONTINUE`
- Content written by this function MUST NOT contain `EXIT_RECOMMENDATION: HALT`
- Content written by this function MUST NOT contain `status: FAIL`, `status: FAILED`, `status: PARTIAL`

**Ordering invariant** (see FR-002): This function MUST always be called BEFORE `_determine_phase_status()` and BEFORE `_write_executor_result_file()`. These three operations form an ordered triple; their relative order MUST NOT be changed by refactoring. See §7 Change 2 for the enforced sequence.

**The `started_at` mtime guard closes two exploitable gaps**:
1. **Zero-byte agent file**: A file with `st_size == 0` is treated as absent — `CONTINUE` is written,
   eliminating the `PASS_NO_SIGNAL` regression that would otherwise occur.
2. **Stale file from prior sprint run**: A file with `st_mtime < started_at` predates the current
   subprocess launch — it is from a previous run and is overwritten with `CONTINUE`, preventing an
   incorrect `HALT` caused by an accumulation of stale failure files in the results directory.

### FR-002: Injection Site in execute_sprint()

In `executor.py:execute_sprint()`, the call to `_write_preliminary_result()` MUST be inserted **between** `finished_at = datetime.now(timezone.utc)` and the call to `_determine_phase_status()`, guarded by `exit_code == 0`. The `started_at.timestamp()` value available at the call site MUST be passed as the third argument.

```python
finished_at = datetime.now(timezone.utc)
# ... (existing debug_log and signal_handler check) ...

# Option D: Write preliminary result file before status determination.
# Fires only for exit_code == 0. Non-zero paths are unaffected.
# If the agent already wrote a fresh, non-empty result file (Option A), this is a no-op.
if exit_code == 0:
    _write_preliminary_result(config, phase, started_at.timestamp())

status = _determine_phase_status(
    exit_code=exit_code,
    ...
)
```

**The guard `if exit_code == 0` is a hard requirement.** Non-zero exit paths MUST NOT be affected.

**Ordering note**: `started_at` is captured at subprocess launch (line ~581). It is available throughout the phase loop body. Pass `started_at.timestamp()` (float), not `started_at` (datetime), to match the `float` parameter type.

### FR-003: _write_executor_result_file() Overwrite Behavior (Unchanged)

The existing `_write_executor_result_file()` call (line 709) MUST remain in place and unchanged. It fires AFTER `_determine_phase_status()` returns and overwrites the preliminary result file with the full executor report including telemetry (output bytes, last task ID, files changed, duration). This is correct and intentional — the final persisted file will be the full executor report.

**INVARIANT**: When called with `status=PhaseStatus.PASS`, `_write_executor_result_file()` MUST produce output content containing `EXIT_RECOMMENDATION: CONTINUE`. This invariant is verified implicitly by T-003 (which asserts the phase result is `PASS`) and MUST be verified explicitly by asserting the final file content in T-003 (see §6).

### FR-004: Status Flow After Patch (exit_code == 0, no agent result file)

Post-patch flow:
```
exit_code == 0
→ _write_preliminary_result(config, phase, started_at.timestamp()):
    result_path.exists() → FALSE (or stale/empty)
    writes "EXIT_RECOMMENDATION: CONTINUE" to result_file
→ _determine_phase_status():
    exit_code == 0
    result_file.exists() → TRUE
    content = "EXIT_RECOMMENDATION: CONTINUE"
    has_halt = FALSE
    has_continue = TRUE
    → return PhaseStatus.PASS     ← FIXED
→ _write_executor_result_file() overwrites with full executor report
    (contains EXIT_RECOMMENDATION: CONTINUE)
```

### FR-005: Status Flow for Non-Zero Exit Codes (Unchanged)

For `exit_code != 0` (including 124/TIMEOUT, negative signal-kill codes such as -9/-15):
- `_write_preliminary_result()` is NOT called
- `_determine_phase_status()` executes the non-zero path identically to today
- `TIMEOUT`, `ERROR`, `INCOMPLETE`, `PASS_RECOVERED` all return as before

### FR-006: Prompt Injection in build_prompt()

In `process.py:ClaudeProcess.build_prompt()`, append a new `## Result File` section as the LAST section of the prompt, after the existing `## Important` section.

```python
f"## Important\n"
f"- This is Phase {pn} of a multi-phase sprint\n"
f"- Previous phases have already been executed in separate sessions\n"
f"- Do not re-execute work from prior phases\n"
f"- Focus only on the tasks defined in the phase file\n"
f"\n"
f"## Result File\n"
f"- When all tasks are complete, write this file: {config.result_file(self.phase).as_posix()}\n"
f"- Content must be exactly: EXIT_RECOMMENDATION: CONTINUE\n"
f"- If a STRICT-tier task fails and you halt early, write: EXIT_RECOMMENDATION: HALT\n"
f"- This file is read by the sprint executor to determine phase outcome."
```

**Constraint**: The injection MUST NOT change the location of `## Sprint Context`, `## Execution Rules`, or `## Scope Boundary` sections. The result file section is appended at the end.

**Constraint**: The injected path MUST use `config.result_file(self.phase).as_posix()` — the exact path the executor reads, formatted as a POSIX string for consistent cross-platform representation. Do NOT hardcode a path.

**Constraint**: The instruction MUST NOT prompt the agent to write HALT unless a STRICT-tier task fails. Unconditional HALT instructions would corrupt the flow.

**Constraint**: `## Result File` MUST be the last `##`-level section in the prompt. Verify with: `assert prompt.rindex("## Result File") > prompt.rindex("## Important")`.

**Verify attribute name**: The attribute `self.phase` in `build_prompt()` must match the actual attribute name set in `ClaudeProcess.__init__`. Confirm against the constructor before implementing — do not assume `self.phase` if the constructor uses a different name.

### FR-007: Agent-Written File Takes Precedence (Priority Preservation)

`_write_preliminary_result()` MUST NOT overwrite a fresh, non-empty agent-written result file. If `result_path.exists()` returns True AND `result_path.stat().st_size > 0` AND `result_path.stat().st_mtime >= started_at`, the function MUST return immediately without writing.

This replaces the erroneous v1.0.0 statement that the function "MUST overwrite" agent content.

**Consequence table**:

| Agent file state | `exists()` | `st_size` | `st_mtime` | `_write_preliminary_result()` action | `_determine_phase_status()` result |
|---|---|---|---|---|---|
| Not written (current bug) | False | — | — | Writes CONTINUE | PASS ✓ |
| Written CONTINUE (Option A success) | True | > 0 | >= started_at | No-op (fresh) | PASS ✓ |
| Written HALT (Option A, STRICT fail) | True | > 0 | >= started_at | No-op (fresh) | HALT ✓ |
| Written CONTINUE, 0 bytes (degenerate) | True | 0 | any | Overwrites with CONTINUE | PASS ✓ |
| Stale HALT from prior run | True | > 0 | < started_at | Overwrites with CONTINUE | PASS ✓ |
| Stale CONTINUE from prior run | True | > 0 | < started_at | Overwrites with CONTINUE | PASS ✓ |

---

## 4. Non-Functional Requirements

### NFR-001: Zero-Impact on Non-Zero Exit Paths

The guard `if exit_code == 0` is the single point of protection. No existing test for `TIMEOUT`, `ERROR`, `INCOMPLETE`, or `PASS_RECOVERED` must change behavior. The non-zero paths in `_determine_phase_status()` MUST produce identical results to today.

**Negative exit codes**: On Linux, a subprocess killed by a signal returns a negative `returncode` (e.g., `-9` for SIGKILL, `-15` for SIGTERM). These are non-zero and are excluded by the `exit_code == 0` guard. Verify that `_determine_phase_status()` handles `exit_code < 0` without exception — it must fall through to `ERROR` or `INCOMPLETE`, not raise.

### NFR-002: Atomicity and Concurrency

`_write_preliminary_result()` uses `result_path.write_text()` (single atomic write on POSIX). No partial writes are possible for the write itself.

**TOCTOU note**: The `exists()` / `stat()` checks and the subsequent `write_text()` are not atomic as a unit. In the current executor architecture, `execute_sprint()` processes phases sequentially in a single thread with no concurrent writers during the `exit_code == 0` window. This makes the TOCTOU window benign in practice. If the executor is ever parallelized to run phases concurrently, replace the `exists()`/`stat()` check with `os.open(..., os.O_WRONLY | os.O_CREAT | os.O_EXCL)` for atomic exclusive creation. Document this constraint in `_write_preliminary_result()`'s docstring.

### NFR-003: Test Suite Integrity

All existing tests must pass without modification. Before implementing, run `uv run pytest tests/sprint/ -v` and confirm no existing test asserts `PASS_NO_REPORT` as the expected output of `execute_sprint()` with `exit_code=0`. (Direct-call tests for `_determine_phase_status()` that assert `PASS_NO_REPORT` are unaffected — they bypass `execute_sprint()` entirely.)

### NFR-004: Backward Compatibility of _determine_phase_status()

`_determine_phase_status()` signature and behavior are unchanged. `PASS_NO_REPORT` remains a valid return value (reachable via direct calls in tests). The status `PASS_NO_REPORT` is not removed from `PhaseStatus` enum.

### NFR-005: File Path Determinism

`_write_preliminary_result()` MUST use `config.result_file(phase)` — the same path used by `_determine_phase_status()` (passed as `result_file=config.result_file(phase)`) and `_write_executor_result_file()`. All three functions operate on the same file path. No new path logic is introduced.

### NFR-006: Sentinel Contract

The string `EXIT_RECOMMENDATION: CONTINUE` is a sentinel value in the `_determine_phase_status()` parsing protocol. Any future modification to that parsing logic MUST remain compatible with this exact string. This sentinel contract MUST be documented as a comment in `_determine_phase_status()` at the point where it checks for `CONTINUE`.

### NFR-007: Option A Compliance Telemetry

The sprint log SHOULD record which path produced the result file for each phase: `agent-written` (Option A) or `executor-preliminary` (Option D). This enables measuring Option A compliance rate across sprints. Implementation: `_write_preliminary_result()` SHOULD return a boolean indicating whether it wrote the file. The call site in `execute_sprint()` logs the outcome at DEBUG level.

---

## 5. Broader Implication Analysis

### Implication 1: The `_write_executor_result_file()` Overwrite Chain

**Sequence after patch**:
1. `_write_preliminary_result()` → writes minimal `EXIT_RECOMMENDATION: CONTINUE` (or no-op if agent wrote fresh file)
2. `_determine_phase_status()` → reads file, returns `PhaseStatus.PASS`
3. `_write_executor_result_file(status=PhaseStatus.PASS, ...)` → overwrites with full executor report

The final file on disk is the full executor report. The preliminary file is transient (exists for ~microseconds between steps 1 and 3). Any downstream consumer that reads the result file AFTER the phase completes (e.g., the TUI, the logger, future pipeline steps) will always see the full executor report. The preliminary content is never exposed to downstream consumers. ✓

### Implication 2: Race Condition Between Preliminary Write and execute_sprint() Signal Check

Between `finished_at = datetime.now(timezone.utc)` and `_write_preliminary_result()`, the code checks `signal_handler.shutdown_requested` (line 690–693). If shutdown was requested during the poll loop:
- `logger.write_phase_interrupt(...)` is called
- `sprint_result.outcome = SprintOutcome.INTERRUPTED`
- `break` exits the phase loop

The `_write_preliminary_result()` call is placed **after** this signal check. If shutdown is requested, the break fires before `_write_preliminary_result()` runs. No preliminary file is written for interrupted phases. This is correct — an interrupted phase should not get `PASS` status. ✓

**Exact insertion order** (post-patch):
```python
# line 676
finished_at = datetime.now(timezone.utc)
# line 677-684: _phase_dur debug_log (existing)
# line 686-693: signal_handler.shutdown_requested check (existing)
#               → breaks loop if interrupted (no preliminary write)
# line 695: NEW _write_preliminary_result() guard
if exit_code == 0:
    _write_preliminary_result(config, phase, started_at.timestamp())
# line 696: existing _determine_phase_status()
status = _determine_phase_status(...)
```

**Signal handler ordering guarantee**: The signal check is evaluated once per phase, not continuously. A signal arriving after the check passes (returns False) but before `_write_preliminary_result()` completes will be caught at the start of the next phase iteration. This is correct — the current phase completes with its `exit_code`. Python's GIL ensures no interleaving of the signal check and write in the single-threaded executor. ✓

### Implication 3: Interaction with _classify_from_result_file() (Non-Zero Path)

`_classify_from_result_file()` is called only inside the `if exit_code != 0:` branch (lines 995–1003). Since `_write_preliminary_result()` only fires for `exit_code == 0`, there is zero interaction between the preliminary write and `_classify_from_result_file()`. The mtime freshness check at line 850 is irrelevant to this patch. ✓

### Implication 4: Mtime Freshness Guard

`_classify_from_result_file()` checks: `if started_at > 0 and mtime < started_at: return None`

Even if (hypothetically) `_classify_from_result_file()` were to read the preliminary file, the mtime freshness check would pass: `started_at` is captured at subprocess launch time (line 581), `_write_preliminary_result()` fires after subprocess exits (line ~697). File mtime is always > started_at. ✓

### Implication 5: Option A Prompt Injection — LLM Compliance Rate

The prompt injection (Option A) depends on agent compliance. Observed compliance in v2.25.5 was 0% (agent never wrote the file). The prompt injection adds explicit instructions; expected compliance rate after injection: 60–80% (LLMs generally follow explicit file write instructions when the path is concrete).

**When agent complies with CONTINUE** (fresh, non-empty file): `_write_preliminary_result()` detects fresh file → no-op. `_determine_phase_status()` reads the agent file. Returns `PhaseStatus.PASS`. `_write_executor_result_file()` overwrites with executor report. Final status: `pass`. ✓

**When agent complies with HALT** (fresh, non-empty file): No-op. `_determine_phase_status()` reads HALT. Returns `PhaseStatus.HALT`. Sprint halts correctly. ✓

**When agent doesn't comply (no file)**: Option D fires. Status: `pass`. ✓

**When agent writes garbage** (file exists but no recognized signal): If fresh + non-empty, `_write_preliminary_result()` skips. `_determine_phase_status()` falls through to `PASS_NO_SIGNAL`. This is a minor regression from Option D alone. Mitigation: the prompt injection instructs the agent to write EXACTLY `EXIT_RECOMMENDATION: CONTINUE` — garbage output is unlikely given explicit instruction.

**When agent writes zero bytes**: `st_size == 0` → treated as absent → `_write_preliminary_result()` overwrites with CONTINUE → `PhaseStatus.PASS`. ✓

### Implication 6: Stale File Risk — Mitigated by mtime Guard

If a stale result file from a **previous sprint run** exists at `results/phase-N-result.md`, its `st_mtime` will predate `started_at` (the launch time of the current subprocess). `_write_preliminary_result()` detects this via the mtime check and overwrites the stale file with `EXIT_RECOMMENDATION: CONTINUE`. `_determine_phase_status()` returns `PhaseStatus.PASS`. ✓

**Risk previously classified Low — upgraded to Medium** for repeated sprint re-runs in the same directory. Without the mtime fix (v1.0.0), a stale HALT file from a prior run would cause a deterministic and accumulated failure: every re-run in the same directory would HALT at the phase that previously failed, even after the underlying issue was resolved. The mtime guard in v1.1.0 fully mitigates this.

**Residual risk**: If the system clock is adjusted backward between sprint runs (NTP correction, VM clock skew), a stale file's mtime could appear newer than `started_at`. This is extremely unlikely in practice. Mitigated by the `_write_executor_result_file()` unconditional overwrite that always writes the correct final content.

### Implication 7: Double Write on _write_executor_result_file()

After the patch, `_write_executor_result_file()` always writes to `result_path.write_text(content)` (line 967), which is an unconditional overwrite. This overwrites both:
- The preliminary file (written by `_write_preliminary_result()`)
- Any agent-written file (Option A)

This is correct: the executor result file is always the authoritative final record. The comment at line 935–936 ("Overwrites any agent-written file — executor is authoritative") remains valid. ✓

### Implication 8: Test TestBackwardCompat.test_three_arg_call

This test (test_phase8_halt_fix.py:232-243) calls `_determine_phase_status()` directly with no result file and asserts `PASS_NO_REPORT`. This test continues to work correctly because it bypasses `execute_sprint()` entirely and calls `_determine_phase_status()` directly. `PASS_NO_REPORT` is still a valid return value from `_determine_phase_status()` when called directly without a result file. ✓

### Implication 9: Preflight Phases (python/skip mode)

Phases with `execution_mode == "python"` or `execution_mode == "skip"` are handled by `execute_preflight_phases()` (called before the main loop, line 533) and are skipped in the main loop at lines 542–543. The preliminary write logic in the main loop is never reached for python/skip phases. These phases continue to use `PhaseStatus.PREFLIGHT_PASS`. ✓

---

## 6. Test Requirements

### T-001: _write_preliminary_result() writes CONTINUE content (unit)

```python
def test_write_preliminary_result_creates_file_with_continue(tmp_path):
    config = _make_config(tmp_path)
    phase = config.phases[0]
    (tmp_path / "results").mkdir(exist_ok=True)
    started_at = datetime.now(timezone.utc).timestamp() - 1  # 1s ago
    from superclaude.cli.sprint.executor import _write_preliminary_result
    _write_preliminary_result(config, phase, started_at)
    content = config.result_file(phase).read_text()
    assert "EXIT_RECOMMENDATION: CONTINUE" in content
    assert "EXIT_RECOMMENDATION: HALT" not in content
```

### T-002: _write_preliminary_result() skips fresh non-empty HALT file (unit)

```python
def test_write_preliminary_result_skips_if_fresh_nonempty_file_exists(tmp_path):
    config = _make_config(tmp_path)
    phase = config.phases[0]
    (tmp_path / "results").mkdir(exist_ok=True)
    config.result_file(phase).write_text("EXIT_RECOMMENDATION: HALT\n")
    # started_at is in the past so the file is "fresh" (mtime >= started_at)
    started_at = datetime.now(timezone.utc).timestamp() - 5
    from superclaude.cli.sprint.executor import _write_preliminary_result
    _write_preliminary_result(config, phase, started_at)
    content = config.result_file(phase).read_text()
    # Must not have been overwritten — HALT preserved
    assert "EXIT_RECOMMENDATION: HALT" in content
```

### T-002b: _write_preliminary_result() overwrites zero-byte file (unit)

```python
def test_write_preliminary_result_overwrites_zero_byte_file(tmp_path):
    """Zero-byte agent file (degenerate write) must be treated as absent."""
    config = _make_config(tmp_path)
    phase = config.phases[0]
    (tmp_path / "results").mkdir(exist_ok=True)
    config.result_file(phase).write_text("")  # 0 bytes
    started_at = datetime.now(timezone.utc).timestamp() - 5
    from superclaude.cli.sprint.executor import _write_preliminary_result
    _write_preliminary_result(config, phase, started_at)
    content = config.result_file(phase).read_text()
    assert "EXIT_RECOMMENDATION: CONTINUE" in content
```

### T-003: execute_sprint() produces PhaseStatus.PASS (not PASS_NO_REPORT) for exit_code=0 with no agent-written result file (integration)

```python
def test_execute_sprint_pass_not_pass_no_report_when_no_result_file(tmp_path):
    """After patch: exit_code=0 + no agent result file → PhaseStatus.PASS."""
    config = _make_config(tmp_path, num_phases=1)
    phase = config.active_phases[0]
    captured_results = []

    class _FakePopen:
        pid = 9100
        returncode = 0
        def poll(self): return 0
        def wait(self, timeout=None): return 0
        def terminate(self): pass
        def kill(self): pass

    # NOTE: Do NOT pre-write the result file (simulates agent non-compliance)
    with (
        patch("shutil.which", return_value="/usr/bin/claude"),
        patch("superclaude.cli.sprint.process._subprocess.Popen", return_value=_FakePopen()),
        patch("superclaude.cli.sprint.executor.SprintTUI") as mock_tui,
        patch("superclaude.cli.sprint.executor.SprintLogger") as mock_logger,
        patch("superclaude.cli.sprint.executor.OutputMonitor") as mock_monitor,
        patch("superclaude.cli.sprint.executor.notify_phase_complete"),
        patch("superclaude.cli.sprint.executor.notify_sprint_complete"),
    ):
        _setup_tui_monitor_mocks(mock_tui, mock_monitor)
        mock_logger.return_value.write_summary = MagicMock(
            side_effect=lambda sr: captured_results.append(sr)
        )
        # Create output file (agent produced output)
        config.results_dir.mkdir(exist_ok=True)
        config.output_file(phase).write_text('{"type":"result","subtype":"success"}\n')
        try:
            execute_sprint(config)
        except SystemExit:
            pass

    assert len(captured_results) >= 1
    phase_result = captured_results[0].phase_results[0]
    assert phase_result.status == PhaseStatus.PASS, (
        f"Expected PASS after patch, got {phase_result.status}"
    )
    # Verify final file on disk contains CONTINUE (FR-003 invariant)
    final_content = config.result_file(phase).read_text()
    assert "EXIT_RECOMMENDATION: CONTINUE" in final_content, (
        "Final result file must contain CONTINUE after executor overwrite"
    )
```

### T-004: Preliminary write does NOT fire for non-zero exit_code (unit)

```python
def test_write_preliminary_result_not_called_for_nonzero_exit(tmp_path):
    """Validate the guard: _write_preliminary_result is never called for exit_code != 0."""
    config = _make_config(tmp_path, num_phases=1)
    phase = config.active_phases[0]

    class _FakeFailPopen:
        pid = 9101
        returncode = 1
        def poll(self): return 1
        def wait(self, timeout=None): return 1
        def terminate(self): pass
        def kill(self): pass

    with (
        patch("shutil.which", return_value="/usr/bin/claude"),
        patch("superclaude.cli.sprint.process._subprocess.Popen", return_value=_FakeFailPopen()),
        patch("superclaude.cli.sprint.executor.SprintTUI") as mock_tui,
        patch("superclaude.cli.sprint.executor.SprintLogger"),
        patch("superclaude.cli.sprint.executor.OutputMonitor") as mock_monitor,
        patch("superclaude.cli.sprint.executor.notify_phase_complete"),
        patch("superclaude.cli.sprint.executor.notify_sprint_complete"),
        patch("superclaude.cli.sprint.executor.DiagnosticCollector"),
        patch("superclaude.cli.sprint.executor.FailureClassifier"),
        patch("superclaude.cli.sprint.executor.ReportGenerator"),
        patch("superclaude.cli.sprint.executor._write_preliminary_result") as mock_prelim,
    ):
        _setup_tui_monitor_mocks(mock_tui, mock_monitor)
        config.results_dir.mkdir(exist_ok=True)
        config.output_file(phase).write_text('{"type":"result","subtype":"error"}\n')
        try:
            execute_sprint(config)
        except SystemExit:
            pass

    mock_prelim.assert_not_called()
```

### T-005: build_prompt() contains Result File section (unit)

```python
def test_build_prompt_contains_result_file_section(tmp_path):
    config = _make_config(tmp_path)
    phase = config.active_phases[0]
    from superclaude.cli.sprint.process import ClaudeProcess
    proc = ClaudeProcess.__new__(ClaudeProcess)
    proc.config = config
    proc.phase = phase  # adjust attribute name to match actual __init__ if different
    prompt = proc.build_prompt()
    assert "## Result File" in prompt
    assert "EXIT_RECOMMENDATION: CONTINUE" in prompt
    assert str(config.result_file(phase)) in prompt
    # Result File must be the LAST ##-level section
    assert prompt.rindex("## Result File") > prompt.rindex("## Important")
    # HALT instruction must be conditional on STRICT-tier failure
    assert "STRICT" in prompt or "strict" in prompt.lower()
    # Instruction must be conditional, not unconditional
    assert "if" in prompt.lower()
```

### T-006: Stale HALT file from prior run does not cause incorrect HALT (integration)

```python
def test_stale_halt_file_does_not_cause_incorrect_halt(tmp_path):
    """
    Given:  A stale HALT result file from a prior sprint run exists
    When:   A new sprint run executes Phase N with exit_code=0
    Then:   The stale HALT file must NOT cause the phase to be marked HALT.
            The mtime guard in _write_preliminary_result() overwrites it with CONTINUE.
    """
    config = _make_config(tmp_path, num_phases=1)
    phase = config.active_phases[0]
    captured_results = []

    # Pre-create stale HALT file (simulate prior failed run)
    config.results_dir.mkdir(exist_ok=True)
    stale_file = config.result_file(phase)
    stale_file.write_text("EXIT_RECOMMENDATION: HALT\n")
    # Back-date the file to before any reasonable started_at
    import os, time
    stale_mtime = time.time() - 3600  # 1 hour ago
    os.utime(stale_file, (stale_mtime, stale_mtime))

    class _FakePopen:
        pid = 9102
        returncode = 0
        def poll(self): return 0
        def wait(self, timeout=None): return 0
        def terminate(self): pass
        def kill(self): pass

    with (
        patch("shutil.which", return_value="/usr/bin/claude"),
        patch("superclaude.cli.sprint.process._subprocess.Popen", return_value=_FakePopen()),
        patch("superclaude.cli.sprint.executor.SprintTUI") as mock_tui,
        patch("superclaude.cli.sprint.executor.SprintLogger") as mock_logger,
        patch("superclaude.cli.sprint.executor.OutputMonitor") as mock_monitor,
        patch("superclaude.cli.sprint.executor.notify_phase_complete"),
        patch("superclaude.cli.sprint.executor.notify_sprint_complete"),
    ):
        _setup_tui_monitor_mocks(mock_tui, mock_monitor)
        mock_logger.return_value.write_summary = MagicMock(
            side_effect=lambda sr: captured_results.append(sr)
        )
        config.output_file(phase).write_text('{"type":"result","subtype":"success"}\n')
        try:
            execute_sprint(config)
        except SystemExit:
            pass

    assert len(captured_results) >= 1
    phase_result = captured_results[0].phase_results[0]
    assert phase_result.status == PhaseStatus.PASS, (
        f"Stale HALT file caused incorrect HALT — mtime guard failed. Got: {phase_result.status}"
    )
```

---

## 7. Exact Code Changes

### Change 1: executor.py — Add _write_preliminary_result()

**Function definition location**: After `_write_crash_recovery_log()` (line ~922), before `_write_executor_result_file()` (line ~925). This is the **definition** placement. The **call site** is in `execute_sprint()` — see Change 2.

```python
def _write_preliminary_result(
    config: SprintConfig,
    phase: Phase,
    started_at: float,
) -> bool:
    """Write a minimal preliminary result file before status determination.

    Called by execute_sprint() ONLY when exit_code == 0. The caller is
    responsible for the guard. Non-zero exit paths must never trigger this write.

    Ensures _determine_phase_status() finds a result file with
    EXIT_RECOMMENDATION: CONTINUE and returns PhaseStatus.PASS instead of
    falling through to PASS_NO_REPORT.

    Skips the write if the agent already wrote a fresh, non-empty result file
    (Option A success). "Fresh" means mtime >= started_at (written during this
    subprocess run). "Non-empty" means st_size > 0.

    Returns True if this function wrote the file (Option D path), False if it
    was a no-op (Option A path or OSError). Used by the call site for telemetry.

    ORDERING INVARIANT: This function MUST be called BEFORE _determine_phase_status()
    and BEFORE _write_executor_result_file(). Do not reorder these three calls.

    CONCURRENCY NOTE: The exists()/stat() check and write_text() are not atomic.
    This is safe in the current single-threaded executor. If phases are ever run
    concurrently, replace with os.open(..., os.O_WRONLY | os.O_CREAT | os.O_EXCL).

    SENTINEL CONTRACT: The string 'EXIT_RECOMMENDATION: CONTINUE' is a sentinel
    parsed by _determine_phase_status(). Any change to that parsing logic must
    remain compatible with this exact content.
    """
    result_path = config.result_file(phase)
    if result_path.exists():
        try:
            stat = result_path.stat()
            if stat.st_size > 0 and stat.st_mtime >= started_at:
                # Fresh, non-empty agent-written file — preserve it (may contain HALT)
                return False
        except OSError:
            pass  # Can't stat — fall through to write attempt
    try:
        result_path.parent.mkdir(parents=True, exist_ok=True)
        result_path.write_text("EXIT_RECOMMENDATION: CONTINUE\n")
        return True
    except OSError as e:
        import logging as _logging
        _logging.getLogger(__name__).warning(
            "preliminary result write failed: %s; phase may report PASS_NO_REPORT", e
        )
        return False
```

### Change 2: executor.py — Inject call in execute_sprint()

**Call site location**: In the main phase loop body, between the signal_handler check (line ~690–693) and `_determine_phase_status()` call (line ~696).

**Before** (existing, line ~695–704):
```python
                # Determine phase status
                status = _determine_phase_status(
                    exit_code=exit_code,
                    result_file=config.result_file(phase),
                    output_file=config.output_file(phase),
                    config=config,
                    phase=phase,
                    started_at=started_at.timestamp(),
                    error_file=config.error_file(phase),
                )
```

**After** (with injection):
```python
                # Option D: Write preliminary result file before status determination.
                # Fires only for exit_code == 0. Non-zero paths are unaffected.
                # If the agent already wrote a fresh, non-empty result file (Option A),
                # this is a no-op. Stale files (mtime < started_at) are overwritten.
                # ORDERING INVARIANT: this call MUST precede _determine_phase_status()
                # and _write_executor_result_file(). Do not reorder.
                if exit_code == 0:
                    _wrote_preliminary = _write_preliminary_result(
                        config, phase, started_at.timestamp()
                    )
                    debug_log(
                        f"preliminary_result_write path={'option_d' if _wrote_preliminary else 'option_a_or_noop'}"
                    )

                # Determine phase status
                status = _determine_phase_status(
                    exit_code=exit_code,
                    result_file=config.result_file(phase),
                    output_file=config.output_file(phase),
                    config=config,
                    phase=phase,
                    started_at=started_at.timestamp(),
                    error_file=config.error_file(phase),
                )
```

### Change 3: process.py — Append Result File section to build_prompt()

**Location**: `ClaudeProcess.build_prompt()` return statement (line ~166–193).

**Before** (end of return string):
```python
        f"## Important\n"
        f"- This is Phase {pn} of a multi-phase sprint\n"
        f"- Previous phases have already been executed in separate sessions\n"
        f"- Do not re-execute work from prior phases\n"
        f"- Focus only on the tasks defined in the phase file"
```

**After**:
```python
        f"## Important\n"
        f"- This is Phase {pn} of a multi-phase sprint\n"
        f"- Previous phases have already been executed in separate sessions\n"
        f"- Do not re-execute work from prior phases\n"
        f"- Focus only on the tasks defined in the phase file\n"
        f"\n"
        f"## Result File\n"
        f"- When all tasks are complete, write this file: {config.result_file(self.phase).as_posix()}\n"
        f"- Content must be exactly: EXIT_RECOMMENDATION: CONTINUE\n"
        f"- If a STRICT-tier task fails and you halt early, write: EXIT_RECOMMENDATION: HALT\n"
        f"- This file is read by the sprint executor to determine phase outcome."
```

**Note**: Verify that `self.phase` matches the actual attribute name in `ClaudeProcess.__init__`. If it differs (e.g., `self._phase`), use the correct name.

**Note**: `## Result File` MUST be the last `##`-level heading in the returned string. Do not insert additional sections after it.

---

## 8. Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|-----------|
| Stale agent-written HALT file from prior run causes incorrect HALT | ~~Low~~ **Medium** (for repeated re-runs in same dir) | High | **Mitigated in v1.1.0** by mtime guard in `_write_preliminary_result()` |
| Agent writes zero-byte file → PASS_NO_SIGNAL re-introduced | Low | Medium | **Mitigated in v1.1.0** by `st_size > 0` check; zero-byte file overwritten with CONTINUE |
| Agent writes garbage file (non-empty, no signal) → PASS_NO_SIGNAL | Low | Low | Explicit prompt reduces probability; PASS_NO_SIGNAL is still is_success=True |
| OSError on preliminary write → falls back to PASS_NO_REPORT | Very Low | Low | try/except with WARNING log; behavior identical to current state |
| Option A prompt causes agent to write file to wrong path | Low | Medium | as_posix() f-string injection uses config.result_file(phase) — exact path |
| TOCTOU race between exists() and write_text() | Very Low (single-threaded) | High (if triggered) | Documented in NFR-002; mitigate with O_EXCL if parallelism added |
| Existing tests fail due to patch | None | — | NFR-003 requires pre-implementation test run to verify |

---

## 9. Acceptance Criteria

- [ ] `_write_preliminary_result()` exists and is importable from `executor.py`
- [ ] `_write_preliminary_result()` accepts `started_at: float` as third parameter
- [ ] `uv run pytest tests/sprint/test_executor.py -v` passes with 0 failures
- [ ] `uv run pytest tests/sprint/test_phase8_halt_fix.py -v` passes with 0 failures
- [ ] New test T-003 (`test_execute_sprint_pass_not_pass_no_report_when_no_result_file`) passes
- [ ] New test T-002b (`test_write_preliminary_result_overwrites_zero_byte_file`) passes
- [ ] New test T-006 (`test_stale_halt_file_does_not_cause_incorrect_halt`) passes
- [ ] Sprint re-run of v2.25.5 reports `pass` (not `pass_no_report`) for phases 1–5
- [ ] Sprint re-run in same output directory (with stale result files from prior run) produces `pass` (not `HALT`) for phases that succeed
- [ ] `PhaseStatus.PASS_NO_REPORT` remains in the enum (backward compatibility)
- [ ] `_determine_phase_status()` direct-call tests for `PASS_NO_REPORT` continue to pass
- [ ] `uv run pytest tests/sprint/ -v` full suite: 0 regressions
- [ ] Pre-implementation baseline: `uv run pytest tests/sprint/ -v` passes before any code changes

---

## 10. Out of Scope

- Removing `PASS_NO_REPORT` from `PhaseStatus` enum
- Cleaning stale result files between sprint runs (mitigated by mtime guard; full cleanup remains out of scope)
- Modifying `_determine_phase_status()` signature or priority chain
- Changing how `execute_phase_tasks()` / `_run_task_subprocess()` builds prompts (separate code path from `execute_sprint()`)
- Replacing `write_text()` with `O_EXCL` atomic creation (deferred until executor is parallelized; documented in NFR-002)
