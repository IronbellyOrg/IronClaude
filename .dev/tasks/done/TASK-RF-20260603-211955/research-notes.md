# Research Notes: Broaden per-task error_max_turns recovery (Phase 7 / T07.05 detection gap)

**Date:** 2026-06-03
**Scenario:** A (explicit — diagnosis + design fully specified)
**Depth Tier:** Quick (single function + targeted tests, <5 files, no discovery)
**Track Count:** 1

Scope discovery + grounding completed inline by the orchestrator (the troubleshoot
diagnosis this task derives from). All line numbers verified live against
`src/superclaude/cli/sprint/executor.py` and `tests/sprint/test_executor.py` on
branch state = `master` + 1 (HEAD 99bdf77d; PR #121 machinery present).

---

## EXISTING_FILES

- `src/superclaude/cli/sprint/executor.py`
  - `_TASK_SUCCESS_ENVELOPE_PATTERN` — module-level regex, **L1820-1822**. Matches only
    `"subtype":"success"` or `"type"/"subtype":"task_complete"`. Leave intact.
  - `_task_completed_before_overrun(output_path) -> bool` — **L1825-1867**. Reads the
    task NDJSON, builds `lines = [non-empty stripped]`, then `for line in lines[:-1]`
    (**L1863-1864**) searches `_TASK_SUCCESS_ENVELOPE_PATTERN`. Missing/empty guards at
    L1849-1859. This is the helper to extend.
  - per-task classifier — **L1017-1032**: `exit 0→PASS`, `124→INCOMPLETE`,
    `error_max_turns AND _task_completed_before_overrun → PASS_RECOVERED` (**L1021-1028**),
    `_is_transient_failure → FAIL_RECOVERABLE` (L1029-1030), `else → FAIL_TERMINAL`. No
    change needed here — it already maps the helper's True to PASS_RECOVERED.
- `src/superclaude/cli/sprint/models.py` — `TaskStatus.PASS_RECOVERED` (L49), `.is_success`
  = {PASS, PASS_RECOVERED} (L57). No change.
- `tests/sprint/test_executor.py` — holds the Phase 6 per-task recovery tests (see
  PATTERNS). Add new tests here.

## PATTERNS_AND_CONVENTIONS

- Existing Phase 6 tests are the exact template (verified, read in full):
  - `test_per_task_error_max_turns_after_completion_recovers` (**L733-768**): writes a
    per-task NDJSON to `config.task_output_file(phase, tasks[0])` with a `subtype:success`
    line BEFORE the terminal `error_max_turns` line; `_subprocess_factory` returns
    `(1, 101, size)`; asserts `results[0].status == TaskStatus.PASS_RECOVERED` and
    `.is_success is True`; then phase aggregation `all(r.status.is_success ...)`.
  - `test_per_task_error_max_turns_without_completion_still_fails` (**L816-853**): NDJSON
    with NO success envelope, only working lines + terminal `error_max_turns`; asserts
    `FAIL_TERMINAL` + phase fails. This is the guardrail.
  - `test_per_task_genuine_failure_still_fails` (L770-792), `test_per_task_timeout_phase_still_fails`
    (L794-814): non-regression guards for exit 1 (no evidence) and exit 124.
- Fixture idiom: `config = _make_config(tmp_path, num_phases=1)`; `out =
  config.task_output_file(phase, tasks[0]); out.parent.mkdir(parents=True, exist_ok=True);
  out.write_text(...)`; define a `_subprocess_factory(task, config, phase)` returning the
  `(exit_code, turns, output_bytes)` triple; call `execute_phase_tasks(...)`.
- Assertions are STRONG: `== TaskStatus.PASS_RECOVERED`, `.is_success is True/False`,
  phase-level `PhaseStatus`. Never `!= FAIL`.

## GAPS_AND_QUESTIONS

- Final regex token set + tail window N: design specifies a conservative strong-verdict
  regex and N=15; the builder must encode exactly this and the tests must include an
  anti-false-positive test proving tail-scoping (verdict EARLY, outside the window → still
  False). No open external gaps.

## RECOMMENDED_OUTPUTS

- Modify `executor.py`: add `_TASK_TAIL_COMPLETION_PATTERN` + a second OR-branch in
  `_task_completed_before_overrun` scanning the last N pre-terminal lines.
- Add 3 tests to `tests/sprint/test_executor.py` mirroring the Phase 6 tests:
  positive (tail verdict, no envelope → PASS_RECOVERED), guardrail unchanged (already
  exists — assert still passes), anti-false-positive (early-only verdict → FAIL_TERMINAL).
- Optionally a direct unit test of `_task_completed_before_overrun` on a tmp file.

## SUGGESTED_PHASES (for the builder — Template 01)

1. Branch from master + implement `_TASK_TAIL_COMPLETION_PATTERN` + helper second branch.
2. Add the 3 mirrored tests.
3. Regression proof: `git stash` baseline `uv run pytest tests/sprint/ -q` vs post-change;
   prove 0 NEW failures + new tests pass.
4. `make lint` exit 0; `make verify-sync` no NEW drift (do not touch `.claude/`).
5. Commit on `fix/` branch; ship PR to master.

## TEMPLATE_NOTES

- Template 01 (generic) — known inputs/outputs, single-function change + tests, ~1-2h.
- QA_GATE: FINAL_ONLY. TESTING: UNIT. VALIDATION: lint + verify-sync + regression-diff.

## AMBIGUITIES_FOR_USER

None — intent, design, files, line numbers, and test patterns are all pinned. The only
deliberately-deferred decision (exact regex tokens / window N) is specified in the design
and will be adversarially sanity-checked by the false-positive test.
