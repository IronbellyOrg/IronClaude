# Phase 1 — Real-Pipeline Eval Foundations

Establish fixture locations, execution roots, and artifact contracts before building seeded inputs.

---

### T01.01 — Define eval workspace layout
**Roadmap Item IDs**: C1,C2,C3,X1,X2,A1
**Tier**: STANDARD
**Effort**: S
**Steps**:
1. **[PLANNING]** Choose a single eval root under `.dev/releases/complete/v3.2_fidelity-refactor___/evals/`
2. **[EXECUTION]** Define subdirectories for `fixtures/`, `runs/`, `artifacts/`, and `verification/`
3. **[EXECUTION]** Define per-eval IDs and output directories for C1, C2, C3, X1, X2, A1
4. **[VERIFICATION]** Confirm every planned eval has a unique artifact destination
**Acceptance Criteria**:
1. A single eval root exists in the release directory
2. Each eval has a deterministic run/output location
3. Output locations are in-repo and inspectable
**Validation**:
1. Directory manifest is documented in a markdown file under the eval root
2. No output path points to transient-only logs
**Dependencies**: None

---

### T01.02 — Freeze real-artifact contracts per release
**Roadmap Item IDs**: C1,C2,C3
**Tier**: STRICT
**Effort**: M
**Steps**:
1. **[PLANNING]** Record the minimum acceptable artifacts for v3.1, v3.2, and v3.05
2. **[EXECUTION]** Define exact pass/fail evidence required for each artifact
3. **[EXECUTION]** Mark warning-only outputs as supporting evidence only unless persisted and deterministic
4. **[VERIFICATION]** Review contracts against the proposal and current pipeline behavior
**Acceptance Criteria**:
1. v3.1 contract requires `roadmap.md` and `anti-instinct-audit.md`
2. v3.2 contract requires wiring output plus task/sprint outcome artifact
3. v3.05 contract requires convergence result with halt/progress evidence
4. Each contract rejects log-only proof
**Validation**:
1. Artifact contract file exists under the eval root
2. Contract language explicitly says no mocks and no unit-test-only proof
**Dependencies**: T01.01

---

### T01.03 — Define canonical no-mock CLI invocations
**Roadmap Item IDs**: C1,C2,C3
**Tier**: STRICT
**Effort**: M
**Steps**:
1. **[PLANNING]** Identify the real CLI entrypoint for each eval type
2. **[EXECUTION]** Define canonical `superclaude roadmap run` command for roadmap-side evals
3. **[EXECUTION]** Define canonical `superclaude sprint run` command for runtime/wiring evals
4. **[EXECUTION]** Define convergence-enabled roadmap invocation for v3.05 evals
5. **[VERIFICATION]** Ensure commands exercise the affected release surfaces rather than isolated helpers
**Acceptance Criteria**:
1. Every core eval has a real CLI command attached to it
2. No command uses mocked harnesses or unit-test substitutes
3. Commands are documented in executable markdown blocks
**Validation**:
1. Command manifest exists under the eval root
2. Each command references a real fixture path and real output dir
**Dependencies**: T01.02
