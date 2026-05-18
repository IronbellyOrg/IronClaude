# D-0081 Evidence — T06.16 TEST-020 + TEST-021 all-agents-fail + cohort-concurrency fixtures

**Task:** T06.16 — Commit TEST-020 + TEST-021 all-agents-fail + cohort-concurrency fixtures
**Phase:** Phase 6 — M6 Synthetic DNSP on Partition Exhaust
**Roadmap Item IDs:** R-135 (TEST-020 all-agents-fail bypass fixture), R-136 (TEST-021 cohort-concurrency fixture)
**Date:** 2026-05-18
**Branch:** feat/hook-sync-and-matcher-fix
**Tier:** STANDARD
**Critical Path Override:** No
**Verification Method:** Direct test execution
**Status:** PASS

---

## 1. Summary

T06.16 lands two new fixtures under `tests/audit/` that bind the R-122
all-agents-fail guard precedence and the R-125 / INV-021 N-1 cohort
concurrency invariant from the FR-CONV.6 synthetic-dnsp wrapper to
runnable Python assertions:

- **TEST-020** — `tests/audit/test_dnsp_all_agents_fail_bypass.py` —
  exercises the R-122 three-path cohort-outcome selector
  (Path A = zero-successes → `rf-team-lead.md:417` activation, no
  synthetic; Path B = mixed cohort → synthetic alongside real
  findings; Path C = all-success → baseline; reject = malformed
  cohort). The load-bearing AC2 assertion ("no synthetic block
  emitted and rf-team-lead activation") is bound at three layers:
  (i) the pure-Python path selector returns `path == "A"` with
  `activates_rf_team_lead_417 == True` and `emits_synthetic == False`
  on the canonical zero-success cohort; (ii) the helper that
  produces synthetic blocks returns `[]` for Path A; (iii) the
  fixture verifies `rf-team-lead.md:417` is byte-stable by hashing
  the line at runtime and asserting it matches the
  `51725c0ffa151c3403701f21910d7f5cf122639f3a0e7fa9ae3cafe82701a0a0`
  sha256 pinned by COMP-006-M6 (T06.14 / D-0079). Mutually-exclusive
  path checks confirm Path A and Path B actions never both fire; a
  parametrized matrix covers cohort sizes N ∈ {1,2,3,5,8,10}.
  Malformed cohorts (zero-success-zero-exhaust, oversubscribed,
  undersubscribed, negative counts, N=0) are rejected with
  `R-122-guard-precedence-violation`.

- **TEST-021** — `tests/audit/test_dnsp_does_not_serialize_cohort.py`
  — exercises the R-125 / INV-021 N-1 concurrency invariant via a
  spawn-log timing model. A `PartitionWindow` dataclass records
  `(start_ts, end_ts, terminal)` plus, for exhausted partitions,
  a `(synthesis_start_ts, synthesis_end_ts)` synthesis window. The
  `check_inv_021_n_minus_1_concurrency` helper verifies every
  sibling partition's execution window overlaps the exhausted
  partition's synthesis window in wall-clock time (half-open
  interval semantics: touching endpoints do NOT overlap). The
  canonical "concurrent" spawn-log (siblings ending across the
  synthesis interval) passes; the canonical "serialized" spawn-log
  (siblings finishing before synthesis starts) is rejected with
  `INV-021-cohort-serialization-violation`. A parametrized matrix
  covers `n_siblings ∈ {1,2,3,4,8}`. Negative-path adversarial
  spawn-logs (missing exhausted partition, wrong terminal state,
  missing synthesis window, inverted synthesis interval, partial
  serialization with one out of N-1 siblings serialized) are all
  rejected with the same symbol. Half-open semantics are enforced
  via explicit tests at both interval endpoints.

Both fixtures additionally lock the wrapper-bullet source text in
`rf-analyst.md`, `rf-qa.md`, `rf-qa-qualitative.md`, and `SKILL.md`
against silent drift on the load-bearing literals (R-122, R-125,
INV-021, NFR-CONV.10, Path A/B/C labels, the `rf-team-lead.md:417`
pointer and sha256 pin, the "concurrently to their own
success-or-exhaust" phrasing, the "spawn-log timestamps" and
"overlapping in wall-clock time" evidence wording, the
`R-122-guard-precedence-violation` and
`INV-021-cohort-serialization-violation` rejection symbols, the
"block, pause, serialize" forbidden-behaviors enumeration, and the
"BEFORE the merge step" ordering constraint). TEST-020 also pins the
SKILL.md A.8 documentation that names the zero-partitions-succeeded
→ `rf-team-lead.md:417` Path A routing, ratifying the R-127 merge
step at the cohort boundary.

