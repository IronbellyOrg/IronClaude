# D-0038 -- T05.02: Stale Deviation Artifacts Trigger Re-Run

## Summary

Stale `spec-deviations.md` (roadmap_hash mismatch) triggers annotate-deviations re-run. Downstream gates reset on stale detection. Stale artifact is never passed to downstream steps.

## Test Evidence

**Test file:** `tests/sprint/test_executor.py::TestFreshness`

**Validation command:** `uv run pytest tests/sprint/test_executor.py -v -k "stale or freshness"`

**Result:** 11 passed, 0 failed

### Tests executed:

| Test | Assertion | Result |
|------|-----------|--------|
| `test_freshness_matching_hash_returns_true` | Matching hash -> True (fresh) | PASS |
| `test_freshness_mismatched_hash_returns_false` | Mismatched hash -> False (stale) | PASS |
| `test_freshness_missing_file_returns_false` | Missing file -> False | PASS |
| `test_freshness_missing_field_returns_false` | Missing roadmap_hash field -> False | PASS |
| `test_freshness_read_error_returns_false` | Read error -> False | PASS |
| `test_freshness_empty_file_returns_false` | Empty file -> False | PASS |
| `test_freshness_corrupt_frontmatter_returns_false` | Corrupt frontmatter -> False | PASS |
| `test_freshness_missing_roadmap_md_returns_false` | Missing roadmap.md -> False | PASS |
| `test_freshness_none_hash_in_field_returns_false` | null hash in field -> False | PASS |
| `test_freshness_mismatch_resets_gate_pass_state` | Hash mismatch resets downstream gate-pass states | PASS |
| `test_freshness_match_does_not_modify_gate_pass_state` | Matching hash does not modify gate state | PASS |

## Implementation

- **Function**: `_check_annotate_deviations_freshness()` in `executor.py`
- **Mechanism**: SHA-256 hash comparison between current roadmap.md content and stored `roadmap_hash` in spec-deviations.md frontmatter
- **On mismatch**: Returns False AND resets downstream gate pass states (spec-fidelity, deviation-analysis)
- **Fail-closed**: Any error condition (missing file, corrupt frontmatter, missing field) returns False

## Acceptance Criteria Verification

- [x] Stale spec-deviations.md (hash mismatch) triggers annotate-deviations re-run (function returns False)
- [x] Downstream gates (spec-fidelity, deviation-analysis) reset on stale detection
- [x] Stale artifact is never passed to downstream steps (function returns False before proceeding)
- [x] `uv run pytest tests/sprint/test_executor.py -v -k "stale or freshness"` exits 0
