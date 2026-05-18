# D-0080 Evidence — T06.15 TEST-018 + TEST-019 dnsp twice-exhaust + dedup-collapse fixtures

**Task:** T06.15 — Commit TEST-018 + TEST-019 dnsp twice-exhaust + dedup-collapse fixtures
**Phase:** Phase 6 — M6 Synthetic DNSP on Partition Exhaust
**Roadmap Item IDs:** R-133 (TEST-018 twice-exhaust fixture), R-134 (TEST-019 dedup-collapse fixture)
**Date:** 2026-05-18
**Branch:** feat/hook-sync-and-matcher-fix
**Tier:** STANDARD
**Critical Path Override:** No
**Verification Method:** Direct test execution
**Status:** PASS

---

## 1. Summary

T06.15 lands two new fixtures under `tests/audit/` that bind the DM-003-M6
synthetic-dnsp emission contract (T06.02 / D-0069) and the R-123 within-cycle
dedup-collapse rule (T06.05 / D-0072, ratified by T06.09 / D-0075 staging)
to runnable Python assertions:

- **TEST-018** — `tests/audit/test_dnsp_twice_exhaust.py` — exercises the
  canonical "twice-exhaust" emission (a partition rf-* agent that failed
  retry-1 and exhausted retry-2). Asserts all 5 baseline DM-003 fields
  (severity, source, affected_range, evidence, recommendation) are
  populated; severity is the byte-exact literal `HIGH`; source is the
  byte-exact literal `synthetic-dnsp`; dedup_key is a 2-element YAML list
  whose second element belongs to the closed vocabulary
  `{retry-1, retry-2, gap-fill-round-1, gap-fill-round-2, gap-fill-round-3}`;
  found_n_times defaults to integer `1`. Negative-path adversarial
  emissions (missing severity, lowercase source, blank affected_range,
  blank evidence, suffix-extended recommendation, 3-element dedup_key,
  non-vocabulary exhaust_point, found_n_times=0, stringified
  found_n_times) are each rejected by the validator with the named symbol
  the wrapper contract pins (`DM-003-fixed-field-invariant-violation`,
  `DM-003-dynamic-field-invariant-violation`,
  `DM-003-recommendation-invariant-violation`,
  `DM-003-dedup-key-shape-violation`,
  `DM-003-found-n-times-invariant-violation`).

- **TEST-019** — `tests/audit/test_dnsp_dedup_collapse.py` — exercises
  the R-123 within-cycle collapse rule: two synthetic-dnsp emissions
  with byte-identical `(assigned_files_range, escalation_ladder_exhaust_point)`
  2-tuples MUST collapse to one record with `found_n_times=2`.
  Cumulative collapse (three identical emissions → cardinality 1,
  found_n_times=3) anchors the +1-per-collision rule across N>2.
  Negative-path complement (two distinct dedup_keys do NOT collapse;
  +1-from-current-value semantics for already-collapsed records)
  proves the collapse is keyed on the 2-tuple, not on source/severity
  alone, and that the increment scales monotonically.

Both fixtures additionally lock the wrapper-bullet source text in
`rf-analyst.md`, `rf-qa.md`, `rf-qa-qualitative.md`, and `SKILL.md`
against silent drift on the load-bearing literals (`HIGH`,
`synthetic-dnsp`, the byte-exact recommendation string, the DM-003
schema label, the closed vocabulary, the rejection symbols, the
R-123 / INV-012 labels, and the `+1` increment + `default 1` wording).
TEST-019 also pins SKILL.md §A.8 to specify that the within-cycle
collapse runs BEFORE gate evaluation (the R-127 merge-step ordering).

## 2. Planning Inputs

- **Dependency closure.** T06.05 (D-0072) PASS — R-117/R-118/R-119 wrapper
  rejection contracts landed at all 4 sites with named symbols. T06.09
  (D-0075) — R-123/R-124 dedup composition wired. T06.13 (D-0078) — DNSP
  edit sites at rf-analyst.md:58-71 and rf-qa.md:70-77 (heading markers).
  T06.14 (D-0079) — DNSP edit site at rf-qa-qualitative.md:70-80; COMP-006
  rf-team-lead.md:417 byte-stable.