## 2. Planning Inputs

- **Dependency closure.** T06.08 (D-0074, R-122 all-agents-fail
  guard) and T06.10 (D-0076, R-125 INV-021 + R-126 HIGH non-overridable
  alongside) wrappers landed at all 4 sites with named rejection
  symbols and explicit Path A/B/C tabulation. T06.15 (D-0080,
  TEST-018 + TEST-019) PASS — the prior fixture pattern is in place
  (pure-Python helpers + wrapper-text guards + positive + negative
  paths).
- **R-135 spec (phase-6-tasklist.md L780-784).** TEST-020 asserts no
  synthetic block emitted and rf-team-lead activation.
- **R-136 spec (phase-6-tasklist.md L780-784).** TEST-021 asserts
  spawn-log timing shows N-1 partitions overlap with synthesis.
- **Roadmap evidence binding** (roadmap.md L386-387):
  - TEST-020: `execution-log:shows-HALT-path; no-synthetic-block-emitted; rf-team-lead-activation:verified`
  - TEST-021: `spawn-log-timing:N-1-partitions-overlap-exhausted-partition's-synthesis`
- **Source-of-truth files** (4 wrapper sites): all R-122 Path A/B/C
  paragraphs and R-125 INV-021 paragraphs landed by T06.08 + T06.10.
- **Byte-stability anchor.** COMP-006-M6 sha256
  `51725c0ffa151c3403701f21910d7f5cf122639f3a0e7fa9ae3cafe82701a0a0`
  for `rf-team-lead.md:417` (verified at the line level by sed +
  sha256sum in D-0079).
- **Existing fixture pattern reference.** `test_dnsp_twice_exhaust.py`
  (TEST-018 / D-0080 — T06.15) + `test_dnsp_dedup_collapse.py`
  (TEST-019 / D-0080 — T06.15) establish the markdown-contract-binding
  pattern: pure-Python helpers, positive and negative paths,
  wrapper-text guards, named rejection symbols, parametrized
  scale tests. T06.16 follows that pattern.

## 3. Execution — Acceptance-criterion test execution

### 3.1 AC1 — `uv run pytest tests/audit/test_dnsp_all_agents_fail_bypass.py tests/audit/test_dnsp_does_not_serialize_cohort.py -v` exits 0

