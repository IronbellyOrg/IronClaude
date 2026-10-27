---
spec_source: pass-no-report-fix-spec.md
generated: "2026-03-16T00:00:00Z"
generator: requirements-extraction-specialist-v1
functional_requirements: 9
nonfunctional_requirements: 7
total_requirements: 16
complexity_score: 0.62
complexity_class: moderate
domains_detected: 5
risks_identified: 7
dependencies_identified: 8
success_criteria_count: 13
extraction_mode: full
pipeline_diagnostics: {elapsed_seconds: 123.0, started_at: "2026-03-16T14:17:23.861189+00:00", finished_at: "2026-03-16T14:19:26.878170+00:00"}
---

## Functional Requirements

**FR-001: `_write_preliminary_result()` Function**
A new module-level function `_write_preliminary_result(config: SprintConfig, phase: Phase, started_at: float) -> bool` MUST be added to `executor.py` with the following behavior:
- Derives `result_path = config.result_file(phase)`
- Returns immediately (no-op, returns `False`) if result file exists AND `st_size > 0` AND `st_mtime >= started_at`
- Treats zero-byte files (`st_size == 0`) as absent — proceeds to write
- Treats stale files (`st_mtime < started_at`) as absent — proceeds to overwrite
- Creates parent directory with `mkdir(parents=True, exist_ok=True)` before writing
- Writes exactly `EXIT_RECOMMENDATION: CONTINUE\n` to the result path
- Wraps the write in `try/except OSError` — on failure, emits WARNING via module logger and returns `False`
- Returns `True` if it wrote the file (Option D path), `False` if no-op or error
- MUST NOT accept `exit_code` as a parameter (caller guards on `exit_code == 0`)

**Content invariants for the written file:**
- MUST contain `EXIT_RECOMMENDATION: CONTINUE`
- MUST NOT contain `EXIT_RECOMMENDATION: HALT`
- MUST NOT contain `status: FAIL`, `status: FAILED`, or `status: PARTIAL`

**FR-002: Injection Site in `execute_sprint()`**
In `executor.py:execute_sprint()`, a call to `_write_preliminary_result()` MUST be inserted between `finished_at = datetime.now(timezone.utc)` / signal handler check and the call to `_determine_phase_status()`, guarded by `if exit_code == 0`. The guard is a hard requirement — non-zero exit paths MUST NOT be affected. `started_at.timestamp()` (float) MUST be passed as the third argument. The result (`_wrote_preliminary`) MUST be logged at DEBUG level with the path taken (`option_d` or `option_a_or_noop`).

**FR-003: `_write_executor_result_file()` Overwrite Behavior**
The existing `_write_executor_result_file()` call MUST remain in place and unchanged. It fires AFTER `_determine_phase_status()` and unconditionally overwrites the preliminary result with the full executor report. When called with `status=PhaseStatus.PASS`, the output content MUST contain `EXIT_RECOMMENDATION: CONTINUE`.

**FR-004: Status Flow for `exit_code == 0` with No Agent File**
Post-patch, the execution flow for `exit_code == 0` and no pre-existing agent result file MUST be:
1. `_write_preliminary_result()` writes `EXIT_RECOMMENDATION: CONTINUE`
2. `_determine_phase_status()` reads the file, returns `PhaseStatus.PASS` (not `PASS_NO_REPORT`)
3. `_write_executor_result_file()` overwrites with full executor report containing `EXIT_RECOMMENDATION: CONTINUE`

**FR-005: Status Flow for Non-Zero Exit Codes**
For `exit_code != 0` (including 124/TIMEOUT and negative signal-kill codes such as `-9`/`-15`):
- `_write_preliminary_result()` MUST NOT be called
- `_determine_phase_status()` MUST execute identically to pre-patch behavior
- `TIMEOUT`, `ERROR`, `INCOMPLETE`, `PASS_RECOVERED` MUST all return as before
- `_determine_phase_status()` MUST NOT raise on `exit_code < 0`; negative codes MUST fall through to `ERROR` or `INCOMPLETE`

