# D-0102 — T05.25 TEST-013 coverage-gate integration tests

**Task:** T05.25 (Phase 5, Roadmap R-101)
**Status:** MET — 6 of 6 PASS.
**Last refreshed:** 2026-05-21 (re-verification after upstream
`_new_run_id` wiring blocker cleared).

## 1. Scope

`tests/cli/eval/test_coverage_gate_integration.py` exercises the FR-G5
coverage gate (T04.14) end-to-end through two surfaces:

1. **Doctor surface** (`uv run superclaude eval doctor
   --check-coverage`) — covered by 4 cases.
2. **Run surface** (`uv run superclaude eval run`, top-of-run gate) —
   covered by 2 cases.

## 2. Test matrix

| # | Case | Surface | Result |
|---|---|---|---|
| 1 | `test_doctor_check_coverage_passes_when_suite_covers_all_matchers` | doctor (happy path, 3-matcher fixture) | PASS |
| 2 | `test_doctor_check_coverage_fails_when_fourth_matcher_uncovered` | doctor (4-matcher fixture, one uncovered) | PASS |
| 3 | `test_doctor_check_coverage_stderr_names_uncovered_pattern` | doctor stderr roster contract | PASS |
| 4 | `test_doctor_check_coverage_json_payload_lists_uncovered_pattern` | doctor `--json` payload contract | PASS |
| 5 | `test_run_exits_2_when_settings_has_uncovered_matcher` | `eval run` top-of-run gate, exit 2 contract | PASS |
| 6 | `test_run_writes_coverage_missing_artifact_under_output_dir` | `eval run` artifact-write contract (`coverage_missing:<pattern>`) | PASS |

## 3. Fixtures

`tests/cli/eval/fixtures/coverage_gate/`:

- `suite.yaml` — three evals declaring one `expect_tool_call` per v1
  MCP matcher prefix (`mcp__auggie__`, `mcp__auggie-mcp__`,
  `mcp__airis-mcp-gateway__`).
- `settings_complete.json` — three matchers, fully covered.
- `settings_missing.json` — four matchers: three covered plus the
  uncovered `mcp__auggie__novel_tool_v2` used as the breach probe.

## 4. Acceptance criteria mapping

- "complete coverage passes" — case 1 (and cases 3/4 cross-check the
  failure-side roster). **MET**.
- "missing matcher fails with exit 2" — case 2 (doctor) and case 5
  (`eval run` top-of-run gate). **MET**.
- "doctor stderr names the uncovered pattern" — case 3 asserts the
  exact `PreToolUse: mcp__auggie__novel_tool_v2` line on stderr and
  that no covered matcher leaks into the failure roster. **MET**.
- "`coverage_missing:<pattern>` artifact file is produced" — case 6
  asserts the sanitised filename, JSON payload (`coverage_missing:
  true`, `pattern`, `event`), and that only the missing pattern
  produces a file. **MET**.

## 5. Verification commands

```
uv run pytest tests/cli/eval/test_coverage_gate_integration.py -v
```

Live capture: `evidence/T05.25/pytest-test-013.log` (6 passed, 0
failed).