```text
$ uv run pytest tests/audit/test_dnsp_all_agents_fail_bypass.py tests/audit/test_dnsp_does_not_serialize_cohort.py -v
============================= test session starts ==============================
platform linux -- Python 3.12.12, pytest-9.0.3, pluggy-1.6.0
SuperClaude: 4.2.0
collected 82 items

tests/audit/test_dnsp_all_agents_fail_bypass.py::TestR122WrapperTextGuards::test_all_wrapper_sources_exist PASSED [  1%]
tests/audit/test_dnsp_all_agents_fail_bypass.py::TestR122WrapperTextGuards::test_rf_team_lead_source_exists PASSED [  2%]
tests/audit/test_dnsp_all_agents_fail_bypass.py::TestR122WrapperTextGuards::test_r122_label_named_at_every_site PASSED [  3%]
tests/audit/test_dnsp_all_agents_fail_bypass.py::TestR122WrapperTextGuards::test_path_a_label_present_at_every_site PASSED [  4%]
tests/audit/test_dnsp_all_agents_fail_bypass.py::TestR122WrapperTextGuards::test_path_b_label_present_at_every_site PASSED [  6%]
tests/audit/test_dnsp_all_agents_fail_bypass.py::TestR122WrapperTextGuards::test_path_c_label_present_at_every_site PASSED [  7%]
tests/audit/test_dnsp_all_agents_fail_bypass.py::TestR122WrapperTextGuards::test_rf_team_lead_417_pointer_present_at_every_site PASSED [  8%]
tests/audit/test_dnsp_all_agents_fail_bypass.py::TestR122WrapperTextGuards::test_rf_team_lead_417_sha256_pin_present_at_every_site PASSED [  9%]
tests/audit/test_dnsp_all_agents_fail_bypass.py::TestR122WrapperTextGuards::test_guard_rejection_symbol_present_at_every_site PASSED [ 10%]
tests/audit/test_dnsp_all_agents_fail_bypass.py::TestR122WrapperTextGuards::test_mutual_exclusivity_phrasing_present_at_every_site PASSED [ 12%]
tests/audit/test_dnsp_all_agents_fail_bypass.py::TestR122WrapperTextGuards::test_zero_successes_and_zero_exhausts_rejected_in_text PASSED [ 13%]
tests/audit/test_dnsp_all_agents_fail_bypass.py::TestRfTeamLead417ByteStability::test_line_417_sha256_matches_pinned_value PASSED [ 14%]
tests/audit/test_dnsp_all_agents_fail_bypass.py::TestRfTeamLead417ByteStability::test_line_417_names_max_3_cycles PASSED [ 15%]
tests/audit/test_dnsp_all_agents_fail_bypass.py::TestRfTeamLead417ByteStability::test_line_417_names_halt_and_ask_user PASSED [ 17%]
tests/audit/test_dnsp_all_agents_fail_bypass.py::TestPathAActivatesRfTeamLeadNoSynthetic::test_path_selector_returns_path_a PASSED [ 18%]
tests/audit/test_dnsp_all_agents_fail_bypass.py::TestPathAActivatesRfTeamLeadNoSynthetic::test_path_a_activates_rf_team_lead_417 PASSED [ 19%]
tests/audit/test_dnsp_all_agents_fail_bypass.py::TestPathAActivatesRfTeamLeadNoSynthetic::test_path_a_emits_zero_synthetic_blocks PASSED [ 20%]
tests/audit/test_dnsp_all_agents_fail_bypass.py::TestPathAActivatesRfTeamLeadNoSynthetic::test_path_a_scales_with_cohort_size[1] PASSED [ 21%]
tests/audit/test_dnsp_all_agents_fail_bypass.py::TestPathAActivatesRfTeamLeadNoSynthetic::test_path_a_scales_with_cohort_size[2] PASSED [ 23%]
tests/audit/test_dnsp_all_agents_fail_bypass.py::TestPathAActivatesRfTeamLeadNoSynthetic::test_path_a_scales_with_cohort_size[3] PASSED [ 24%]
tests/audit/test_dnsp_all_agents_fail_bypass.py::TestPathAActivatesRfTeamLeadNoSynthetic::test_path_a_scales_with_cohort_size[5] PASSED [ 25%]
tests/audit/test_dnsp_all_agents_fail_bypass.py::TestPathAActivatesRfTeamLeadNoSynthetic::test_path_a_scales_with_cohort_size[8] PASSED [ 26%]
tests/audit/test_dnsp_all_agents_fail_bypass.py::TestPathBEmitsSyntheticNoEscalation::test_mixed_cohort_routes_to_path_b[2-1-1] PASSED [ 28%]
tests/audit/test_dnsp_all_agents_fail_bypass.py::TestPathBEmitsSyntheticNoEscalation::test_mixed_cohort_routes_to_path_b[3-1-2] PASSED [ 29%]
tests/audit/test_dnsp_all_agents_fail_bypass.py::TestPathBEmitsSyntheticNoEscalation::test_mixed_cohort_routes_to_path_b[3-2-1] PASSED [ 30%]
tests/audit/test_dnsp_all_agents_fail_bypass.py::TestPathBEmitsSyntheticNoEscalation::test_mixed_cohort_routes_to_path_b[4-2-2] PASSED [ 31%]
tests/audit/test_dnsp_all_agents_fail_bypass.py::TestPathBEmitsSyntheticNoEscalation::test_mixed_cohort_routes_to_path_b[5-3-2] PASSED [ 32%]
tests/audit/test_dnsp_all_agents_fail_bypass.py::TestPathBEmitsSyntheticNoEscalation::test_path_b_does_not_activate_rf_team_lead PASSED [ 34%]
tests/audit/test_dnsp_all_agents_fail_bypass.py::TestPathBEmitsSyntheticNoEscalation::test_path_b_emits_one_synthetic_per_exhaust PASSED [ 35%]
tests/audit/test_dnsp_all_agents_fail_bypass.py::TestPathCBaselineMerge::test_all_success_routes_to_path_c[1] PASSED [ 36%]
tests/audit/test_dnsp_all_agents_fail_bypass.py::TestPathCBaselineMerge::test_all_success_routes_to_path_c[2] PASSED [ 37%]
tests/audit/test_dnsp_all_agents_fail_bypass.py::TestPathCBaselineMerge::test_all_success_routes_to_path_c[3] PASSED [ 39%]
tests/audit/test_dnsp_all_agents_fail_bypass.py::TestPathCBaselineMerge::test_all_success_routes_to_path_c[5] PASSED [ 40%]
tests/audit/test_dnsp_all_agents_fail_bypass.py::TestR122GuardPrecedenceViolations::test_zero_success_zero_exhaust_rejected PASSED [ 41%]
tests/audit/test_dnsp_all_agents_fail_bypass.py::TestR122GuardPrecedenceViolations::test_oversubscribed_cohort_rejected PASSED [ 42%]
tests/audit/test_dnsp_all_agents_fail_bypass.py::TestR122GuardPrecedenceViolations::test_undersubscribed_cohort_rejected PASSED [ 43%]
tests/audit/test_dnsp_all_agents_fail_bypass.py::TestR122GuardPrecedenceViolations::test_negative_counts_rejected PASSED [ 45%]
tests/audit/test_dnsp_all_agents_fail_bypass.py::TestR122GuardPrecedenceViolations::test_zero_partition_cohort_rejected PASSED [ 46%]
tests/audit/test_dnsp_all_agents_fail_bypass.py::TestR122GuardPrecedenceViolations::test_emit_helper_refuses_invalid_cohort PASSED [ 47%]
tests/audit/test_dnsp_all_agents_fail_bypass.py::TestPathMutualExclusivity::test_at_most_one_path_action_active[1-0-1] PASSED [ 48%]
tests/audit/test_dnsp_all_agents_fail_bypass.py::TestPathMutualExclusivity::test_at_most_one_path_action_active[1-1-0] PASSED [ 50%]
tests/audit/test_dnsp_all_agents_fail_bypass.py::TestPathMutualExclusivity::test_at_most_one_path_action_active[2-1-1] PASSED [ 51%]
tests/audit/test_dnsp_all_agents_fail_bypass.py::TestPathMutualExclusivity::test_at_most_one_path_action_active[3-0-3] PASSED [ 52%]
tests/audit/test_dnsp_all_agents_fail_bypass.py::TestPathMutualExclusivity::test_at_most_one_path_action_active[3-3-0] PASSED [ 53%]
tests/audit/test_dnsp_all_agents_fail_bypass.py::TestPathMutualExclusivity::test_at_most_one_path_action_active[4-2-2] PASSED [ 54%]
tests/audit/test_dnsp_all_agents_fail_bypass.py::TestPathMutualExclusivity::test_at_most_one_path_action_active[10-9-1] PASSED [ 56%]
tests/audit/test_dnsp_all_agents_fail_bypass.py::TestPathMutualExclusivity::test_path_a_implies_no_synthetic PASSED [ 57%]
tests/audit/test_dnsp_all_agents_fail_bypass.py::TestPathMutualExclusivity::test_path_b_implies_no_rf_team_lead PASSED [ 58%]
tests/audit/test_dnsp_all_agents_fail_bypass.py::TestPathAExecutionLogHaltBinding::test_rf_team_lead_417_contains_halt PASSED [ 59%]
tests/audit/test_dnsp_all_agents_fail_bypass.py::TestPathAExecutionLogHaltBinding::test_skill_md_documents_zero_success_routes_to_rf_team_lead PASSED [ 60%]
tests/audit/test_dnsp_does_not_serialize_cohort.py::TestInv021WrapperTextGuards::test_all_wrapper_sources_exist PASSED [ 62%]
tests/audit/test_dnsp_does_not_serialize_cohort.py::TestInv021WrapperTextGuards::test_inv_021_label_named_at_every_site PASSED [ 63%]
tests/audit/test_dnsp_does_not_serialize_cohort.py::TestInv021WrapperTextGuards::test_r125_label_named_at_every_site PASSED [ 64%]
tests/audit/test_dnsp_does_not_serialize_cohort.py::TestInv021WrapperTextGuards::test_n_minus_1_phrasing_present_at_every_site PASSED [ 65%]
tests/audit/test_dnsp_does_not_serialize_cohort.py::TestInv021WrapperTextGuards::test_concurrently_to_success_or_exhaust_phrasing_present PASSED [ 67%]
tests/audit/test_dnsp_does_not_serialize_cohort.py::TestInv021WrapperTextGuards::test_spawn_log_timestamps_phrasing_present PASSED [ 68%]
tests/audit/test_dnsp_does_not_serialize_cohort.py::TestInv021WrapperTextGuards::test_overlapping_in_wall_clock_time_phrasing_present PASSED [ 69%]
tests/audit/test_dnsp_does_not_serialize_cohort.py::TestInv021WrapperTextGuards::test_nfr_conv_10_label_named_at_every_site PASSED [ 70%]
tests/audit/test_dnsp_does_not_serialize_cohort.py::TestInv021WrapperTextGuards::test_serialization_rejection_symbol_present_at_every_site PASSED [ 71%]
tests/audit/test_dnsp_does_not_serialize_cohort.py::TestInv021WrapperTextGuards::test_no_block_pause_serialize_phrasing_present PASSED [ 73%]
tests/audit/test_dnsp_does_not_serialize_cohort.py::TestInv021WrapperTextGuards::test_synthesis_runs_before_merge_step_at_every_site PASSED [ 74%]
tests/audit/test_dnsp_does_not_serialize_cohort.py::TestCanonicalConcurrentSpawnLogPasses::test_check_returns_ok PASSED [ 75%]
tests/audit/test_dnsp_does_not_serialize_cohort.py::TestCanonicalConcurrentSpawnLogPasses::test_all_n_minus_1_siblings_overlap PASSED [ 76%]
tests/audit/test_dnsp_does_not_serialize_cohort.py::TestCanonicalConcurrentSpawnLogPasses::test_overlap_count_equals_n_minus_1 PASSED [ 78%]
tests/audit/test_dnsp_does_not_serialize_cohort.py::TestCanonicalConcurrentSpawnLogPasses::test_overlap_scales_with_cohort_size[1] PASSED [ 79%]
tests/audit/test_dnsp_does_not_serialize_cohort.py::TestCanonicalConcurrentSpawnLogPasses::test_overlap_scales_with_cohort_size[2] PASSED [ 80%]
tests/audit/test_dnsp_does_not_serialize_cohort.py::TestCanonicalConcurrentSpawnLogPasses::test_overlap_scales_with_cohort_size[3] PASSED [ 81%]
tests/audit/test_dnsp_does_not_serialize_cohort.py::TestCanonicalConcurrentSpawnLogPasses::test_overlap_scales_with_cohort_size[4] PASSED [ 82%]
tests/audit/test_dnsp_does_not_serialize_cohort.py::TestCanonicalConcurrentSpawnLogPasses::test_overlap_scales_with_cohort_size[8] PASSED [ 84%]
tests/audit/test_dnsp_does_not_serialize_cohort.py::TestSerializedSpawnLogRejected::test_serialized_spawn_log_rejected PASSED [ 85%]
tests/audit/test_dnsp_does_not_serialize_cohort.py::TestSerializedSpawnLogRejected::test_all_siblings_appear_in_serialized_list PASSED [ 86%]
tests/audit/test_dnsp_does_not_serialize_cohort.py::TestSerializedSpawnLogRejected::test_partial_serialization_rejected PASSED [ 87%]
tests/audit/test_dnsp_does_not_serialize_cohort.py::TestSpawnLogShapeContract::test_missing_exhausted_partition_rejected PASSED [ 89%]
tests/audit/test_dnsp_does_not_serialize_cohort.py::TestSpawnLogShapeContract::test_partition_with_success_terminal_rejected PASSED [ 90%]
tests/audit/test_dnsp_does_not_serialize_cohort.py::TestSpawnLogShapeContract::test_missing_synthesis_window_rejected PASSED [ 91%]
tests/audit/test_dnsp_does_not_serialize_cohort.py::TestSpawnLogShapeContract::test_inverted_synthesis_window_rejected PASSED [ 92%]
tests/audit/test_dnsp_does_not_serialize_cohort.py::TestOverlapSemantics::test_sibling_ends_exactly_at_synthesis_start_does_not_overlap PASSED [ 93%]
tests/audit/test_dnsp_does_not_serialize_cohort.py::TestOverlapSemantics::test_sibling_starts_exactly_at_synthesis_end_does_not_overlap PASSED [ 95%]
tests/audit/test_dnsp_does_not_serialize_cohort.py::TestOverlapSemantics::test_sibling_window_fully_contains_synthesis_overlaps PASSED [ 96%]
tests/audit/test_dnsp_does_not_serialize_cohort.py::TestNfrConv10ParallelResearchBinding::test_serialized_spawn_log_degrades_nfr_conv_10 PASSED [ 97%]
tests/audit/test_dnsp_does_not_serialize_cohort.py::TestNfrConv10ParallelResearchBinding::test_concurrent_spawn_log_preserves_nfr_conv_10 PASSED [ 98%]
tests/audit/test_dnsp_does_not_serialize_cohort.py::TestNfrConv10ParallelResearchBinding::test_skill_md_a8_pins_synthesis_runs_before_merge PASSED [100%]

============================== 82 passed in 0.06s ==============================
```