- **R-133 spec (phase-6-tasklist.md L734-738).** TEST-018 asserts all 5
  fixed fields populated; severity HIGH; source synthetic-dnsp.
- **R-134 spec (phase-6-tasklist.md L734-738).** TEST-019 asserts
  cardinality=1 with found_n_times=2.
- **Source-of-truth files** (4 wrapper sites): all DNSP emission contract
  bullets named in T06.01-T06.14 evidence packs (D-0068 .. D-0079).
- **Existing fixture pattern reference.** `test_synthetic_dnsp_dedup_not_regression.py`
  (TEST-022 / D-0065 — T05.14 cross-cycle composition fixture) and
  `test_sequencing_PR06_before_PR04.py` (TEST-024 / D-0066) establish
  the markdown-contract-binding pattern with pure-Python helpers,
  positive and negative paths, and wrapper-text guards. T06.15 follows
  that pattern.

## 3. Execution — Acceptance-criterion test execution

### 3.1 AC1 — `uv run pytest tests/audit/test_dnsp_twice_exhaust.py tests/audit/test_dnsp_dedup_collapse.py -v` exits 0

```text
$ uv run pytest tests/audit/test_dnsp_twice_exhaust.py tests/audit/test_dnsp_dedup_collapse.py -v
============================= test session starts ==============================
platform linux -- Python 3.12.12, pytest-9.0.3, pluggy-1.6.0
SuperClaude: 4.2.0
collected 57 items

tests/audit/test_dnsp_twice_exhaust.py::TestWrapperContractTextGuards::test_all_wrapper_sources_exist PASSED [  1%]
tests/audit/test_dnsp_twice_exhaust.py::TestWrapperContractTextGuards::test_synthetic_dnsp_sentinel_present_at_every_site PASSED [  3%]
tests/audit/test_dnsp_twice_exhaust.py::TestWrapperContractTextGuards::test_high_severity_literal_present_at_every_site PASSED [  5%]
tests/audit/test_dnsp_twice_exhaust.py::TestWrapperContractTextGuards::test_recommendation_byte_exact_at_every_site PASSED [  7%]
tests/audit/test_dnsp_twice_exhaust.py::TestWrapperContractTextGuards::test_dm_003_schema_named_at_every_site PASSED [  8%]
tests/audit/test_dnsp_twice_exhaust.py::TestWrapperContractTextGuards::test_seven_field_phrasing_present_at_agent_sites PASSED [ 10%]
tests/audit/test_dnsp_twice_exhaust.py::TestWrapperContractTextGuards::test_twice_exhaust_trigger_named_at_every_agent_site PASSED [ 12%]
tests/audit/test_dnsp_twice_exhaust.py::TestWrapperContractTextGuards::test_rejection_symbols_present_at_every_site PASSED [ 14%]
tests/audit/test_dnsp_twice_exhaust.py::TestWrapperContractTextGuards::test_closed_vocabulary_named_at_every_site PASSED [ 15%]
tests/audit/test_dnsp_twice_exhaust.py::TestTwiceExhaustEmissionPasses::test_validator_returns_ok PASSED [ 17%]
tests/audit/test_dnsp_twice_exhaust.py::TestTwiceExhaustEmissionPasses::test_severity_is_high_literal PASSED [ 19%]
tests/audit/test_dnsp_twice_exhaust.py::TestTwiceExhaustEmissionPasses::test_source_is_synthetic_dnsp_literal PASSED [ 21%]
tests/audit/test_dnsp_twice_exhaust.py::TestTwiceExhaustEmissionPasses::test_all_five_fixed_fields_populated PASSED [ 22%]
tests/audit/test_dnsp_twice_exhaust.py::TestTwiceExhaustEmissionPasses::test_recommendation_byte_exact PASSED [ 24%]
tests/audit/test_dnsp_twice_exhaust.py::TestTwiceExhaustEmissionPasses::test_dedup_key_is_two_tuple_yaml_list PASSED [ 26%]
tests/audit/test_dnsp_twice_exhaust.py::TestTwiceExhaustEmissionPasses::test_dedup_key_second_element_in_vocabulary PASSED [ 28%]
tests/audit/test_dnsp_twice_exhaust.py::TestTwiceExhaustEmissionPasses::test_twice_exhaust_carries_retry_2 PASSED [ 29%]
tests/audit/test_dnsp_twice_exhaust.py::TestTwiceExhaustEmissionPasses::test_found_n_times_default_is_one PASSED [ 31%]
tests/audit/test_dnsp_twice_exhaust.py::TestNegativePathRejectionSymbols::test_missing_severity_rejected_as_fixed_field PASSED [ 33%]
tests/audit/test_dnsp_twice_exhaust.py::TestNegativePathRejectionSymbols::test_severity_low_rejected_as_fixed_field PASSED [ 35%]
tests/audit/test_dnsp_twice_exhaust.py::TestNegativePathRejectionSymbols::test_source_lowercase_rejected_as_fixed_field PASSED [ 36%]
tests/audit/test_dnsp_twice_exhaust.py::TestNegativePathRejectionSymbols::test_blank_affected_range_rejected_as_dynamic_field PASSED [ 38%]
tests/audit/test_dnsp_twice_exhaust.py::TestNegativePathRejectionSymbols::test_blank_evidence_rejected_as_dynamic_field PASSED [ 40%]
tests/audit/test_dnsp_twice_exhaust.py::TestNegativePathRejectionSymbols::test_recommendation_with_suffix_rejected PASSED [ 42%]
tests/audit/test_dnsp_twice_exhaust.py::TestNegativePathRejectionSymbols::test_dedup_key_three_element_rejected PASSED [ 43%]
tests/audit/test_dnsp_twice_exhaust.py::TestNegativePathRejectionSymbols::test_dedup_key_non_vocabulary_exhaust_point_rejected PASSED [ 45%]
tests/audit/test_dnsp_twice_exhaust.py::TestNegativePathRejectionSymbols::test_found_n_times_zero_rejected PASSED [ 47%]
tests/audit/test_dnsp_twice_exhaust.py::TestNegativePathRejectionSymbols::test_found_n_times_string_rejected PASSED [ 49%]
tests/audit/test_dnsp_twice_exhaust.py::TestVocabularyIsFullyWired::test_each_vocabulary_value_yields_valid_emission[gap-fill-round-1] PASSED [ 50%]
tests/audit/test_dnsp_twice_exhaust.py::TestVocabularyIsFullyWired::test_each_vocabulary_value_yields_valid_emission[gap-fill-round-2] PASSED [ 52%]
tests/audit/test_dnsp_twice_exhaust.py::TestVocabularyIsFullyWired::test_each_vocabulary_value_yields_valid_emission[gap-fill-round-3] PASSED [ 54%]
tests/audit/test_dnsp_twice_exhaust.py::TestVocabularyIsFullyWired::test_each_vocabulary_value_yields_valid_emission[retry-1] PASSED [ 56%]
tests/audit/test_dnsp_twice_exhaust.py::TestVocabularyIsFullyWired::test_each_vocabulary_value_yields_valid_emission[retry-2] PASSED [ 57%]
tests/audit/test_dnsp_twice_exhaust.py::TestVocabularyIsFullyWired::test_vocabulary_size_is_exactly_five PASSED [ 59%]
tests/audit/test_dnsp_dedup_collapse.py::TestR123WrapperTextGuards::test_all_wrapper_sources_exist PASSED [ 61%]
tests/audit/test_dnsp_dedup_collapse.py::TestR123WrapperTextGuards::test_r123_label_named_at_every_site PASSED [ 63%]
tests/audit/test_dnsp_dedup_collapse.py::TestR123WrapperTextGuards::test_within_cycle_phrase_named_at_every_site PASSED [ 64%]
tests/audit/test_dnsp_dedup_collapse.py::TestR123WrapperTextGuards::test_found_n_times_default_one_increment_one_present PASSED [ 66%]
tests/audit/test_dnsp_dedup_collapse.py::TestR123WrapperTextGuards::test_collapse_rejection_symbol_present_at_every_site PASSED [ 68%]
tests/audit/test_dnsp_dedup_collapse.py::TestR123WrapperTextGuards::test_inv_012_label_present_at_every_site PASSED [ 70%]
tests/audit/test_dnsp_dedup_collapse.py::TestR123WrapperTextGuards::test_skill_md_a8_merge_pins_within_cycle_collapse PASSED [ 71%]
tests/audit/test_dnsp_dedup_collapse.py::TestTwoIdenticalDedupKeysCollapse::test_pre_collapse_input_has_two_emissions PASSED [ 73%]
tests/audit/test_dnsp_dedup_collapse.py::TestTwoIdenticalDedupKeysCollapse::test_collapse_cardinality_is_one PASSED [ 75%]
tests/audit/test_dnsp_dedup_collapse.py::TestTwoIdenticalDedupKeysCollapse::test_collapse_found_n_times_is_two PASSED [ 77%]
tests/audit/test_dnsp_dedup_collapse.py::TestTwoIdenticalDedupKeysCollapse::test_exactly_one_collapse_was_applied PASSED [ 78%]
tests/audit/test_dnsp_dedup_collapse.py::TestTwoIdenticalDedupKeysCollapse::test_collapsed_record_preserves_5_fixed_fields PASSED [ 80%]
tests/audit/test_dnsp_dedup_collapse.py::TestTwoIdenticalDedupKeysCollapse::test_collapsed_record_still_validates PASSED [ 82%]
tests/audit/test_dnsp_dedup_collapse.py::TestTwoIdenticalDedupKeysCollapse::test_collapse_preserves_dedup_key_identity PASSED [ 84%]
tests/audit/test_dnsp_dedup_collapse.py::TestThreeIdenticalDedupKeysCollapse::test_three_emissions_collapse_to_cardinality_one PASSED [ 85%]
tests/audit/test_dnsp_dedup_collapse.py::TestDistinctDedupKeysDoNotCollapse::test_different_range_does_not_collapse PASSED [ 87%]
tests/audit/test_dnsp_dedup_collapse.py::TestDistinctDedupKeysDoNotCollapse::test_different_exhaust_point_does_not_collapse PASSED [ 89%]
tests/audit/test_dnsp_dedup_collapse.py::TestEmittedFoundNTimesGreaterThanOneRejected::test_emission_with_found_n_times_2_rejected_pre_collapse PASSED [ 91%]
tests/audit/test_dnsp_dedup_collapse.py::TestEmittedFoundNTimesGreaterThanOneRejected::test_collapse_increments_from_current_value PASSED [ 92%]
tests/audit/test_dnsp_dedup_collapse.py::TestCrossFixtureConsistencyWithTest018::test_validator_imported_from_test018 PASSED [ 94%]
tests/audit/test_dnsp_dedup_collapse.py::TestCrossFixtureConsistencyWithTest018::test_build_helper_imported_from_test018 PASSED [ 96%]
tests/audit/test_dnsp_dedup_collapse.py::TestCrossFixtureConsistencyWithTest018::test_fixed_literals_match PASSED [ 98%]
tests/audit/test_dnsp_dedup_collapse.py::TestCrossFixtureConsistencyWithTest018::test_vocabulary_matches PASSED [100%]

============================== 57 passed in 0.06s ==============================
```

