# Phase 3.7 — Anti-Instinct Audit Verification

**Result: FAIL (expected — pipeline halted here)**

## Checks

| Check | Expected | Actual | Status |
|-------|----------|--------|--------|
| File exists | yes | yes | PASS |
| fingerprint_coverage present | yes | fingerprint_coverage: 0.73 | PASS |
| undischarged present | yes | undischarged_obligations: 1 | PASS |
| uncovered present | yes | uncovered_contracts: 4 | PASS |
| Pipeline step status | FAIL | FAIL (gate: no_undischarged_obligations) | CONFIRMED |

## Key Values

- `fingerprint_coverage`: 0.73 (33/45 fingerprints found in roadmap)
- `undischarged_obligations`: 1 (line 553: `Hardcoded` in Phase 3)
- `uncovered_contracts`: 4 (IC-001, IC-002, IC-006, IC-007 — all strategy_pattern matches)
- `total_obligations`: 1
- `total_contracts`: 8

## Failure Reason

The anti-instinct gate failed because `undischarged_obligations` is 1 (must be 0). The single undischarged obligation is a `Hardcoded` pattern detected in the Phase 3 section of the merged roadmap. This is an expected failure mode — the pipeline halted at this step and reported it correctly.

## Missing Fingerprints (12)

complexity_class, feature_id, spec_type, target_release, quality_scores, WHAT, SMTP, UUID, NULL, NULLABLE, AUTH_INVALID_CREDENTIALS, OWASP

## Artifact

- File: `.dev/test-fixtures/results/test1-tdd-prd-v2/anti-instinct-audit.md`
- Lines: 53