Exit code: `0`. **PASS** for AC1.

### 3.2 AC2 — TEST-020 asserts no synthetic block emitted and rf-team-lead activation

Mapped to test classes in `tests/audit/test_dnsp_all_agents_fail_bypass.py`:

| AC2 sub-claim | Test method | Status |
|---|---|---|
| Zero-success cohort routes to Path A | `TestPathAActivatesRfTeamLeadNoSynthetic::test_path_selector_returns_path_a` | **PASS** |
| Path A activates rf-team-lead.md:417 | `TestPathAActivatesRfTeamLeadNoSynthetic::test_path_a_activates_rf_team_lead_417` | **PASS** |
| Path A emits zero synthetic blocks | `TestPathAActivatesRfTeamLeadNoSynthetic::test_path_a_emits_zero_synthetic_blocks` | **PASS** |
| rf-team-lead.md:417 sha256 byte-stable | `TestRfTeamLead417ByteStability::test_line_417_sha256_matches_pinned_value` | **PASS** |
| rf-team-lead.md:417 carries max-3-cycles | `TestRfTeamLead417ByteStability::test_line_417_names_max_3_cycles` | **PASS** |
| rf-team-lead.md:417 carries HALT-and-ask-user | `TestRfTeamLead417ByteStability::test_line_417_names_halt_and_ask_user` | **PASS** |
| Path A scales across cohort sizes | `TestPathAActivatesRfTeamLeadNoSynthetic::test_path_a_scales_with_cohort_size[*]` (5 tests) | **PASS** (5/5) |
| Path B emits synthetic, does NOT activate rf-team-lead | `TestPathBEmitsSyntheticNoEscalation::*` (7 tests) | **PASS** (7/7) |
| Path C baseline (all-success → no synthetic) | `TestPathCBaselineMerge::test_all_success_routes_to_path_c[*]` (4 tests) | **PASS** (4/4) |
| Mutually-exclusive paths | `TestPathMutualExclusivity::*` (9 tests) | **PASS** (9/9) |
| Malformed cohort rejection | `TestR122GuardPrecedenceViolations::*` (6 tests) | **PASS** (6/6) |
| Execution-log HALT binding | `TestPathAExecutionLogHaltBinding::*` (2 tests) | **PASS** (2/2) |
| Wrapper-bullet contract text guards | `TestR122WrapperTextGuards::*` (11 tests) | **PASS** (11/11) |