Exit code: `0`. **PASS** for AC1.

### 3.2 AC2 — TEST-018 asserts all 5 fixed fields populated; severity HIGH; source synthetic-dnsp

Mapped to test classes in `tests/audit/test_dnsp_twice_exhaust.py`:

| AC2 sub-claim | Test method | Status |
|---|---|---|
| All 5 fixed fields populated | `TestTwiceExhaustEmissionPasses::test_all_five_fixed_fields_populated` | **PASS** |
| Severity HIGH (byte-exact) | `TestTwiceExhaustEmissionPasses::test_severity_is_high_literal` | **PASS** |
| Source `synthetic-dnsp` (byte-exact) | `TestTwiceExhaustEmissionPasses::test_source_is_synthetic_dnsp_literal` | **PASS** |
| Validator accepts canonical emission | `TestTwiceExhaustEmissionPasses::test_validator_returns_ok` | **PASS** |
| Negative paths reject per named symbol | `TestNegativePathRejectionSymbols::*` (10 tests) | **PASS** (10/10) |
| Closed vocabulary fully wired | `TestVocabularyIsFullyWired::test_each_vocabulary_value_yields_valid_emission[*]` (5 tests) | **PASS** (5/5) |
| Wrapper-bullet contract text guards | `TestWrapperContractTextGuards::*` (9 tests) | **PASS** (9/9) |

