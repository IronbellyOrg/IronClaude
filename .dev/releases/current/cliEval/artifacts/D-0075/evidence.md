# D-0075 — implementation evidence

**Task:** T04.14 (Phase 4, FR-G5 / R-075)
**Completed:** 2026-05-20

## Files added

* `src/superclaude/cli/eval/coverage.py` — pure module: `coverage_gate`,
  `CoverageResult`, `CoverageMatcher`, `eval_covers_pattern`,
  `extract_hook_matchers`, `default_matcher_filter`,
  `sanitize_pattern_for_filename`,
  `COVERAGE_GATE_FAILED_EXIT_CODE`, `COVERAGE_MISSING_ARTIFACT_PREFIX`.
* `tests/cli/eval/test_coverage_gate.py` — 26 tests covering helpers,
  end-to-end gate behaviours, and CLI integration on doctor.

## Files modified

* `src/superclaude/cli/eval/commands.py`
  * Imports `coverage_gate`, `CoverageResult`,
    `COVERAGE_GATE_FAILED_EXIT_CODE` from `.coverage`.
  * `doctor_payload(...)` now accepts `coverage_result: Optional[CoverageResult]`
    and emits one of `{status: "skipped" | "passed" | "failed"}`. When
    requested, the marker carries `result` = `CoverageResult.to_dict()`.
  * `doctor(...)` gains `--suite <name>` (optional) and invokes
    `coverage_gate(settings_path=~/.claude/settings.json, suite=specs)`
    when `--check-coverage` is on. Failure → stderr roster + exit 2.
  * `eval_run(...)` calls the gate AFTER suite parse + filter, BEFORE
    worker dispatch. Failure → roster + exit 2; artifacts land inside
    `resolved_output`.
  * New helpers: `_format_coverage_summary`, `_format_coverage_missing_roster`.
* `tests/cli/eval/test_doctor.py`
  * Coverage-gate-marker assertions updated: the deferred M2 marker
    (`status: "deferred"`, `milestone: "M4"`, `task: "T04.14"`) was
    retired when this task landed. New shape:
    `{status: "skipped" | "passed" | "failed"}` with `result` when
    requested.

## Tests

70 / 70 passing across `test_doctor.py` and `test_coverage_gate.py`:

```
tests/cli/eval/test_coverage_gate.py: 26 passed
tests/cli/eval/test_doctor.py:        44 passed
```

Full pytest log: `.dev/releases/current/cliEval/evidence/T04.14/pytest.log`.

Two unrelated failures remain in the wider `tests/cli/eval/` suite —
both pre-date this task:

* `test_ban_import_rule.py::test_clean_tree_passes_ruff_check` — fails
  because the existing `eval_run` body references helpers
  (`_run_one_spec`, `_new_run_id`, `RUN_CLEAN_EXIT_CODE`, …) that have
  not yet been defined in `commands.py`. These F821 errors exist on the
  branch before this commit; T04.14 does not regress that count
  (35 errors → 23 errors after this task because new imports are now
  used).
* `test_eval_group.py::test_run_skeleton_emits_deferral_notice_on_stderr` —
  uses `CliRunner(mix_stderr=False)`, an API removed in modern Click.
  This is also pre-existing on the branch.

## Acceptance criteria — verification

| AC | Method | Result |
|---|---|---|
| `coverage_gate(settings_path, suite)` exists with the documented signature | `coverage.py:261-348` | ✅ |
| v1 covers `mcp__auggie__*`, `mcp__auggie-mcp__*`, `mcp__airis-mcp-gateway__*` | `_DEFAULT_MCP_TOOL_PREFIXES` + `default_matcher_filter` | ✅ |
| Missing coverage emits `coverage_missing:<pattern>` artifact + exits 2 | `test_coverage_gate_fails_and_writes_artifact_for_uncovered_pattern`, `test_cli_doctor_check_coverage_fails_when_uncovered_matcher_present` | ✅ |
| 4th matcher stub → gate fails | `test_coverage_gate_fails_when_fourth_matcher_added_without_eval` | ✅ |
| `D-0075/spec.md` documents matcher → eval mapping | this directory | ✅ |
| `eval doctor --check-coverage` wires the gate | `commands.py` doctor body | ✅ |
| `eval run` wires the gate at top-of-run | `commands.py` eval_run body (post-filter, pre-orchestrator) | ✅ |

## Confidence

Confidence: 90%. The gate is deterministic, the CLI wiring is covered
by unit tests, and the doctor regression net is green. The remaining
10% reflects the deferred M5 validation against a real
`~/.claude/settings.json` + the real suite manifest, which T05.25
owns.
