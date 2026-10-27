# D-0023 — T02.09 Evidence: Commit TEST-004..006 fixtures

**Task:** T02.09 (Phase 2)
**Roadmap items:** R-043, R-044, R-045
**Date:** 2026-05-17
**Status:** PASS

---

## 1. Scope

T02.09 lands three pytest test files plus their fixtures under
`tests/audit/fixtures/execution_context/`, asserting the M2 `##
Execution Context` block contract:

| TEST   | Roadmap | Assertion |
|--------|---------|-----------|
| TEST-004 | R-043 | Fully-populated → 3 labeled bullets present in declared order |
| TEST-005 | R-044 | Minimal BUILD_REQUEST → References-only degradation, Source areas / Key constraints physically absent |
| TEST-006 | R-045 | NFR-CONV.3 hidden-input guard — `grep -cE "src/\|/.*:[0-9]+"` returns 0 across clean fixtures; ≥1 against leak fixture (detector wiring oracle) |

## 2. Files Created

| Path | Purpose |
|---|---|
| `tests/audit/fixtures/execution_context/__init__.py` | Package marker |
| `tests/audit/fixtures/execution_context/fully_populated.md` | TEST-004 fixture (fully-populated form) |
| `tests/audit/fixtures/execution_context/minimal_buildrequest.md` | TEST-005 fixture (degraded form) |
| `tests/audit/fixtures/execution_context/hidden_input_leak.md` | TEST-006 negative-path fixture |
| `tests/audit/test_execution_context_full.py` | TEST-004 (5 cases) |
| `tests/audit/test_execution_context_minimal_buildrequest.py` | TEST-005 (6 cases) |
| `tests/audit/test_execution_context_no_file_paths.py` | TEST-006 (5 cases) |

## 3. Test Run

```
$ uv run pytest \
    tests/audit/test_execution_context_full.py \
    tests/audit/test_execution_context_minimal_buildrequest.py \
    tests/audit/test_execution_context_no_file_paths.py -v
...
collected 16 items

tests/audit/test_execution_context_full.py::TestExecutionContextFull::test_fixture_exists PASSED
tests/audit/test_execution_context_full.py::TestExecutionContextFull::test_block_heading_present PASSED
tests/audit/test_execution_context_full.py::TestExecutionContextFull::test_block_sits_between_frontmatter_and_first_phase PASSED
tests/audit/test_execution_context_full.py::TestExecutionContextFull::test_all_three_labeled_bullets_present PASSED
tests/audit/test_execution_context_full.py::TestExecutionContextFull::test_labeled_bullets_in_declared_order PASSED
tests/audit/test_execution_context_minimal_buildrequest.py::TestExecutionContextMinimal::test_fixture_exists PASSED
tests/audit/test_execution_context_minimal_buildrequest.py::TestExecutionContextMinimal::test_block_heading_present PASSED
tests/audit/test_execution_context_minimal_buildrequest.py::TestExecutionContextMinimal::test_references_bullet_present PASSED
tests/audit/test_execution_context_minimal_buildrequest.py::TestExecutionContextMinimal::test_source_areas_bullet_absent PASSED
tests/audit/test_execution_context_minimal_buildrequest.py::TestExecutionContextMinimal::test_key_constraints_bullet_absent PASSED
tests/audit/test_execution_context_minimal_buildrequest.py::TestExecutionContextMinimal::test_only_one_labeled_bullet_in_block PASSED
tests/audit/test_execution_context_no_file_paths.py::TestHiddenInputGuardCleanFixtures::test_fully_populated_header_has_zero_hidden_input_hits PASSED
tests/audit/test_execution_context_no_file_paths.py::TestHiddenInputGuardCleanFixtures::test_minimal_header_has_zero_hidden_input_hits PASSED
tests/audit/test_execution_context_no_file_paths.py::TestHiddenInputGuardCleanFixtures::test_clean_fixtures_match_real_grep_output PASSED
tests/audit/test_execution_context_no_file_paths.py::TestHiddenInputGuardDetectsLeaks::test_leak_fixture_has_nonzero_hidden_input_hits PASSED
tests/audit/test_execution_context_no_file_paths.py::TestHiddenInputGuardDetectsLeaks::test_leak_fixture_matches_real_grep_output PASSED

============================== 16 passed in 0.04s ==============================
```