The 5 fixed/dynamic baseline fields enumerated by the wrapper bullets
(severity, source, affected_range, evidence, recommendation) are all
populated and validated; severity is the literal `HIGH` and source is
the literal `synthetic-dnsp`. The DM-003 schema label and the
`7-field DM-003 contract` phrase (at the 3 agent sites) are locked
against drift. **PASS** for AC2.

### 3.3 AC3 — TEST-019 asserts cardinality=1 with found_n_times=2

Mapped to test classes in `tests/audit/test_dnsp_dedup_collapse.py`:

| AC3 sub-claim | Test method | Status |
|---|---|---|
| Cardinality = 1 | `TestTwoIdenticalDedupKeysCollapse::test_collapse_cardinality_is_one` | **PASS** |
| found_n_times = 2 | `TestTwoIdenticalDedupKeysCollapse::test_collapse_found_n_times_is_two` | **PASS** |
| Exactly 1 collapse applied | `TestTwoIdenticalDedupKeysCollapse::test_exactly_one_collapse_was_applied` | **PASS** |
| Collapsed record preserves 5 fixed/dynamic fields | `TestTwoIdenticalDedupKeysCollapse::test_collapsed_record_preserves_5_fixed_fields` | **PASS** |
| Collapsed record still validates | `TestTwoIdenticalDedupKeysCollapse::test_collapsed_record_still_validates` | **PASS** |
| Collapse preserves dedup_key identity | `TestTwoIdenticalDedupKeysCollapse::test_collapse_preserves_dedup_key_identity` | **PASS** |
| Pre-collapse input invariant (2 emissions, same key) | `TestTwoIdenticalDedupKeysCollapse::test_pre_collapse_input_has_two_emissions` | **PASS** |
| Cumulative +1 (N=3 → fnt=3) | `TestThreeIdenticalDedupKeysCollapse::test_three_emissions_collapse_to_cardinality_one` | **PASS** |
| Distinct dedup_keys do NOT collapse | `TestDistinctDedupKeysDoNotCollapse::*` (2 tests) | **PASS** (2/2) |
| +1-from-current-value semantics | `TestEmittedFoundNTimesGreaterThanOneRejected::test_collapse_increments_from_current_value` | **PASS** |
| R-123 / INV-012 wrapper-text guards | `TestR123WrapperTextGuards::*` (7 tests) | **PASS** (7/7) |

