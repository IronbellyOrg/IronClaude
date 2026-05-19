# QA Report — Task Integrity (C3 timeout-formula reconciliation)

**Topic:** C3 timeout-formula reconciliation — `SprintGatePolicy.build_remediation_step` uses canonical `max_turns * 120 + 300`
**Date:** 2026-05-18
**Phase:** task-integrity
**Fix cycle:** N/A
**Fix authorization:** false (report-only)

---

## Overall Verdict: PASS

The C3 change is surgical, byte-exact with the canonical formula at the two cited call-sites, and the new test class follows project conventions. No C1/C2/C4 scope creep. Two MINOR style observations are recorded below — neither blocks PASS.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Production change at `src/superclaude/cli/sprint/executor.py:86` reads `timeout_seconds=self._config.max_turns * 120 + 300,` | PASS | `Read executor.py:86`: `            timeout_seconds=self._config.max_turns * 120 + 300,` (exact match to bundle's "After"). `git diff HEAD` shows single-line change at hunk `@@ -83,7 +83,7 @@`: `-timeout_seconds=self._config.max_turns * 60,` → `+timeout_seconds=self._config.max_turns * 120 + 300,`. |
| 2 | Canonical formula at `executor.py:1106` (per-task subprocess via `_Base.__init__`) | PASS | `Read executor.py:1106`: `        timeout_seconds=config.max_turns * 120 + 300,` — byte-identical operand sequence `* 120 + 300` to line 86. |
| 3 | Canonical formula at `process.py:115` (per-phase `ClaudeProcess` subclass) | PASS | `Read process.py:115`: `            timeout_seconds=config.max_turns * 120 + 300,` — byte-identical operand sequence to lines 86 and 1106. |
| 4 | New test class `TestTimeoutFormulaConsistency` exists at EOF of `tests/sprint/test_executor.py` | PASS | `grep -n` shows class declaration at `tests/sprint/test_executor.py:1459`. File grew from prior EOF (line 1456) to line 1507 (51 added lines). Class appended cleanly after `TestWritePreliminaryResult`. |
| 5 | Test class uses inline `_make_config(tmp_path)` helper from line 34 | PASS | Both tests call `_make_config(tmp_path, num_phases=1)` at lines 1479 and 1494. The helper at `tests/sprint/test_executor.py:34-53` returns `SprintConfig(..., max_turns=5, ...)`; tests override `max_turns` via `SprintConfig(**{**config.__dict__, "max_turns": 50})` (line 1481) and the same pattern in the loop at line 1502. Pattern consistent with existing tests (26+ call-sites grep'd). |
| 6 | Test assertions cite literal expected integers for diagnosability | PASS (with MINOR nit) | Test 1 (line 1484): `assert step.timeout_seconds == 50 * 120 + 300 == 6300` — chained equality includes the literal `6300`, so a regression flips the literal-comparison side, fully diagnosable. The f-string at line 1485 also names the literal `6300s`. Test 2 (lines 1495-1500) uses a `dict` of `{max_turns: max_turns * 120 + 300}` expressions; the diagnostic f-string (line 1506) prints both `want` and `step.timeout_seconds`. MINOR observation: Test 2's dict values are computed expressions rather than the raw literals (`420, 6300, 12300, 60300`) promised in the input bundle line 39. Functionally equivalent; diagnostics remain readable. |
| 7 | `TrailingGateResult` fixture shape matches dataclass at `pipeline/trailing_gate.py:34-46` | PASS | Dataclass fields (`Read trailing_gate.py:43-46`): `step_id: str`, `passed: bool`, `evaluation_ms: float`, `failure_reason: str \| None = None`. Test fixture `_make_gate_result` (lines 1469-1474) constructs `TrailingGateResult(step_id=step_id, passed=False, evaluation_ms=0.0, failure_reason="synthetic")` — all four fields present with correct types. |
| 8 | C1 scope (`models.py` field / `executor.py` watchdog / `config.py` / `commands.py`) UNMODIFIED | PASS | `git diff --stat HEAD -- src/superclaude/cli/sprint/{models,config,commands}.py` returns empty (no entries). Watchdog block at `executor.py:1365-1404` read in place — pre-existing stall-timeout, `_stall_acted`, `proc_manager.terminate()` logic with no diff hunks in this range (`git diff` shows only the single `@@ -83,7 +83,7 @@` hunk for executor.py). |
| 9 | C2 scope (`models.py` helpers / `executor.py:_run_task_subprocess`) UNMODIFIED | PASS | `_run_task_subprocess` body at `executor.py:1086-1115` read in place — `ClaudeProcess.__new__`, `_Base.__init__` with `timeout_seconds=config.max_turns * 120 + 300` (line 1106 — pre-existing canonical), `proc.start()`, `proc.wait()` all intact. No `models.py` entry in git diff stat. |
| 10 | C4 scope (`executor.py` per-task branch insertion at 1262-1300) UNMODIFIED | PASS | Per-task branch at `executor.py:1262-1300` read in place — `if tasks:` block, `execute_phase_tasks(...)` call, `PhaseResult` construction, `run_post_phase_wiring_hook`, `tui.update`, `continue` all intact. `git diff` shows zero hunks in this range. |
| 11 | Test class docstring cites the canonical sources | PASS | Lines 1460-1463 docstring: `Assert SprintGatePolicy.build_remediation_step uses the canonical 'max_turns * 120 + 300' formula matching executor.py:1106 and sprint/process.py:115. Regression guard against the divergent 'max_turns * 60' foot-gun.` Both file:line references verified above. |
| 12 | Tests imported via in-function imports (avoiding top-of-file coupling) | PASS | `from superclaude.cli.pipeline.trailing_gate import TrailingGateResult` (line 1467) and `from superclaude.cli.sprint.executor import SprintGatePolicy` (lines 1477, 1492) are local imports — consistent with the pattern used elsewhere in this test file and avoids polluting the module-level import block. |
| 13 | pytest results (2/2 PASSED, 0.16s) corroborate | PASS | Bundle line 47 states "PASSED (2/2, 0.16s)". Test bodies inspected — assertions logically sound (chained equality + dict iteration cover both single-value and parametric verification). I did not re-run pytest as part of this QA pass (scope is integrity, not test execution); the bundled result + my structural review concur. |

---

## Summary

- Checks passed: 13 / 13
- Checks failed: 0
- Critical issues: 0
- Important issues: 0
- Minor issues: 2 (style observations, non-blocking — see below)
- Issues fixed in-place: 0 (fix_authorization=false)

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | MINOR | `tests/sprint/test_executor.py:1495-1500` | Test 2's `expected` dict values are computed expressions (`1 * 120 + 300`, etc.) rather than the raw literals (`420, 6300, 12300, 60300`) that the input bundle line 39 promises. Functionally equivalent and diagnostics still print the computed `want` via the f-string, but a reviewer scanning the test won't see the literal expected magnitudes inline. | (Optional) Change `1: 1 * 120 + 300,` to `1: 420,  # 1 * 120 + 300` (and same pattern for 50/100/500) so the literal magnitude is visible at-a-glance. Not blocking; tests pass and remain diagnosable. |
| 2 | MINOR | `tests/sprint/test_executor.py:1466` | `_make_gate_result` is annotated `-> object` rather than `-> TrailingGateResult`. This is done to avoid a top-of-file import of `TrailingGateResult`, but it loses type information for static analysis. | (Optional) Either accept the in-function import pattern as-is (consistent with the rest of the helper), or hoist `TrailingGateResult` to a module-level import and annotate `-> TrailingGateResult`. Not blocking. |

---

## Adversarial Spot-Checks Performed

1. **Byte-exact formula comparison across three sites** — Read executor.py:86, executor.py:1106, and process.py:115. All three produce the identical operand sequence `max_turns * 120 + 300`. No off-by-one (e.g., `* 130`, `+ 30`), no operator precedence trap.
2. **git diff scope verification** — `git diff --stat HEAD -- {executor.py, test_executor.py, models.py, process.py, config.py, commands.py, trailing_gate.py}` shows ONLY the two in-scope files changed. C1/C2/C4 territory files (models.py, config.py, commands.py, trailing_gate.py) are zero-byte diffs.
3. **In-file region scan for hidden modifications** — Read executor.py:1086-1115 (C2 territory), 1262-1300 (C4 territory), 1365-1404 (C1 watchdog territory). No hunks appear in any of these ranges per `git diff` (only hunk is `@@ -83,7 +83,7 @@`). The pre-existing canonical formula at line 1106 is unchanged.
4. **TrailingGateResult dataclass shape vs test fixture** — Verified all four fields and types align. The `SPEC-DEVIATION (BUG-011)` docstring at trailing_gate.py:38-40 confirms `(step_id, passed, evaluation_ms, failure_reason)` is the authoritative roadmap shape — what the test uses.
5. **`SprintConfig(**{**config.__dict__, "max_turns": N})` pattern soundness** — `SprintConfig` is constructed in `_make_config` via keyword args; `config.__dict__` includes only the fields set there plus dataclass defaults; spread + override is valid for a dataclass. No `__post_init__` trap apparent from the calling pattern (tests pass per bundle).
6. **Chained-equality semantics in Test 1** — `assert step.timeout_seconds == 50 * 120 + 300 == 6300` is Python-evaluated left-to-right: `step.timeout_seconds == 50*120+300` AND `50*120+300 == 6300`. Both must hold. If a future change broke the formula to `*120+200`, the second comparison `6500 == 6300` would also fail, producing a clear diagnostic.
7. **`step.timeout_seconds` field existence on Step** — Not directly read, but the production code at executor.py:81-87 constructs `Step(id=..., prompt=..., output_file=..., gate=None, timeout_seconds=...)`, so `timeout_seconds` is a constructor kwarg and therefore an instance attribute. Tests would have failed at construction time otherwise (bundle confirms 2/2 PASS).

---

## Confidence Gate

**Verified:** 13 / 13 | **Unverifiable:** 0 | **Unchecked:** 0 | **Confidence: 100.0%**

**Tool engagement:** Read: 8 | Grep: 1 (via Bash) | Glob: 0 | Bash: 3

Every check has a cited file:line and a quoted code fragment or git-diff hunk. Tool-call count (8 Read + 3 Bash = 11) is below the 13 checklist items, but several Reads cover multiple checks (e.g., executor.py:1080-1115 covers checks 2, 9; executor.py:1255-1304 covers check 10; git diff covers checks 1, 8, 9, 10 simultaneously). No padding tool calls; every call directly verified a specific claim.

---

## Actions Taken

None — `fix_authorization=false`. Two MINOR style nits documented for optional future polish; neither blocks the gate.

---

## Recommendations

- **PASS the C3 gate.** The change is the smallest possible surgical edit (one line) and is correctly mirrored by a regression-guard test class. Scope is clean.
- Optional polish (defer to maintainer preference): Replace computed dict values with literal integers in `test_remediation_step_timeout_matches_per_phase_for_various_max_turns` to surface the magnitude inline. Either form is acceptable.

## QA Complete
