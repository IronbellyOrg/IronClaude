# Phase 3 — Implement Verifiers and Evidence Guards

Create verifier logic that accepts only real, persisted, third-party-checkable outputs.

---

### T03.01 — Implement C1 artifact verifier
**Roadmap Item IDs**: C1
**Tier**: STANDARD
**Effort**: M
**Steps**:
1. **[PLANNING]** Define the exact evidence fields required from `anti-instinct-audit.md`
2. **[EXECUTION]** Implement a verifier that checks for uncovered contracts, obligations, and roadmap artifact presence
3. **[EXECUTION]** Reject results that rely on explanation without persisted evidence
4. **[VERIFICATION]** Test verifier against a known-good sample artifact shape
**Acceptance Criteria**:
1. Verifier checks persisted files, not logs alone
2. Verifier can distinguish pass, fail, and ambiguous results
3. Verifier rejects missing artifact sets
**Validation**:
1. Verifier documentation explains what makes a result third-party verifiable
**Dependencies**: T02.01

---

### T03.02 — Implement C2 artifact verifier
**Roadmap Item IDs**: C2
**Tier**: STANDARD
**Effort**: M
**Steps**:
1. **[PLANNING]** Define the exact evidence fields required from wiring output
2. **[EXECUTION]** Implement a verifier that checks for non-zero defect evidence and associated run output
3. **[EXECUTION]** Add handling for suspicious zero-findings outcomes
4. **[VERIFICATION]** Ensure verifier rejects results that do not include a real run artifact
**Acceptance Criteria**:
1. Verifier requires wiring artifact plus run-status artifact
2. Zero-findings cases are not auto-accepted without sanity evidence
3. Verifier identifies ambiguous outcomes separately
**Validation**:
1. Verifier contract is written under the eval root
**Dependencies**: T02.02

---

### T03.03 — Implement C3 artifact verifier
**Roadmap Item IDs**: C3
**Tier**: STANDARD
**Effort**: M
**Steps**:
1. **[PLANNING]** Define the exact evidence fields required from convergence outputs
2. **[EXECUTION]** Implement a verifier that checks halt reason, progress evidence, and run count status
3. **[EXECUTION]** Reject outputs that only imply budget behavior without persisted evidence
4. **[VERIFICATION]** Ensure verifier matches current convergence implementation surfaces
**Acceptance Criteria**:
1. Verifier requires persisted convergence evidence
2. Generic spec-fidelity failure without convergence evidence does not count
3. Halt/progress interpretation rules are documented
**Validation**:
1. Verifier spec references current convergence engine behavior
**Dependencies**: T02.03
