# Phase 5.5 -- Spec+PRD Anti-Instinct Audit

**Date**: 2026-04-02
**Source**: `.dev/test-fixtures/results/test2-spec-prd/anti-instinct-audit.md`

## Extracted Metrics

| Metric | Value |
|--------|-------|
| fingerprint_coverage | 0.67 |
| undischarged_obligations | 0 |
| uncovered_contracts | 3 |
| total_obligations | 1 |
| total_contracts | 6 |
| fingerprint_total | 18 |
| fingerprint_found | 12 |

## Details

### Obligation Scanner
- 1 obligation detected, 1 discharged, 0 undischarged
- **Status**: PASS (no gate-blocking undischarged obligations)

### Integration Contract Coverage
- 6 contracts total, 3 covered, 3 uncovered
- Uncovered contracts are all `middleware_chain` related:
  - IC-004: `src/middleware/auth-middleware.ts` Bearer token extraction
  - IC-005: auth-middleware.ts (line 165)
  - IC-006: auth-middleware.ts dependency chain (line 212)
- **Status**: FAIL -- uncovered_contracts must be 0 for gate pass

### Fingerprint Coverage
- 18 total fingerprints, 12 found in roadmap (66.7%)
- Missing fingerprints: AUTH_SERVICE_ENABLED, JIRA, RBAC, PASETO, CSRF, REST
- **Note**: Several missing fingerprints (JIRA, RBAC, PASETO) are out-of-scope items. CSRF and REST are implicit. AUTH_SERVICE_ENABLED is a config detail.

## Pipeline Impact

Anti-instinct step returned **FAIL** due to `uncovered_contracts=3`. This correctly halted the pipeline at step 8/13, preventing downstream steps (spec-fidelity, deviation-analysis, remediate, certify) from executing.

Gate failure reason: "Semantic check 'integration_contracts_covered' failed: uncovered_contracts must be 0; integration contracts lack explicit wiring tasks in roadmap"

## Verdict

**PASS (as expected behavior)** -- Anti-instinct correctly detected uncovered integration contracts and halted the pipeline. The gate is functioning as designed.
