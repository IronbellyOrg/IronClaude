# D-0090 — TEST-025 Invariant-Preservation Composite (T07.09)

**Status:** PASS
**Roadmap Item:** R-150
**Surface Under Test:** NFR-CONV.6..10 (five load-bearing invariants)
**Fixture:** `tests/audit/test_invariant_preservation_NFR_6_through_10.py`
**Date:** 2026-05-18
**Auditor:** task-executor (T07.09)
**HEAD at audit:** `efaa33d` (`feat/hook-sync-and-matcher-fix`)

## 1. Scope

T07.09 commits the composite fixture demanded by R-150 — a single
pytest module that exercises each of the five load-bearing invariants
the Task-Builder Convergence v3.9 release commits to preserve:

| Inv. | Label | Detector reused | M7 dep. |
|---|---|---|---|
| NFR-CONV.6 | self-contained-item | `test_nfr_conv_6_self_contained.py` (T07.04 / D-0086) | T07.04 |
| NFR-CONV.7 | evidence-bound-item | `test_evidence_bound_tb_add_8.py` (T02.10 / D-0024) | — |
| NFR-CONV.8 | persistent-`.dev/tasks/`-artifact | live `.dev/tasks/` traversal (D-0087 §3.1) | T07.05 |
| NFR-CONV.9 | zero-trust QA | `test_nfr_conv_9_zero_trust.py` (T07.07 / D-0088) | T07.07 |
| NFR-CONV.10 | parallel-research | `test_dnsp_does_not_serialize_cohort.py` (T06.16 / D-0081) | — |

Per `phase-7-tasklist.md` line 403 the composite fixture must
"[exercise] all 5 invariants … per Negative Criteria." Each invariant's
existing per-surface detector is imported into the composite module so
a single pytest run names every invariant by ID and fails loudly the
moment any surface drifts.

## 2. Method

Each invariant has a dedicated `TestInvariantN_<label>` class. Detectors
are imported verbatim from the source-of-truth test modules:

- `run_all_tb_add` + `tb_add_1` from `test_nfr_conv_6_self_contained` —
  exercises the Q-DM-1 five-field schema (NFR-CONV.6).
- `tb_add_8` from `test_evidence_bound_tb_add_8` — exercises the
  per-item Context evidence binding (NFR-CONV.7).
- A direct traversal of `.dev/tasks/{to-do,done}/TASK-*/` collects the
  set of immediate subdirectory names and asserts the canonical set
  `{research, qa, synthesis, reviews, phase-outputs}` is preserved
  (NFR-CONV.8). `phase-outputs/` is the on-disk physical name for the
  logical `adversarial` bucket per D-0087 §3.1.
- `_score_rf_qa_verdict` + `PASS_BULLET`/`FAIL_BULLET`/`SEVERITY_TRIPLE`
  from `test_nfr_conv_9_zero_trust` — exercises the rf-qa.md verdict
  anchor and the 1-LOW-finding gate (NFR-CONV.9).
- `check_inv_021_n_minus_1_concurrency` +
  `build_canonical_overlap_spawn_log` + `build_serialized_spawn_log`
  from `test_dnsp_does_not_serialize_cohort` — exercises the cohort
  concurrency rule and the `INV-021-cohort-serialization-violation`
  rejection symbol (NFR-CONV.10).

A trailing `TestCompositeAggregateVerdict` class re-runs all five
detectors and asserts a single aggregate dict
`{NFR-CONV.6..10: PASS}`.

## 3. Result