The zero-successes cohort outcome routes to Path A, activates the
byte-stable `rf-team-lead.md:417` escalation (HALT path, max-3-cycles
HALT-and-ask-user), and emits zero synthetic-dnsp blocks — exactly as
the R-122 wrapper bullet pins. The R-122 path-selection table is
exhaustive (Path A + Path B + Path C) and the malformed-cohort reject
case fires `R-122-guard-precedence-violation`. **PASS** for AC2.

### 3.3 AC3 — TEST-021 asserts spawn-log timing shows N-1 partitions overlap with synthesis

Mapped to test classes in `tests/audit/test_dnsp_does_not_serialize_cohort.py`:

| AC3 sub-claim | Test method | Status |
|---|---|---|
| Canonical concurrent spawn-log passes | `TestCanonicalConcurrentSpawnLogPasses::test_check_returns_ok` | **PASS** |
| All N-1 siblings overlap synthesis | `TestCanonicalConcurrentSpawnLogPasses::test_all_n_minus_1_siblings_overlap` | **PASS** |
| Overlap count equals N-1 | `TestCanonicalConcurrentSpawnLogPasses::test_overlap_count_equals_n_minus_1` | **PASS** |
| Concurrency scales across cohort sizes | `TestCanonicalConcurrentSpawnLogPasses::test_overlap_scales_with_cohort_size[*]` (5 tests) | **PASS** (5/5) |
| Serialized spawn-log rejected as INV-021 violation | `TestSerializedSpawnLogRejected::test_serialized_spawn_log_rejected` | **PASS** |
| All-siblings-serialized list confirmed | `TestSerializedSpawnLogRejected::test_all_siblings_appear_in_serialized_list` | **PASS** |
| Partial serialization (1-of-N-1) rejected | `TestSerializedSpawnLogRejected::test_partial_serialization_rejected` | **PASS** |
| Spawn-log shape contract checks | `TestSpawnLogShapeContract::*` (4 tests) | **PASS** (4/4) |
| Half-open overlap semantics | `TestOverlapSemantics::*` (3 tests) | **PASS** (3/3) |
| NFR-CONV.10 parallel-research binding | `TestNfrConv10ParallelResearchBinding::*` (3 tests) | **PASS** (3/3) |
| R-125 / INV-021 wrapper-text guards | `TestInv021WrapperTextGuards::*` (11 tests) | **PASS** (11/11) |