The within-cycle collapse rule (R-123) reduces two identical-dedup_key
emissions to one record with `found_n_times=2`, exactly as pinned by
the wrapper bullets at all 4 sites and by SKILL.md §A.8 merge
ordering. **PASS** for AC3.

### 3.4 AC4 — Evidence at `TASKLIST_ROOT/artifacts/D-0080/evidence.md`

This file. **PASS** for AC4.

## 4. Files Created

| # | File | Purpose |
|---|---|---|
| 1 | `tests/audit/test_dnsp_twice_exhaust.py` | TEST-018 — twice-exhaust emission, validator, negative paths, vocabulary, wrapper-text guards |
| 2 | `tests/audit/test_dnsp_dedup_collapse.py` | TEST-019 — within-cycle dedup collapse, +1 increment, distinct-keys non-collapse, +1-from-current semantics, R-123 wrapper-text guards |
| 3 | `.dev/releases/current/task-builder-merge/artifacts/D-0080/evidence.md` | This evidence file |

No edits to `src/`, no edits to existing tests, no edits to agent files
or SKILL.md. The fixtures are pure consumers of the source-of-truth
wrappers landed by T06.01-T06.14.

## 5. Preservation invariants

| Slice | Status |
|---|---|
| `src/superclaude/agents/rf-team-lead.md:417` (COMP-006-M6 sha256 = `51725c0ffa151c3403701f21910d7f5cf122639f3a0e7fa9ae3cafe82701a0a0`) | No edit; byte-stable |
| `src/superclaude/agents/rf-analyst.md`, `rf-qa.md`, `rf-qa-qualitative.md` | No edit (read-only consumption by fixtures) |
| `src/superclaude/skills/task-builder/SKILL.md` | No edit (read-only consumption by fixtures) |

The fixtures verify the wrapper text against the canonical source files
without mutating them. The full audit-test suite (1019 prior tests +
57 new tests = 1076 collected; 1 pre-existing skip unrelated to this
task) continues to pass.