**FR-006: Prompt Injection in `build_prompt()`**
In `process.py:ClaudeProcess.build_prompt()`, a new `## Result File` section MUST be appended as the LAST section of the prompt, after the existing `## Important` section, containing:
- The exact result file path via `config.result_file(self.phase).as_posix()` — no hardcoded paths
- Instruction: `Content must be exactly: EXIT_RECOMMENDATION: CONTINUE`
- Conditional HALT instruction: only when a STRICT-tier task fails
- `## Result File` MUST be the last `##`-level heading (verified by `prompt.rindex("## Result File") > prompt.rindex("## Important")`)
- MUST NOT reposition existing sections (`## Sprint Context`, `## Execution Rules`, `## Scope Boundary`)
- `self.phase` attribute name MUST match the actual `ClaudeProcess.__init__` attribute before implementing

**FR-007: Agent-Written File Priority Preservation**
`_write_preliminary_result()` MUST NOT overwrite a fresh, non-empty agent-written result file. The freshness condition is: `exists()` AND `st_size > 0` AND `st_mtime >= started_at`. This preserves agent-written `HALT` signals from STRICT-tier task failures. See consequence table (§3 FR-007) for all state transitions.

**FR-008: Ordering Invariant**
The three operations `_write_preliminary_result()`, `_determine_phase_status()`, and `_write_executor_result_file()` form an ordered triple. Their relative execution order MUST NOT be changed by any future refactoring. This invariant MUST be documented in `_write_preliminary_result()`'s docstring.

**FR-009: Preflight Phase Isolation**
Phases with `execution_mode == "python"` or `execution_mode == "skip"` are handled by `execute_preflight_phases()` and are skipped in the main loop. The preliminary write logic MUST NOT be reached for python/skip phases — they MUST continue to use `PhaseStatus.PREFLIGHT_PASS` unchanged.

---

## Non-Functional Requirements

**NFR-001: Zero-Impact on Non-Zero Exit Paths**
No existing test for `TIMEOUT`, `ERROR`, `INCOMPLETE`, or `PASS_RECOVERED` may change behavior. The `exit_code == 0` guard is the single protection point. Negative exit codes (`< 0`) must be handled without exception by `_determine_phase_status()`.

**NFR-002: Atomicity and Concurrency**
`_write_preliminary_result()` uses `result_path.write_text()` (single atomic POSIX write). The `exists()`/`stat()`/`write_text()` sequence is not atomic as a unit, but is safe under the current single-threaded sequential executor. If phases are ever parallelized, this MUST be replaced with `os.open(..., os.O_WRONLY | os.O_CREAT | os.O_EXCL)`. This constraint MUST be documented in the function's docstring.

**NFR-003: Test Suite Integrity**
All existing tests MUST pass without modification. Pre-implementation baseline: `uv run pytest tests/sprint/ -v` MUST pass before any code changes. No existing test that asserts `PASS_NO_REPORT` as the output of `execute_sprint()` with `exit_code=0` must exist — verify before implementing. Direct-call tests for `_determine_phase_status()` asserting `PASS_NO_REPORT` are unaffected and must continue to pass.

**NFR-004: Backward Compatibility of `_determine_phase_status()`**
The signature and behavior of `_determine_phase_status()` MUST remain unchanged. `PASS_NO_REPORT` MUST remain a valid return value (reachable via direct calls). `PhaseStatus.PASS_NO_REPORT` MUST NOT be removed from the enum.

**NFR-005: File Path Determinism**
`_write_preliminary_result()` MUST use `config.result_file(phase)` — the identical path used by `_determine_phase_status()` and `_write_executor_result_file()`. No new path logic is introduced.

**NFR-006: Sentinel Contract**
The string `EXIT_RECOMMENDATION: CONTINUE` is a sentinel parsed by `_determine_phase_status()`. Any future change to that parsing logic MUST remain compatible with this exact string. This sentinel contract MUST be documented as a comment in `_determine_phase_status()` at the point where it checks for `CONTINUE`.

**NFR-007: Option A Compliance Telemetry**
The sprint log SHOULD record which path produced the result file per phase: `agent-written` (Option A) or `executor-preliminary` (Option D). `_write_preliminary_result()` MUST return a boolean enabling this distinction. The call site in `execute_sprint()` MUST log the outcome at DEBUG level.

