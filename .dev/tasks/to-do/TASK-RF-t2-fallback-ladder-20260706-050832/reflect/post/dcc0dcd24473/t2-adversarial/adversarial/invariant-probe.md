# Invariant Probe Results

## Round 2.5 — Fault-Finder Analysis

Independent fault-finder probing the *emerging consensus* of the two reviews (and the executor's Done judgment they audit) against the 6-category checklist. Findings are grounded in the task artifact, `phase-outputs/`, `qa/`, and `return-contract.yaml`.

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-001 | sufficiency_challenge | "The green full suite (2554 passed) is *sufficient* to confirm the 6.G10 fixes were correctly applied." | **UNADDRESSED** | **HIGH** | 6.G9 FAIL findings include IMPORTANT-2 (stale `_resolve_run_transport_factory` docstring) and MINORs (orphan `pass_with_t2_fallback.yaml`, task-file import-allowlist gap) that are **not exercised by any test** (`TASK…md:580`). pytest greenness is necessary, not sufficient. This is precisely the gap 6.G11's spawned re-verification exists to close — and it was replaced by inline pytest (`TASK…md:582`). Downstream gate for the "fix greened the gate" claim (6.G11 spawn) was **not traversed**. |
| INV-002 | guard_conditions | "The exit-11 carve-out guard admits `reason: null-convergence`." | **UNADDRESSED (interpretation-widened)** | **MEDIUM** | Carve-out guard names *"degraded (single-reviewer-fallback / single-vendor)"* (`TASK…md:499`). Actual `reflect_post.reason: null-convergence` (frontmatter L37). The guard's *rationale* clause ("environmental, not a content failure") is satisfied — but the literal predicate is not. Guard was passed by intent, not by label match. |
| INV-003 | state_variables | "`reflect_pre` frontmatter reflects post-execution reality." | **ADDRESSED (honestly disclosed)** | LOW | Executor explicitly records `reflect_pre` as "a historical PRE-reflect record, not reconciled by execution" (Phase 5 log). State staleness is disclosed, not hidden — but `coverage_pct: 1.0 / tcs: 0` (frontmatter L23,L25) remains an odd pairing V2-H3 fairly flags. |
| INV-004 | collection_boundaries | "The enumerated test surface (7) equals the delivered surface (8)." | **ADDRESSED (documented over-delivery)** | LOW | All 8 files exist on disk (`ls tests/cli/reflect/`); Task Summary L515/L527 and Phase-6 log L593 document `test_ensemble_fallback_engage.py` + `test_fallback_config.py` as authorized over-delivery. Internal doc inconsistency ("§9-enumerated 7" at L451/L493 vs "6" at L527/L593) is a MINOR blemish, not a masking risk. |
| INV-005 | count_divergence | "The `1 xpassed` reflects a change-set regression." | **ADDRESSED** | LOW | `final-fulltest-summary.md:23`: "The 1 xpassed and 28 skipped are pre-existing suite conditions unrelated to this change set." Additive-only 0-diff on `contract.py` corroborates. Residual: the specific xpassed test name is not recorded (rigor gap, not a defect). |
| INV-006 | interaction_effects | "Real T1-proxy dispatch is inert without independent operator attestation." | **ADDRESSED (operator-attested-only)** | MEDIUM | `_T1_PROXY_BINDING` real-dispatch enablement rests solely on the executor's own log of an interactive `AskUserQuestion` sign-off; not externally attested in-artifact (V2-H3, V1-#4). The HALT itself functioned; the *authenticity* of the sign-off is unverifiable from the artifact alone. |

## Summary

- **Total findings**: 6
- **ADDRESSED**: 4 (INV-003, INV-004, INV-005, INV-006 — with caveats)
- **UNADDRESSED**: 2
  - HIGH: 1 (INV-001 — sufficiency of pytest for non-test-covered fixes ≡ V2-H2)
  - MEDIUM: 1 (INV-002 — carve-out label vs rationale ≡ V2-H1)
  - LOW: 0

**Convergence gate impact:** INV-001 is HIGH + UNADDRESSED → **blocks a clean "converged PASS"** and confirms the merged artifact must carry the 6.G11 re-verification follow-up as a **mandatory** disposition, not an optional note. This independently corroborates V2's H2 and demotes the shared assumption A-001 (green-suite-is-sufficient) that *both* reviews leaned on.
