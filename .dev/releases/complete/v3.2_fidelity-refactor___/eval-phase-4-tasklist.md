# Phase 4 — Run the Three Core Evals

Execute the core no-mock evals in sequence and collect real artifacts.

---

### T04.01 — Run C1 omission recovery eval
**Roadmap Item IDs**: C1
**Tier**: STRICT
**Effort**: M
**Steps**:
1. **[EXECUTION]** Run the canonical roadmap command against the C1 fixture
2. **[EXECUTION]** Capture all output artifacts in the deterministic run directory
3. **[VERIFICATION]** Apply the C1 verifier to the produced artifacts
4. **[COMPLETION]** Record verdict and artifact manifest
**Acceptance Criteria**:
1. Real roadmap pipeline executes
2. `roadmap.md` and `anti-instinct-audit.md` are produced
3. Seeded omission/scaffold defects are reflected in persisted artifacts
**Validation**:
1. Verifier returns pass/fail/ambiguous with cited artifact paths
**Dependencies**: T03.01

---

### T04.02 — Run C2 wiring integration-gap eval
**Roadmap Item IDs**: C2
**Tier**: STRICT
**Effort**: M
**Steps**:
1. **[EXECUTION]** Run the canonical sprint command against the C2 fixture
2. **[EXECUTION]** Capture wiring artifacts and run-status outputs
3. **[VERIFICATION]** Apply the C2 verifier to the produced artifacts
4. **[COMPLETION]** Record verdict and artifact manifest
**Acceptance Criteria**:
1. Real sprint pipeline executes
2. Wiring artifact is produced and inspectable
3. Seeded integration defect is surfaced in persisted outputs
**Validation**:
1. Verifier cites the concrete files proving the defect was caught
**Dependencies**: T03.02

---

### T04.03 — Run C3 TurnLedger convergence-economics eval
**Roadmap Item IDs**: C3
**Tier**: STRICT
**Effort**: L
**Steps**:
1. **[EXECUTION]** Run the canonical convergence-enabled roadmap command against the C3 fixture
2. **[EXECUTION]** Capture convergence/halt/progress outputs in the deterministic run directory
3. **[VERIFICATION]** Apply the C3 verifier to the produced artifacts
4. **[COMPLETION]** Record verdict and artifact manifest
**Acceptance Criteria**:
1. Real convergence-enabled roadmap path executes
2. Persisted artifacts show convergence/halt/progress evidence
3. Result proves or disproves the economic-control claim without mocks
**Validation**:
1. Verifier output cites exact convergence artifacts and verdict basis
**Dependencies**: T03.03