```text
$ uv run pytest tests/audit/test_invariant_preservation_NFR_6_through_10.py -v
============================= test session starts ==============================
collected 19 items

TestCompositeFixtureWiring::test_five_invariants_enumerated PASSED       [  5%]
TestCompositeFixtureWiring::test_all_detector_fixtures_resolvable PASSED [ 10%]
TestCompositeFixtureWiring::test_dev_tasks_root_exists PASSED            [ 15%]
TestInvariant1_SelfContainedItem::test_full_fields_fixture_all_tb_add_pass PASSED
TestInvariant1_SelfContainedItem::test_stripped_fixture_fails_tb_add_1_with_named_field PASSED
TestInvariant1_SelfContainedItem::test_q_dm_1_schema_field_count PASSED
TestInvariant2_EvidenceBoundItem::test_bare_path_fixture_fails_tb_add_8 PASSED
TestInvariant2_EvidenceBoundItem::test_file_line_fixture_all_pass PASSED
TestInvariant2_EvidenceBoundItem::test_justified_absence_fixture_all_pass PASSED
TestInvariant3_PersistentArtifact::test_canonical_subdirs_all_present PASSED
TestInvariant3_PersistentArtifact::test_canonical_subdir_set_unchanged_by_rename PASSED
TestInvariant3_PersistentArtifact::test_task_id_naming_pattern_preserved PASSED
TestInvariant4_ZeroTrustQA::test_pass_bullet_byte_identical PASSED
TestInvariant4_ZeroTrustQA::test_fail_bullet_byte_identical PASSED
TestInvariant4_ZeroTrustQA::test_severity_triple_intact PASSED
TestInvariant4_ZeroTrustQA::test_one_low_finding_scores_fail PASSED
TestInvariant5_ParallelResearch::test_concurrent_spawn_log_accepted PASSED
TestInvariant5_ParallelResearch::test_serialized_spawn_log_rejected PASSED
TestCompositeAggregateVerdict::test_all_five_invariants_pass PASSED       [100%]

============================== 19 passed in 0.04s ==============================
```

Exit 0. All 19 assertions across the 5 invariant classes pass.

## 4. Regression sweep

The composite import-graph re-runs the source-of-truth modules. Bundled
sweep against the four detector modules + the composite:

```text
$ uv run pytest \
  tests/audit/test_nfr_conv_6_self_contained.py \
  tests/audit/test_nfr_conv_9_zero_trust.py \
  tests/audit/test_evidence_bound_tb_add_8.py \
  tests/audit/test_dnsp_does_not_serialize_cohort.py \
  tests/audit/test_invariant_preservation_NFR_6_through_10.py -q
106 passed in 0.11s
```

No regression in the detector source modules introduced by the new
composite.

## 5. Acceptance-Criteria Trace (`phase-7-tasklist.md` T07.09)

| AC | Result | Evidence |
|---|---|---|
| `uv run pytest tests/audit/test_invariant_preservation_NFR_6_through_10.py -v` exits 0 | PASS | §3 — 19/19 PASS |
| Composite fixture exercises each of the 5 invariants (NFR-CONV.6..10) | PASS | §2 — one `TestInvariantN_*` class per invariant + 5-key aggregate dict in `TestCompositeAggregateVerdict` |
| All 5 invariant assertions pass | PASS | §3 + `TestCompositeAggregateVerdict::test_all_five_invariants_pass` PASSED |
| Evidence at `TASKLIST_ROOT/artifacts/D-0090/evidence.md` | PASS | this file |

## 6. Dependencies satisfied

| Dep (per `phase-7-tasklist.md` T07.09) | Status | Evidence |
|---|---|---|
| T07.04 (NFR-CONV.6 fixture committed) | PASS | D-0086 evidence; `test_nfr_conv_6_self_contained.py` green |
| T07.07 (NFR-CONV.9 + NFR-CONV.2 fixtures committed) | PASS | D-0088 evidence; `test_nfr_conv_9_zero_trust.py` green (35/35) |
| T07.08 (NFR-CONV-R1 + NFR-CONV.3 + TEST-023) | PASS | D-0089 evidence; `test_hidden_input_guard.py` green |

## 7. Verdict

**PASS** — TEST-025 composite invariant-preservation gate committed
at `tests/audit/test_invariant_preservation_NFR_6_through_10.py`. All
five load-bearing invariants (NFR-CONV.6..10) green at HEAD `efaa33d`.

## 8. Reproduce

```bash
uv run pytest tests/audit/test_invariant_preservation_NFR_6_through_10.py -v
```

Expected: 19 passed, exit 0.
