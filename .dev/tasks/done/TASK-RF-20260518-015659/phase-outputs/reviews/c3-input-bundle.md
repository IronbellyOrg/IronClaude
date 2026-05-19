# C3 QA Input Bundle

## Modified production file

**Path:** `src/superclaude/cli/sprint/executor.py` (line 86 region — inside `SprintGatePolicy.build_remediation_step`)

**Before:**
```python
            id=f"{gate_result.step_id}_remediation",
            prompt=prompt,
            output_file=output_dir / f"{gate_result.step_id}_remediation.md",
            gate=None,
            timeout_seconds=self._config.max_turns * 60,
        )
```

**After:**
```python
            id=f"{gate_result.step_id}_remediation",
            prompt=prompt,
            output_file=output_dir / f"{gate_result.step_id}_remediation.md",
            gate=None,
            timeout_seconds=self._config.max_turns * 120 + 300,
        )
```

The change reconciles `max_turns * 60` (divergent) with the canonical `max_turns * 120 + 300` used at:
- `src/superclaude/cli/sprint/executor.py:1106` (per-task subprocess via `_Base.__init__`)
- `src/superclaude/cli/sprint/process.py:115` (per-phase sprint `ClaudeProcess` subclass)

## New test class

**Path:** `tests/sprint/test_executor.py` (appended at EOF)

**Class:** `TestTimeoutFormulaConsistency`

**Functions:**
1. `test_remediation_step_timeout_matches_canonical_formula` — constructs `SprintConfig(max_turns=50)` (via `SprintConfig(**{**_make_config(tmp_path).__dict__, "max_turns": 50})`), invokes `SprintGatePolicy(config).build_remediation_step(TrailingGateResult(step_id="step-x", passed=False, evaluation_ms=0.0, failure_reason="synthetic"))`, asserts `step.timeout_seconds == 50 * 120 + 300 == 6300`.
2. `test_remediation_step_timeout_matches_per_phase_for_various_max_turns` — iterates `max_turns ∈ {1, 50, 100, 500}`, asserts `step.timeout_seconds == max_turns * 120 + 300` in each case (literals: 420, 6300, 12300, 60300).

Helper `_make_gate_result(self, step_id="step-x")` constructs `TrailingGateResult` per `src/superclaude/cli/pipeline/trailing_gate.py:34-46`.

Reuses the existing `_make_config(tmp_path, num_phases=1)` helper from `tests/sprint/test_executor.py:35`.

## pytest results summary

**Result:** PASSED (2/2, 0.16s)

Raw output: `.dev/tasks/to-do/TASK-RF-20260518-015659/phase-outputs/test-results/phase-3-c3-pytest-output.txt`
Summary: `.dev/tasks/to-do/TASK-RF-20260518-015659/phase-outputs/test-results/phase-3-c3-summary.md`

## QA scope

This gate verifies ONLY the C3 timeout-formula reconciliation change in `src/superclaude/cli/sprint/executor.py` around line 86 and the new `TestTimeoutFormulaConsistency` class in `tests/sprint/test_executor.py`. No changes to C1 (`models.py` field / `executor.py` watchdog / `config.py` loader / `commands.py` Click), C2 (`models.py` helpers / `executor.py` `_run_task_subprocess`), or C4 (`executor.py` per-task branch insertion) are in scope. The watchdog block at `executor.py:1365-1404`, the `_run_task_subprocess` body at `executor.py:1086-1115`, and the per-task branch at `executor.py:1262-1300` were NOT modified by Phase 3.
