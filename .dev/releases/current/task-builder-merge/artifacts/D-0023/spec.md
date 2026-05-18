# D-0023 — T02.09 Spec: Commit TEST-004..006 fixtures

**Task:** T02.09 (Phase 2)
**Roadmap items:** R-043, R-044, R-045
**Date:** 2026-05-17

## Goal

Land three pytest fixtures + the corresponding test files asserting the
M2 `## Execution Context` block contract:

- **TEST-004 (R-043).** Fully-populated BUILD_REQUEST → header contains all
  three DM-001 labeled bullets (`**References:**`, `**Source areas:**`,
  `**Key constraints:**`) in declared order, between frontmatter and the
  first `### T<PP>.<TT>` phase task.
- **TEST-005 (R-044).** Minimal BUILD_REQUEST → header degrades to
  References-only: `**References:**` bullet present, `Source areas:` and
  `Key constraints:` substrings absent (R-038 — physical removal, not
  blanking or stub-bulleting).
- **TEST-006 (R-045).** NFR-CONV.3 hidden-input determinism — header range
  satisfies `grep -cE "src/|/.*:[0-9]+"` returning 0. A deliberately leaky
  fixture is included as a negative-path oracle so the detector is proved
  to be wired (the test cannot vacuously pass).

## Paths

- Fixtures:
  - `tests/audit/fixtures/execution_context/fully_populated.md`
  - `tests/audit/fixtures/execution_context/minimal_buildrequest.md`
  - `tests/audit/fixtures/execution_context/hidden_input_leak.md`
- Tests:
  - `tests/audit/test_execution_context_full.py`
  - `tests/audit/test_execution_context_minimal_buildrequest.py`
  - `tests/audit/test_execution_context_no_file_paths.py`

## Dependencies

- T02.07 (D-0021) PASS — COMP-001-M2 SKILL.md template + guidance edits.
- T02.08 (D-0022) — rf-task-builder header emission (samples in D-0017 and
  D-0020 already demonstrate the emission rule; T02.09 fixtures are
  frozen copies of that same shape, not generated live).

## Verification command

```
uv run pytest \
  tests/audit/test_execution_context_full.py \
  tests/audit/test_execution_context_minimal_buildrequest.py \
  tests/audit/test_execution_context_no_file_paths.py -v
```

Expected: exit 0 with 16 PASSED (5 / 6 / 5 across the three files).