---

## Complexity Assessment

**complexity_score: 0.62**
**complexity_class: moderate**

**Rationale:**

| Factor | Weight | Score | Notes |
|---|---|---|---|
| Code change surface area | Low | 0.3 | Three localized changes in 2 files; no schema changes |
| State sequencing criticality | High | 0.8 | Strict ordering invariant across 3 functions; incorrect order causes data corruption |
| Edge case density | Medium | 0.65 | 5 distinct file-state branches (absent, fresh CONTINUE, fresh HALT, zero-byte, stale); mtime guard adds temporal dimension |
| Concurrency hazard | Low-Medium | 0.4 | TOCTOU documented and benign now, but latent high-impact if parallelism added |
| Test complexity | Medium | 0.6 | 6 tests including 2 full integration mocks with Popen patching |
| Backward compatibility constraints | Medium | 0.5 | Must not alter `_determine_phase_status()` or remove `PASS_NO_REPORT`; must not break direct-call tests |
| LLM compliance dependency | Medium | 0.55 | Option A is probabilistic (60–80% expected); Option D is the deterministic fallback |

The fix is mechanically small but requires careful attention to execution ordering, mtime-based freshness semantics, and the interaction between two defensive layers (Option D + Option A). The primary risk surface is the ordering invariant and stale-file edge cases, not algorithmic complexity.

---

## Architectural Constraints

1. **Executor authority**: `executor.py` comment at line 706–707 establishes the executor as authoritative. Preliminary writes and final overwrites must follow this principle — agent-written files are advisory, executor-written files are final.

2. **Single-threaded sequential execution**: The current executor processes phases sequentially in a single thread. The `_write_preliminary_result()` design assumes no concurrent writers during the `exit_code == 0` window. Any future parallelization requires replacing `exists()`/`stat()`/`write_text()` with `os.open(..., O_EXCL)`.

3. **Path determinism via `config.result_file(phase)`**: All three functions (`_write_preliminary_result`, `_determine_phase_status`, `_write_executor_result_file`) MUST operate on the same file path returned by `config.result_file(phase)`. No independent path construction is permitted.

4. **Ordered triple invariant**: `_write_preliminary_result()` → `_determine_phase_status()` → `_write_executor_result_file()` is a hard execution ordering constraint. Refactoring that reorders these three calls is forbidden.

5. **Guard isolation**: The `if exit_code == 0:` guard is the sole protection for non-zero exit paths. `_write_preliminary_result()` must not internally check `exit_code` — this responsibility belongs exclusively to the call site.

6. **No changes to `_determine_phase_status()` signature or priority chain**: The classifier is treated as a black box. The fix operates by preparing its input (result file presence), not by modifying its logic.

7. **Preflight phase isolation**: `execute_preflight_phases()` runs before the main loop; the preliminary write logic in the main loop is architecturally unreachable for python/skip phases.

8. **Signal handler check precedes preliminary write**: The shutdown signal check at lines 690–693 must remain before the preliminary write call. If shutdown is requested, the loop breaks before the write fires.

9. **Cross-platform path representation**: `config.result_file(self.phase).as_posix()` must be used in prompt injection to ensure consistent path formatting across platforms.

10. **No modification to `execute_phase_tasks()` / `_run_task_subprocess()`**: These are separate code paths from `execute_sprint()` and are out of scope.

---

## Risk Inventory

**RISK-001** — Stale agent-written HALT file from prior run causes incorrect HALT
- **Severity**: Medium (upgraded from Low in v1.1.0)
- **Trigger**: Repeated sprint re-runs in the same output directory where a prior run left a HALT result file
- **Mitigation**: mtime guard in `_write_preliminary_result()` — file with `st_mtime < started_at` is overwritten with CONTINUE. Verified by T-006.

**RISK-002** — Agent writes zero-byte file → `PASS_NO_SIGNAL` re-introduced
- **Severity**: Low
- **Trigger**: Agent produces a result file but writes 0 bytes (degenerate LLM behavior)
- **Mitigation**: `st_size > 0` check treats zero-byte files as absent; `_write_preliminary_result()` overwrites with CONTINUE. Verified by T-002b.

