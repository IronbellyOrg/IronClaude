# Phase 5 — Build and Run Composite Evals

Once core single-release proof surfaces are stable, build cross-release scenarios.

---

### T05.01 — Build X1 mocked-steps-to-unwired-runtime composite fixture
**Roadmap Item IDs**: X1
**Tier**: STRICT
**Effort**: L
**Steps**:
1. **[PLANNING]** Design a scenario where roadmap scaffolding debt can propagate into runtime wiring debt
2. **[EXECUTION]** Build the composite fixture using real roadmap and sprint entrypoints
3. **[VERIFICATION]** Confirm both release proof surfaces can be exercised in one scenario
**Acceptance Criteria**:
1. Composite uses real pipeline stages, not stitched-together fake artifacts
2. v3.1 and v3.2 proof surfaces are both reachable
**Validation**:
1. Composite fixture document maps each seeded defect to both expected artifact families
**Dependencies**: T04.01, T04.02

---

### T05.02 — Run X1 composite eval
**Roadmap Item IDs**: X1
**Tier**: STRICT
**Effort**: L
**Steps**:
1. **[EXECUTION]** Run roadmap phase of X1 and capture artifacts
2. **[EXECUTION]** Run sprint/runtime phase of X1 and capture artifacts
3. **[VERIFICATION]** Confirm the same seeded defect is traceable across both artifact sets
4. **[COMPLETION]** Record verdict and propagation mapping
**Acceptance Criteria**:
1. Both real pipelines execute
2. Cross-artifact mapping is inspectable by a third party
3. Proof does not rely on verbal interpretation alone
**Validation**:
1. Composite verdict cites exact artifact paths for both halves of the scenario
**Dependencies**: T05.01

---

### T05.03 — Build and run X2 omission-to-drift-to-wiring composite
**Roadmap Item IDs**: X2
**Tier**: STRICT
**Effort**: XL
**Steps**:
1. **[PLANNING]** Design a scenario starting at spec/extraction loss and ending in wiring failure
2. **[EXECUTION]** Build the real fixture chain
3. **[EXECUTION]** Run roadmap and runtime paths in sequence
4. **[VERIFICATION]** Confirm extraction/anti-instinct/wiring artifacts all participate in the same proof chain
5. **[COMPLETION]** Record verdict and traceability matrix
**Acceptance Criteria**:
1. Composite produces at least one artifact from each targeted release proof surface
2. Same seeded defect is traceable across the chain
3. Result is third-party verifiable without code inspection
**Validation**:
1. Traceability matrix exists in the run directory
**Dependencies**: T04.01, T04.02
