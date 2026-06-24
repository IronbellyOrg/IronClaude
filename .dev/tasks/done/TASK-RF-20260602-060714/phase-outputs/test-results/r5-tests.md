# R5 Test Surfaces — Results (Step 4.14)

**Captured:** 2026-06-02 07:20
**Raw output:** `r5-tests.txt`
**Overall:** ✅ ALL GREEN — no failures.

## Per-surface results

| Surface | Result |
|---|---|
| `tests/roadmap/test_structural_checkers.py` | **61 passed, 1 skipped** (pre-existing `test_security_missing_is_ambiguous` skip) |
| `tests/roadmap/test_spec_roadmap_id_containment.py` | **11 passed** (schema-stable + round-trip now assert 9-key set incl. `md_ids`) |
| `tests/roadmap/test_gates_data.py` | **227 passed** (MERGE_GATE 8-semantic-check composition guard intact) |
| `tests/roadmap/test_pipeline_envelope.py` | **9 passed** (envelope `md_ids` round-trip via `to_dict`/`envelope_from_dict` works; `test_envelope_round_trip` green) |

## 3 ported PR #111 oracle tests (all PASS)

| Test | Result | Asserts |
|---|---|---|
| `test_phantom_id_honors_explicit_non_references_for_milestone_d_ids` | ✅ PASS | M{n}-D{nn} multi-milestone + Explicit-non-references allowlist → 0 signatures findings (canonical v1-MVP bug shape) |
| `test_phantom_id_backward_compatible_without_explicit_non_references` | ✅ PASS | No annotation → 0 HIGH phantom + exactly 3 MEDIUM drift (D01↔D1, D03↔D3, D05↔D5) — legacy behavior preserved |
| `test_phantom_id_bare_d_still_resolves_when_spec_uses_bare_d` | ✅ PASS | Bare-D spec D7/D8 vs roadmap D7/D9 → exactly 1 HIGH phantom (D9), 0 drift — no bare-D regression |

None skipped (scope = MD-FAMILY-PLUS-ALLOWLIST, so test 1 runs with the ported allowlist; no `@pytest.mark.skip` needed).

## Notes
- The new disk-backed recurrence fixture (`fixtures/recurrence/id_containment/milestone_id_case.{md,expected.json}`) was created in Step 4.13; the existing `test_phantom_id_rejected[recurrence_case0]` (parametrized on `spec_roadmap_drift_case`) still passes, and the new fixture is available for a future parametrized case per the corpus README.
- No source/test edits required during this step — all surfaces passed on first run after the 4.1-4.13 edits.