**RISK-003** — Agent writes garbage file (non-empty, no recognized signal) → `PASS_NO_SIGNAL`
- **Severity**: Low
- **Trigger**: Agent writes non-empty content that contains neither CONTINUE nor HALT
- **Mitigation**: Explicit prompt reduces probability. `PASS_NO_SIGNAL` remains `is_success=True`; acceptable degradation.

**RISK-004** — `OSError` on preliminary write → falls back to `PASS_NO_REPORT`
- **Severity**: Low (Very Low probability)
- **Trigger**: Filesystem permission error or disk full during `result_path.write_text()`
- **Mitigation**: `try/except OSError` with WARNING log; behavior is identical to current pre-patch state (no regression, graceful degradation).

**RISK-005** — Option A prompt causes agent to write file to wrong path
- **Severity**: Medium
- **Trigger**: LLM misinterprets or truncates the injected path; writes to a relative or incorrect location
- **Mitigation**: Path injected via `config.result_file(phase).as_posix()` — exact absolute path. Option D provides deterministic fallback if agent writes to wrong location.

**RISK-006** — TOCTOU race between `exists()`/`stat()` check and `write_text()`
- **Severity**: High (if triggered); Very Low (current architecture)
- **Trigger**: Concurrent writer modifies the file between the check and the write
- **Mitigation**: Current single-threaded executor makes this benign. Documented in NFR-002; mitigation (`O_EXCL`) deferred to if/when parallelism is added.

**RISK-007** — Existing tests fail due to patch
- **Severity**: None (by NFR-003 pre-condition)
- **Trigger**: Pre-existing test asserts `PASS_NO_REPORT` from `execute_sprint()` with `exit_code=0`
- **Mitigation**: NFR-003 requires running `uv run pytest tests/sprint/ -v` as a baseline before implementing. If such a test exists, it must be analyzed before proceeding.

---

## Dependency Inventory

**DEP-001**: `src/superclaude/cli/sprint/executor.py` — Primary edit target; contains `execute_sprint()`, `_determine_phase_status()`, `_write_executor_result_file()`, `_write_crash_recovery_log()`

**DEP-002**: `src/superclaude/cli/sprint/process.py` — Secondary edit target; contains `ClaudeProcess.build_prompt()` and `ClaudeProcess.__init__`

**DEP-003**: `src/superclaude/cli/sprint/models.py` — Provides `SprintConfig`, `Phase`, `PhaseStatus`, `SprintOutcome`; `config.result_file(phase)`, `config.output_file(phase)`, `config.results_dir`

**DEP-004**: `tests/sprint/test_executor.py` — Existing test file; new tests T-001, T-002, T-002b, T-004, T-005 added here

**DEP-005**: `tests/sprint/test_phase8_halt_fix.py` — Existing test file; new tests T-003, T-006 added here; contains `TestBackwardCompat.test_three_arg_call` which must continue passing

**DEP-006**: Python standard library — `pathlib.Path` (`write_text`, `exists`, `stat`, `mkdir`), `os` (`utime`, `open`, `O_WRONLY`, `O_CREAT`, `O_EXCL`), `logging`, `datetime`, `timezone`

**DEP-007**: `unittest.mock` — `patch`, `MagicMock` for test infrastructure; patching of `shutil.which`, `subprocess.Popen`, `SprintTUI`, `SprintLogger`, `OutputMonitor`, notification functions, `DiagnosticCollector`, `FailureClassifier`, `ReportGenerator`

**DEP-008**: UV Python environment — `uv run pytest tests/sprint/ -v` required for pre-implementation baseline and acceptance verification

---

## Success Criteria

**SC-001**: `_write_preliminary_result()` is importable from `executor.py` with the exact signature `(config: SprintConfig, phase: Phase, started_at: float) -> bool`

**SC-002**: `uv run pytest tests/sprint/test_executor.py -v` passes with 0 failures

**SC-003**: `uv run pytest tests/sprint/test_phase8_halt_fix.py -v` passes with 0 failures

