# QA Report — Phase 4 Qualitative Edge-Case Completeness

**Lens:** edge-case-completeness | **Phase:** synthesis-gate-equivalent / task-integrity | **Fix authorization:** false | **Date:** 2026-07-02

Note: The edge-case agent returned this matrix directly; the orchestrator persisted it at the required path.

## VERDICT: PASS

All 7 assigned test files (81 tests, all passing) plus the two source requirement docs were reviewed, and each mandated edge case is exercised by at least one test with a real assertion. The "30-day timer" anti-pattern is confirmed absent (staleness is mismatch-based).

## Edge-case → test-name matrix

| # | Edge case | Covering test(s) | File |
|---|---|---|---|
| 1 | Empty-payload negative control | `test_negative_controls_empty_and_non_augment_do_not_classify_reviewed` (empty == STATE_POLLING) | test_contract_setup_validation.py |
| 2 | Non-Augment negative control | same test (non_augment == STATE_POLLING); `test_copied_human_text_cannot_validate_augment_identity`; `test_human_prose_does_not_produce_observed_augment_identity` | validation.py / evidence.py tests |
| 3 | Repo mismatch blocks lock | `test_repo_mismatch_blocks_lock`; `test_repo_mismatch_blocks_candidate_readiness` | validation.py / evidence.py tests |
| 4 | Evidence hash absent/mismatch blocks lock | `test_missing_evidence_hash_blocks_lock` (sha256="" → evidence_hash_present fails) | test_contract_setup_validation.py |
| 5 | Cross-PR evidence shape-only | `test_cross_pr_evidence_flagged_shape_only`; `test_cross_pr_shape_only_blocks_readiness`; `test_default_evidence_is_not_cross_pr_shape_only`; writer cross-PR refusal test | evidence.py / writer.py tests |
| 6 | Stale evidence (mismatch-based) | `test_repo_mismatch_blocks_candidate_readiness`; `test_matching_repo_passes_freshness`; `test_repo_mismatch_blocks_lock` | evidence.py / validation.py tests |
| 7 | Multi-Augment identity requires explicit selection | `test_multiple_augment_identity_candidates_require_explicit_selection` | test_contract_setup_questions.py |
| 8 | `decline_validation: not_exercised` when no sample | `test_missing_decline_evidence_records_not_exercised` (questions + validation suites) | questions.py / validation.py tests |

## Findings

No missing edge cases. Informational only:
- F-1 (INFO): staleness is correctly mismatch-based (`repo_match`, `evidence_hash_present`, `cross_pr_shape_only`); no nonexistent 30-day timer is asserted. Design §8 mentions a non-blocking 30-day age warning, but blocking freshness is mismatch-only.
- F-2 (INFO): item 4 tests hash-absence (`bool(evidence.sha256)` presence gate) — the honest implemented behavior; no separate wrong-but-present-hash path exists.
- F-3 (INFO): negative controls double-covered (report CheckResults + raw `classify()` seam).
- F-4 (INFO): decline test asserts `not_exercised` AND non-blocking `passed is True`.

Confidence: 8/8 edge cases verified = 100%. No files modified.