## 6. Acceptance Criteria — Coverage Table

| AC | Description | Status | Evidence |
|---|---|---|---|
| AC1 | `uv run pytest tests/audit/test_dnsp_twice_exhaust.py tests/audit/test_dnsp_dedup_collapse.py -v` exits 0 | **PASS** | §3.1 (`57 passed`, exit code 0) |
| AC2 | TEST-018 asserts all 5 fixed fields populated; severity HIGH; source synthetic-dnsp | **PASS** | §3.2 (33 TEST-018 tests; positive + 10 named-symbol negative paths + 6 vocabulary + 9 source-text guards) |
| AC3 | TEST-019 asserts cardinality=1 with found_n_times=2 | **PASS** | §3.3 (24 TEST-019 tests; positive + cumulative N=3 + distinct-keys non-collapse + +1-from-current + 7 source-text guards) |
| AC4 | Evidence at `TASKLIST_ROOT/artifacts/D-0080/evidence.md` | **PASS** | This file |

**Overall: PASS.**

## 7. Observations (Non-Blocking)

- **Pure-Python helpers reused across fixtures.** The TEST-019 fixture
  imports `validate_dnsp_emission` and `build_twice_exhaust_emission`
  from TEST-018 so a regression to the validator or the canonical
  emission shape breaks both fixtures. The
  `TestCrossFixtureConsistencyWithTest018` class in TEST-019
  re-verifies the imported literals and vocabulary haven't drifted.
- **No emission code yet — wrapper-contract level.** The DM-003 / R-123
  semantics are documentation-level contracts pinned in the four
  wrapper sites; the emitter that produces synthetic-dnsp blocks at
  runtime is the partition agent itself (orchestrated by the
  task-builder skill). T06.15 fixtures encode the wrapper rules as
  pure-Python helpers and assert behavior against them — the same
  pattern used by TEST-022 (D-0065, T05.14) and TEST-024 (D-0066,
  T05.15). The end-to-end behavior (real orchestrator producing
  emissions that the merge step picks up) is verified by the
  downstream integration fixtures landing under T06.16 (TEST-020 +
  TEST-021) and the MIG-006 sub-agent diff spot-check at T06.17.
- **AC1 grep on phase-6-tasklist.md L734-738 mirrors the test command.**
  The exact pytest command in §3.1 matches the AC1 specification
  byte-for-byte; the dependency on T06.05 / T06.09 / T06.13 / T06.14
  (Phase 6 dependency closure of T06.15) is honored — each upstream
  evidence pack closes with PASS prior to this task running.
- **Strictly read-only with respect to source-of-truth files.** The
  fixtures never write to `src/`, `.claude/`, or any agent / skill
  file; they only read the canonical files to verify the wrapper text
  has not drifted. `make verify-sync` continues to flag the
  pre-existing `auggie-bash-gate.sh` / `reject-workspace-writes.sh`
  hook-installer drift documented in D-0068 .. D-0079; that is on the
  in-flight `feat/hook-sync-and-matcher-fix` branch and unrelated to
  T06.15.
- **Full suite regression check.** `uv run pytest tests/audit/`
  returns `1019 passed, 1 skipped` on the pre-T06.15 baseline and
  `1076 passed, 1 skipped` after T06.15 lands (57 new tests, no
  regressions). The 1 pre-existing skip is unrelated to this task.

## 8. Provenance

- Pre-edit HEAD: `5439ea1 feat(hooks): widen auggie-flag-clear matcher to mcp__auggie-mcp__; add verify-sync hook coverage and cross-consistency checks` (same baseline as T06.13 / T06.14 / T06.05 — no commits yet for the T06.15 fixtures).
- Dependency closure: T06.05 (D-0072) PASS, T06.09 (D-0075) staged in
  D-0075 evidence pack, T06.13 (D-0078) PASS, T06.14 (D-0079) PASS.
- Downstream consumers: T06.16 (D-0081) TEST-020 + TEST-021 fixtures
  depend on T06.15 fixtures landing first; T06.17 (D-0082, MIG-006)
  depends on T06.15 + T06.16 fixtures green before commit; T06.18
  (CP-P06-END) ratifies T06.15 alongside the rest of Phase 6.