**SC-004**: T-003 (`test_execute_sprint_pass_not_pass_no_report_when_no_result_file`) passes — `exit_code=0` + no agent result file → `PhaseStatus.PASS` (not `PASS_NO_REPORT`)

**SC-005**: T-003 final file content assertion passes — `config.result_file(phase).read_text()` contains `EXIT_RECOMMENDATION: CONTINUE` after executor overwrite

**SC-006**: T-002b (`test_write_preliminary_result_overwrites_zero_byte_file`) passes — zero-byte agent file treated as absent, overwritten with CONTINUE

**SC-007**: T-006 (`test_stale_halt_file_does_not_cause_incorrect_halt`) passes — stale HALT file from prior run does not cause `PhaseStatus.HALT` in a new run with `exit_code=0`

**SC-008**: Sprint re-run of v2.25.5 reports `pass` (not `pass_no_report`) for phases 1–5

**SC-009**: Sprint re-run in the same output directory (with stale result files from a prior run) produces `pass` (not `HALT`) for phases that succeed

**SC-010**: `PhaseStatus.PASS_NO_REPORT` remains in the enum — `uv run pytest` passes with 0 regressions on all direct-call tests for `_determine_phase_status()`

**SC-011**: `uv run pytest tests/sprint/ -v` full suite: 0 regressions

**SC-012**: Pre-implementation baseline — `uv run pytest tests/sprint/ -v` passes before any code changes are made

**SC-013**: `build_prompt()` prompt string satisfies `prompt.rindex("## Result File") > prompt.rindex("## Important")` — `## Result File` is the last `##`-level section

---

## Open Questions

**OQ-001**: **`ClaudeProcess` attribute name** — The spec instructs implementers to verify whether `self.phase` matches the actual attribute set in `ClaudeProcess.__init__` (it may be `self._phase` or another name). This must be confirmed by reading the constructor before implementing FR-006 / Change 3.

**OQ-002**: **Exact line numbers for injection in `execute_sprint()`** — The spec references approximate line numbers (~581 for `started_at`, ~676 for `finished_at`, ~690–693 for signal handler check, ~695–704 for `_determine_phase_status()` call). These must be verified against the current file state before applying Change 2, as intervening commits may have shifted them.

**OQ-003**: **Exact insertion point for `_write_preliminary_result()` definition** — The spec says "after `_write_crash_recovery_log()` (line ~922), before `_write_executor_result_file()` (line ~925)." Verify these functions exist at those approximate locations before inserting.

**OQ-004**: **`_classify_from_result_file()` interaction with mtime** — The spec asserts (Implication 4) that even if `_classify_from_result_file()` were to read the preliminary file, the mtime freshness check would pass because `started_at` predates the write. This relies on `started_at` being captured at subprocess launch, not at executor startup. Verify the capture site (described as line ~581) to confirm.

**OQ-005**: **Option A compliance rate measurement** — NFR-007 specifies that telemetry SHOULD distinguish `agent-written` vs `executor-preliminary` result file sources per phase. The spec does not define where this log is persisted (DEBUG log only, or also written to the sprint execution log/TUI). Clarification needed on whether DEBUG-only is sufficient for downstream analytics.

**OQ-006**: **`_determine_phase_status()` behavior for `exit_code < 0`** — NFR-001 requires that negative exit codes fall through to `ERROR` or `INCOMPLETE` without raising. This must be verified empirically; if the current implementation raises on negative codes, a separate fix is required (noted as in-scope for NFR-001 verification, but no fix is explicitly specified).

**OQ-007**: **`debug_log` availability at injection site** — Change 2 references `debug_log(...)` for the telemetry log call. Confirm that `debug_log` is in scope at the injection site in `execute_sprint()` and that it maps to the module logger at DEBUG level (not a custom function with different behavior).

**OQ-008**: **`_setup_tui_monitor_mocks` helper** — Tests T-003, T-004, T-006 reference `_setup_tui_monitor_mocks(mock_tui, mock_monitor)` as an existing test helper. Verify this helper exists in the test files before adding the new tests; if absent, it must be defined or the mock setup inlined.