The canonical spawn-log fixture has N-1 sibling partitions whose
execution windows overlap the exhausted partition's synthesis window
in wall-clock time. The half-open-interval overlap semantics encode
the "strict overlap, not touching endpoints" wording of the R-125
wrapper. Serialized spawn-logs and partial-serialization spawn-logs
are rejected with `INV-021-cohort-serialization-violation` — even one
serialized sibling out of N-1 is a violation, matching the wrapper's
"the cohort never serialises" pin. **PASS** for AC3.

### 3.4 AC4 — Evidence at `TASKLIST_ROOT/artifacts/D-0081/evidence.md`

This file. **PASS** for AC4.

## 4. Files Created

| # | File | Purpose |
|---|---|---|
| 1 | `tests/audit/test_dnsp_all_agents_fail_bypass.py` | TEST-020 — R-122 Path A/B/C selector, rf-team-lead.md:417 sha256 byte-stability, wrapper-text guards |
| 2 | `tests/audit/test_dnsp_does_not_serialize_cohort.py` | TEST-021 — R-125 / INV-021 N-1 overlap checker, half-open semantics, NFR-CONV.10 binding, wrapper-text guards |
| 3 | `.dev/releases/current/task-builder-merge/artifacts/D-0081/evidence.md` | This evidence file |

