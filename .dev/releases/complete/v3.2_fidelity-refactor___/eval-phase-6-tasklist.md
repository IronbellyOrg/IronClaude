# Phase 6 — Adversarial Stretch Eval

Implement the strongest skeptic-proof scenario only after the core and composite evals are stable.

---

### T06.01 — Build A1 superficially-complete-but-disconnected fixture
**Roadmap Item IDs**: A1
**Tier**: STRICT
**Effort**: XL
**Steps**:
1. **[PLANNING]** Choose the smallest adversarial blend that still exercises v3.1, v3.2, and v3.05
2. **[EXECUTION]** Combine identifier laundering, vague integration coverage, inert runtime wiring, and convergence-pressure elements
3. **[VERIFICATION]** Ensure the scenario still runs through real pipelines and emits real artifacts
**Acceptance Criteria**:
1. Adversarial fixture remains executable through real CLI paths
2. Scenario does not depend on fabricated or hand-written fake artifacts
**Validation**:
1. Fixture design document lists each stealth mechanism and its expected artifact signature
**Dependencies**: T04.01, T04.02, T04.03

---

### T06.02 — Run A1 adversarial stretch eval
**Roadmap Item IDs**: A1
**Tier**: STRICT
**Effort**: XL
**Steps**:
1. **[EXECUTION]** Run the required roadmap/sprint/convergence paths for A1
2. **[EXECUTION]** Collect all emitted artifacts into a single run bundle
3. **[VERIFICATION]** Determine whether the scenario is correctly rejected, partially detected, or exposes a remaining blind spot
4. **[COMPLETION]** Record a skeptic-facing verdict summary
**Acceptance Criteria**:
1. Real artifact bundle exists for the full adversarial scenario
2. Outcome is classified as caught, ambiguous, or blind spot with explicit evidence
3. No part of the proof relies on mocked execution
**Validation**:
1. Final verdict cites exact artifact files and unresolved ambiguity if present
**Dependencies**: T06.01
