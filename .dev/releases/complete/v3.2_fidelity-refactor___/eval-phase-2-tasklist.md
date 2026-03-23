# Phase 2 — Build Core Fixtures

Create the smallest real fixtures that can drive artifact-producing runs for the three core evals.

---

### T02.01 — Build C1 Anti-Instincts omission/scaffold spec fixture
**Roadmap Item IDs**: C1
**Tier**: STRICT
**Effort**: M
**Steps**:
1. **[PLANNING]** Create a compact release spec fixture designed for `superclaude roadmap run`
2. **[EXECUTION]** Seed dropped identifiers, missing explicit wiring tasks, and scaffold/mock/no-op language requiring later discharge
3. **[EXECUTION]** Ensure the fixture is still valid enough to run through the pipeline and emit roadmap artifacts
4. **[VERIFICATION]** Dry-run the roadmap command and confirm the fixture is accepted
**Acceptance Criteria**:
1. Fixture is a real roadmap-run input, not synthetic gate-only markdown
2. Fixture can produce `roadmap.md` and `anti-instinct-audit.md`
3. Seeded defect targets uncovered contracts and undischarged obligations
**Validation**:
1. `superclaude roadmap run <fixture> --dry-run` succeeds
2. Fixture specification notes the exact seeded defects
**Dependencies**: T01.03

---

### T02.02 — Build C2 wiring integration-gap runtime fixture
**Roadmap Item IDs**: C2
**Tier**: STRICT
**Effort**: L
**Steps**:
1. **[PLANNING]** Choose a real sprint/task path that exercises wiring verification
2. **[EXECUTION]** Seed one unwired optional callable, one orphan provider module, or one broken registry target in a real task fixture
3. **[EXECUTION]** Ensure the task can be executed via `superclaude sprint run`
4. **[VERIFICATION]** Confirm the fixture path and output location are stable and inspectable
**Acceptance Criteria**:
1. Fixture is executed through `superclaude sprint run`
2. Fixture targets real code-generation or runtime wiring behavior
3. Expected output includes wiring findings artifact(s)
**Validation**:
1. Dry-run or smoke-run confirms the sprint task is recognized
2. Fixture manifest identifies exactly which wiring defect is seeded
**Dependencies**: T01.03

---

### T02.03 — Build C3 TurnLedger convergence-budget fixture
**Roadmap Item IDs**: C3
**Tier**: STRICT
**Effort**: L
**Steps**:
1. **[PLANNING]** Create a roadmap fixture that requires spec-fidelity convergence and can surface budget/halt behavior
2. **[EXECUTION]** Seed bounded but insufficient progress and at least one remediation opportunity
3. **[EXECUTION]** Ensure the fixture is compatible with convergence-enabled roadmap execution
4. **[VERIFICATION]** Confirm the run can produce convergence/halt artifacts rather than only generic failure
**Acceptance Criteria**:
1. Fixture is executed through the real convergence-enabled roadmap path
2. Fixture is designed to surface halt/progress evidence from the convergence engine
3. Output expectations are tied to current implementation artifacts, not proposal-only names
**Validation**:
1. Dry-run or setup verification confirms convergence mode is enabled for the run path
2. Fixture notes explicitly identify the intended budget-pressure mechanism
**Dependencies**: T01.03