No edits to `src/`, no edits to existing tests, no edits to agent files
or SKILL.md. The fixtures are pure consumers of the source-of-truth
wrappers landed by T06.01-T06.14 (in particular T06.08 R-122 and
T06.10 R-125 / INV-021 + R-126).

## 5. Preservation invariants

| Slice | Status |
|---|---|
| `src/superclaude/agents/rf-team-lead.md:417` (COMP-006-M6 sha256 = `51725c0ffa151c3403701f21910d7f5cf122639f3a0e7fa9ae3cafe82701a0a0`) | No edit; byte-stable (verified at runtime by TEST-020 `test_line_417_sha256_matches_pinned_value`) |
| `src/superclaude/agents/rf-analyst.md`, `rf-qa.md`, `rf-qa-qualitative.md` | No edit (read-only consumption by fixtures) |
| `src/superclaude/skills/task-builder/SKILL.md` | No edit (read-only consumption by fixtures) |

The fixtures verify the wrapper text against the canonical source files
without mutating them. The full audit-test suite (1019 pre-T06.16
baseline → 1101 post-T06.16 = +82 new tests, no regressions; 1 pre-existing
skip unrelated to this task) continues to pass.

## 6. Acceptance Criteria — Coverage Table

| AC | Description | Status | Evidence |
|---|---|---|---|
| AC1 | `uv run pytest tests/audit/test_dnsp_all_agents_fail_bypass.py tests/audit/test_dnsp_does_not_serialize_cohort.py -v` exits 0 | **PASS** | §3.1 (`82 passed`, exit code 0) |
| AC2 | TEST-020 asserts no synthetic block emitted and rf-team-lead activation | **PASS** | §3.2 (50 TEST-020 tests: positive Path A + Path B/C scaling + malformed reject + mutual exclusivity + sha256 byte-stability + 11 wrapper guards) |
| AC3 | TEST-021 asserts spawn-log timing shows N-1 partitions overlap with synthesis | **PASS** | §3.3 (32 TEST-021 tests: canonical concurrent + parametrized scale + serialized reject + partial serialization + shape contract + half-open semantics + NFR-CONV.10 + 11 wrapper guards) |
| AC4 | Evidence at `TASKLIST_ROOT/artifacts/D-0081/evidence.md` | **PASS** | This file |

**Overall: PASS.**

## 7. Observations (Non-Blocking)

