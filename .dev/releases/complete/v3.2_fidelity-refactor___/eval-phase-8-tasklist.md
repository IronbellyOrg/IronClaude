# Phase 8 — Finalize Acceptance Thresholds and Publish Verdict Bundle

Freeze what counts as convincing proof and produce the final evidence package.

---

### T08.01 — Freeze acceptance thresholds
**Roadmap Item IDs**: C1,C2,C3,X1,X2,A1
**Tier**: STANDARD
**Effort**: M
**Steps**:
1. **[PLANNING]** Consolidate all verifier rules and ambiguity decisions
2. **[EXECUTION]** Freeze per-release pass/fail thresholds and composite acceptance rules
3. **[VERIFICATION]** Ensure the thresholds match actual artifact behavior seen in pilot runs
**Acceptance Criteria**:
1. Threshold document exists under the eval root
2. Thresholds distinguish core proof from supporting evidence
3. No threshold depends on mock-only or log-only evidence
**Validation**:
1. Threshold doc cites corresponding run bundles
**Dependencies**: T07.01, T07.02, T07.03

---

### T08.02 — Publish final real-eval verdict bundle
**Roadmap Item IDs**: C1,C2,C3,X1,X2,A1
**Tier**: STANDARD
**Effort**: M
**Steps**:
1. **[EXECUTION]** Assemble final artifact manifest across all completed eval runs
2. **[EXECUTION]** Write a verdict summary classifying each eval as PASS, FAIL, AMBIGUOUS, or BLIND SPOT
3. **[EXECUTION]** Include exact artifact paths and a no-mock compliance statement
4. **[VERIFICATION]** Confirm the bundle is third-party reviewable without reading source code
**Acceptance Criteria**:
1. Final verdict bundle exists in the eval root
2. Each verdict cites exact artifact paths
3. Bundle explicitly states that proof came from real CLI pipelines with no mocks
**Validation**:
1. A reviewer can inspect the bundle and understand what each release claim did or did not prove
**Dependencies**: T08.01
