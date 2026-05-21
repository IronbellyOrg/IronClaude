# D-0102 — T05.25 TEST-013 coverage-gate integration tests

**Task:** T05.25 (Phase 5, Roadmap R-101)
**Status:** PARTIAL — 4 of 6 PASS; 2 transitively blocked on the
`_new_run_id` runner defect at `commands.py:1418`.
**Generated:** 2026-05-20 (populated retroactively at the M5 exit
checkpoint T05.28 to close the doc-triplet gap).

## 1. Scope

`tests/cli/eval/test_coverage_gate_integration.py` exercises the FR-G5
coverage gate (T04.14) end-to-end through two surfaces:

1. **Doctor surface** (`uv run superclaude eval doctor
   --check-coverage`) — covered by 4 cases, all PASS today.
2. **Run surface** (`uv run superclaude eval run`, top-of-run gate) —
   covered by 2 cases, both FAIL today on the inherited `_new_run_id`
   NameError before the gate code is reached.

## 2. Test matrix

| # | Case | Surface | Today |
|---|---|---|---|
| 1 | `test_doctor_check_coverage_passes_when_suite_covers_all_matchers` | doctor (happy path) | PASS |
| 2 | `test_doctor_check_coverage_fails_when_fourth_matcher_uncovered` | doctor (4-matcher fixture, one uncovered) | PASS |
| 3 | `test_doctor_check_coverage_stderr_names_uncovered_pattern` | doctor stderr contract | PASS |
| 4 | `test_doctor_check_coverage_json_payload_lists_uncovered_pattern` | doctor `--json` payload contract | PASS |
| 5 | `test_run_exits_2_when_settings_has_uncovered_matcher` | `eval run` top-of-run gate, exit 2 contract | FAIL (NameError) |
| 6 | `test_run_writes_coverage_missing_artifact_under_output_dir` | `eval run` artifact-write contract (`coverage_missing:<pattern>`) | FAIL (NameError) |

## 3. Fixtures

`tests/cli/eval/fixtures/coverage_gate/` (4-matcher fixture set: three
covered + one uncovered).

## 4. Acceptance criteria mapping

- "complete coverage passes" — cases 1, 3, 4. **PASS today**.
- "missing matcher fails with exit 2" — case 5 for `eval run`; case 2
  for `eval doctor`. Case 2 PASS; case 5 transitively blocked.
- "doctor stderr names the uncovered pattern" — case 3. **PASS today**.
- "`coverage_missing:<pattern>` artifact file is produced" — case 6.
  Transitively blocked (no per-run output directory created because
  the runner aborts).

## 5. Blocker

Both run-path cases fail with:

```
NameError: name '_new_run_id' is not defined
  at src/superclaude/cli/eval/commands.py:1418
```

The replacement symbol (`artifact_layout.compose_run_id`) is shipped
and tested under T04.13 (`tests/cli/eval/test_artifact_layout.py`, 19
PASS); the wiring at `commands.py:1418` has not landed (owned by
`.dev/tasks/to-do/TASK-RF-20260518-cliEval-P4-wire-and-ship/`).

When the wiring lands, cases 5 and 6 should pass with no edits to the
test module — both call the public CLI surface and assert against the
documented exit-code-2 + artifact-write contract.

## 6. Verification commands

```
uv run pytest tests/cli/eval/test_coverage_gate_integration.py -v
```

Live capture (this checkpoint): `evidence/T05.25/pytest-test-013.log`.