Exit code: 0.

## 4. Acceptance-criteria mapping

| AC | Criterion | Status | Evidence |
|---|---|---|---|
| AC1 | `uv run pytest tests/audit/test_execution_context_full.py tests/audit/test_execution_context_minimal_buildrequest.py tests/audit/test_execution_context_no_file_paths.py -v` exits 0 | **PASS** | § 3 — 16 passed, exit 0 |
| AC2 | TEST-005 asserts Source areas and Key constraints lines are **absent** (not blank) | **PASS** | `test_source_areas_bullet_absent`, `test_key_constraints_bullet_absent`, and `test_only_one_labeled_bullet_in_block` (assert exactly one labeled bullet) |
| AC3 | TEST-006 asserts `grep` over header range returns 0 | **PASS** | `test_fully_populated_header_has_zero_hidden_input_hits`, `test_minimal_header_has_zero_hidden_input_hits`, `test_clean_fixtures_match_real_grep_output` (cross-validated with real `grep -cE`) |
| AC4 | Evidence at `TASKLIST_ROOT/artifacts/D-0023/evidence.md` | **PASS** | This file |

## 5. Roadmap-row mapping

- **R-043 (TEST-004).** `test_all_three_labeled_bullets_present` + `test_labeled_bullets_in_declared_order` + `test_block_sits_between_frontmatter_and_first_phase` cover the "3 labeled lines, post-frontmatter, pre-first-phase" assertion.
- **R-044 (TEST-005).** `test_references_bullet_present` + the two absence tests + `test_only_one_labeled_bullet_in_block` cover the R-038 degradation rule (physical removal, not blanking).
- **R-045 (TEST-006).** Two clean-path tests + the real `grep -cE` subprocess oracle + two negative-path tests against the leak fixture cover the NFR-CONV.3 hidden-input guard (R-039).

## 6. Design notes

- **Negative-path oracle (TEST-006 leak fixture).** Without a deliberately-leaky fixture, the grep-returns-0 assertion is satisfied by any empty input — including a header-range extractor that silently returns an empty string. The leak fixture proves both the regex and the extractor are wired: it MUST yield ≥1 hit, otherwise the production verification command would falsely pass.
- **Subprocess cross-validation.** Each clean fixture is checked twice: once with an in-process regex compiled to `re.compile(r"src/|/.*:[0-9]+")`, and once by shelling out to real `grep -cE "src/|/.*:[0-9]+"`. This protects against drift between the in-process implementation and the production verification command quoted in the DM-001 spec and roadmap rows.
- **Line-based heading detection.** Substrings of `## Execution Context` appear in YAML frontmatter description fields of fixture files. All tests use `line.strip() == "## Execution Context"` to bind to the actual heading line, not the descriptive mention.
- **Fixture shape matches the rendered samples** in `D-0017/sample-emitter-output.md` (fully-populated) and `D-0020/sample-minimal-buildrequest.md` (degraded), so the fixtures freeze the live emission contract demonstrated by T02.02 and T02.05.

## 7. Verdict

**PASS** — All 4 acceptance criteria satisfied; 16/16 tests green; fixtures + tests + evidence committed.

Dependencies satisfied: T02.07 (D-0021) PASS. T02.08 (D-0022 — rf-task-builder header emission) is functionally satisfied by the SKILL.md narrative at `:879–940` already consumed by the D-0017 and D-0020 samples; the T02.09 fixtures freeze those same emission shapes for regression coverage.
Unblocks: T02.10 (NFR-CONV.7 evidence-bound preservation re-run); T02.11 (MIG-002 landing migration); T02.12 (Phase 2 end checkpoint).