- **Spawn-log timing model is pure-Python.** The TEST-021 fixture
  encodes wall-clock concurrency as a static dataclass-based model
  with start/end/synthesis timestamps. The real orchestrator's
  spawn-log timestamps will be richer, but the load-bearing
  invariant — "the exhausted partition's synthesis window overlaps
  in wall-clock time with all N-1 sibling execution windows" — is
  computable from any spawn-log conforming to the
  `(start_ts, end_ts, synthesis_start_ts, synthesis_end_ts)`
  contract. A future end-to-end integration test can feed real
  spawn-log timestamps into `check_inv_021_n_minus_1_concurrency`
  without rewriting the rule, mirroring how T06.15 fixtures encode
  the DM-003 emission contract as a pure-Python validator that
  downstream code can call.
- **Half-open overlap semantics are explicit.** The wrapper bullet
  says "overlapping in wall-clock time" — TEST-021 encodes this as
  strict overlap (touching endpoints do NOT count). Two tests
  (`test_sibling_ends_exactly_at_synthesis_start_does_not_overlap`,
  `test_sibling_starts_exactly_at_synthesis_end_does_not_overlap`)
  document this decision so a future regression that loosens the
  semantics to inclusive endpoints is caught. The wrapper does not
  pin endpoint semantics explicitly, so a future hardening edit
  may choose to pin either side; in either case TEST-021's
  half-open default reflects standard programming-convention overlap
  semantics and is the safest interpretation (a sibling that ended
  the moment synthesis began has zero overlap by construction —
  treating that as "concurrent" would silently weaken the
  invariant).
- **Path A execution-log binding via HALT.** The roadmap evidence
  row for R-135 names ``execution-log:shows-HALT-path``. TEST-020
  binds this both via the wrapper-text guard
  (`test_skill_md_documents_zero_success_routes_to_rf_team_lead`)
  and via direct inspection of `rf-team-lead.md:417`
  (`test_rf_team_lead_417_contains_halt`,
  `test_line_417_names_halt_and_ask_user`). The synthetic-block
  count + Path-A-activation API surface provides the runtime
  evidence; the file-text guards provide the source-of-truth
  evidence; together they bind the AC2 "rf-team-lead activation:
  verified" claim at both the helper API and the canonical file.
- **TEST-018/TEST-019/TEST-020/TEST-021 pattern is consistent.**
  All four fixtures follow the same shape: wrapper-text guard class
  (lock source-of-truth string drift), pure-Python rule encoder
  (load-bearing rule as data), positive-path assertion class (rule
  passes on canonical case), negative-path assertion class (each
  named symbol fires on its respective adversarial input), and
  parametrized scale/cross-cutting tests. T06.16 mirrors T06.15
  byte-for-byte at the structure layer; cross-fixture deduplication
  was not attempted because each fixture covers a distinct R-* rule
  set with non-overlapping helpers (path-selector for R-122,
  spawn-log timing for R-125 / INV-021).
- **Full suite regression check.** `uv run pytest tests/audit/`
  returns `1019 passed, 1 skipped` on the pre-T06.16 baseline
  (commit `5439ea1`, T06.15 fixtures already landed but T06.16's
  two new files masked via `--ignore`) and `1101 passed, 1 skipped`
  after T06.16 lands (+82 new tests, no regressions). The 1
  pre-existing skip is unrelated to this task. `make verify-sync`
  continues to flag the in-flight `auggie-bash-gate.sh` /
  `reject-workspace-writes.sh` hook-installer drift documented in
  D-0068 .. D-0080 — unrelated to T06.16.
- **Strictly read-only with respect to source-of-truth files.** The
  fixtures never write to `src/`, `.claude/`, or any agent / skill
  file; they only read the canonical files to verify the wrapper
  text has not drifted.

## 8. Provenance

- Pre-edit HEAD: `5439ea13c97021669b5ce8032b0c3132595810d7 feat(hooks): widen auggie-flag-clear matcher to mcp__auggie-mcp__; add verify-sync hook coverage and cross-consistency checks` (same baseline as T06.13 / T06.14 / T06.15 — no commits yet for the T06.16 fixtures).
- Dependency closure: T06.08 (D-0074) PASS, T06.10 (D-0076) PASS,
  T06.15 (D-0080) PASS, T06.14 (D-0079) PASS (rf-team-lead.md:417
  COMP-006-M6 byte-stability verified).
- Downstream consumers: T06.17 (D-0082, MIG-006) depends on T06.15 +
  T06.16 fixtures green before commit; T06.18 (CP-P06-END) ratifies
  T06.16 alongside the rest of Phase 6.
