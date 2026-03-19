# Phase 8 -- Shadow Calibration and Readiness

Collect shadow-mode data across 2+ release cycles, compute statistical readiness metrics (FPR, TPR, p95 latency), and produce a readiness report with an explicit recommendation for shadow-to-soft transition. This phase achieves milestone M6a: statistical evidence supports or blocks soft-mode activation.

### T08.01 -- Run Shadow Mode Across 2+ Release Cycles to Collect Findings Data

| Field | Value |
|---|---|
| Roadmap Item IDs | R-041 |
| Why | Section 7 Phase 2 criteria require shadow data from at least 2 release cycles before any enforcement mode transition can be evaluated |
| Effort | L |
| Risk | Medium |
| Risk Drivers | performance (latency data collection), compliance (section 7 Phase 2 minimum observation period) |
| Tier | EXEMPT |
| Confidence | [████████░░] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Skip verification |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0036 |

**Artifacts (Intended Paths):**
- .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0036/evidence.md

**Deliverables:**
- Shadow mode findings dataset collected across 2+ release cycles, stored as structured data (YAML reports per run) with timestamps, finding counts by type/severity, file scan counts, and execution durations

**Steps:**
1. **[PLANNING]** Confirm shadow mode is active in both roadmap pipeline (Phase 4) and sprint executor (Phase 5)
2. **[PLANNING]** Define data collection schema: per-run timestamp, finding counts by type/severity, files scanned/skipped, execution duration
3. **[EXECUTION]** Execute roadmap pipeline with shadow wiring gate across release cycle 1, collect all emitted reports
4. **[EXECUTION]** Execute sprint tasks with shadow wiring hook across release cycle 1, collect hook logs
5. **[EXECUTION]** Repeat for release cycle 2 (minimum), collecting same data points
6. **[EXECUTION]** Aggregate collected reports into a structured findings dataset
7. **[VERIFICATION]** Verify dataset spans >=2 release cycles with non-zero data points per cycle
8. **[COMPLETION]** Store aggregated dataset at intended artifact path

**Acceptance Criteria:**
- Findings dataset contains data from >=2 distinct release cycles with timestamps
- Each cycle has >=1 roadmap pipeline run and >=1 sprint session with shadow data
- Dataset includes finding counts by type (unwired/orphan/registry) and severity (critical/major/minor)
- Execution duration data is recorded for p95 latency computation in T08.02

**Validation:**
- Manual check: dataset file exists with >=2 release cycle entries and non-zero finding counts
- Evidence: linkable artifact produced at .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0036/evidence.md

**Dependencies:** Phase 4 (roadmap integration), Phase 5 (sprint integration)
**Rollback:** TBD (observational data; no code rollback needed)
**Notes:** This is an operational task spanning multiple release cycles. Do not compress observation period to meet schedule pressure per R3 mitigation.

---

### T08.02 -- Compute FPR, TPR, and p95 Latency from Shadow Data

| Field | Value |
|---|---|
| Roadmap Item IDs | R-042 |
| Why | Section 7 Phase 2 and SC-008 require statistical analysis of shadow data to determine if the system meets readiness thresholds for soft-mode activation |
| Effort | M |
| Risk | Medium |
| Risk Drivers | performance (latency analysis), compliance (SC-008 benchmark) |
| Tier | STRICT |
| Confidence | [████████░░] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0037, D-0050 |

**Artifacts (Intended Paths):**
- .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0037/evidence.md
- .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0050/evidence.md

**Deliverables:**
- Computed FPR (False Positive Rate), TPR (True Positive Rate), and p95 latency metrics from shadow dataset
- Performance benchmark evidence confirming p95 latency <5s for 50 Python files (SC-008)

**Steps:**
1. **[PLANNING]** Load shadow dataset from T08.01 and identify true positive / false positive labels (manual classification or known-fixture comparison)
2. **[PLANNING]** Define FPR = FP / (FP + TN), TPR = TP / (TP + FN) computation methodology
3. **[EXECUTION]** Classify each finding as true positive or false positive based on manual review or known-fixture ground truth
4. **[EXECUTION]** Compute FPR, TPR with confidence intervals
5. **[EXECUTION]** Compute p95 latency from execution duration data
6. **[EXECUTION]** Compare against readiness thresholds: FPR < 15%, TPR > 50%, p95 < 5s
7. **[VERIFICATION]** Validate statistical computations are reproducible from the raw dataset
8. **[COMPLETION]** Record metrics with methodology in evidence artifact

**Acceptance Criteria:**
- FPR, TPR, and p95 latency values computed with documented methodology
- p95 latency is <5s for 50 Python files (SC-008 benchmark threshold)
- Metrics are reproducible: re-running computation on same dataset produces identical results
- Results include confidence intervals or standard deviation for FPR and TPR

**Validation:**
- `uv run pytest tests/audit/ -k "benchmark" -v` exits 0 confirming <5s benchmark (SC-008)
- Evidence: linkable artifact produced at .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0037/evidence.md

**Dependencies:** T08.01 (shadow dataset)
**Rollback:** TBD (analytical task; no code rollback needed)

---

### T08.03 -- Run Retrospective Validation with cli-portify Known-Bug Fixture

| Field | Value |
|---|---|
| Roadmap Item IDs | R-043 |
| Why | SC-009 requires retrospective proof that the wiring analyzer detects a known defect (step_runner unwired callable) in the cli-portify executor |
| Effort | S |
| Risk | Medium |
| Risk Drivers | compliance (SC-009 retrospective validation) |
| Tier | STANDARD |
| Confidence | [████████░░] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0038 |

**Artifacts (Intended Paths):**
- .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0038/evidence.md

**Deliverables:**
- Retrospective validation result confirming the wiring analyzer detects the `step_runner` unwired callable in the cli-portify executor code

**Steps:**
1. **[PLANNING]** Identify the cli-portify executor file and the known `step_runner` unwired callable defect
2. **[PLANNING]** Configure wiring analyzer to scan the cli-portify executor directory
3. **[EXECUTION]** Run `run_wiring_analysis()` against the cli-portify executor codebase
4. **[EXECUTION]** Search findings for a `WiringFinding` with `finding_type="unwired"` referencing `step_runner`
5. **[VERIFICATION]** Confirm `step_runner` appears in findings with correct type and file path
6. **[COMPLETION]** Record finding details in evidence artifact with SC-009 reference

**Acceptance Criteria:**
- Wiring analysis of cli-portify executor produces a finding referencing `step_runner` as unwired callable (SC-009)
- Finding has `finding_type="unwired"` and identifies the correct file path
- Analysis completes without errors on the cli-portify codebase
- Evidence artifact records the exact finding text and file location

**Validation:**
- Manual check: run wiring analysis on cli-portify executor and confirm `step_runner` detected in output
- Evidence: linkable artifact produced at .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0038/evidence.md

**Dependencies:** Phase 2 (core engine), T08.01 (shadow mode operational)
**Rollback:** TBD (validation task; no code rollback needed)

---

### T08.04 -- Characterize Alias and Re-Export Noise Floor

| Field | Value |
|---|---|
| Roadmap Item IDs | R-044 |
| Why | R6 mitigation requires determining whether the alias/re-export FPR noise is separable from genuine wiring defect signal before soft-mode activation |
| Effort | M |
| Risk | Medium |
| Risk Drivers | compliance (R6 alias noise characterization) |
| Tier | STANDARD |
| Confidence | [████████░░] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0039 |

**Artifacts (Intended Paths):**
- .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0039/evidence.md

**Deliverables:**
- Noise floor characterization report documenting: alias/re-export false positive count, percentage of total FPR attributable to aliases, assessment of signal separability

**Steps:**
1. **[PLANNING]** Review R6 risk description: re-export aliases may cause 30-70% FPR
2. **[PLANNING]** Identify re-export patterns in the codebase: `__init__.py` re-exports, `from X import Y as Z` aliases
3. **[EXECUTION]** Classify false positives from T08.02 dataset as alias-caused vs. genuine detection failures
4. **[EXECUTION]** Compute alias-attributable FPR as percentage of total FPR
5. **[EXECUTION]** Assess separability: can alias FPs be filtered by pattern (e.g., `__init__.py` source, `as` keyword) without losing true positives?
6. **[VERIFICATION]** Validate that separability assessment is evidence-based (not speculative)
7. **[COMPLETION]** Record noise floor characterization in evidence artifact with R6 reference

**Acceptance Criteria:**
- Report quantifies alias/re-export false positives as a percentage of total false positives
- Separability assessment is documented with evidence: either "separable by pattern X" or "not separable, blocking soft activation"
- If not separable, report recommends extending shadow period or blocking Phase 9 activation per R6 mitigation
- Analysis covers both `__init__.py` re-exports and `import X as Y` aliases

**Validation:**
- Manual check: noise floor report exists with quantified alias FPR and separability assessment
- Evidence: linkable artifact produced at .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0039/evidence.md

**Dependencies:** T08.02 (FPR data with classified false positives)
**Rollback:** TBD (analytical task; no code rollback needed)

---

### Checkpoint: Phase 8 / Tasks T08.01-T08.04

**Purpose:** Verify shadow data collection and initial statistical analysis before computing readiness thresholds.
**Checkpoint Report Path:** .dev/releases/current/v3.0_unified-audit-gating/checkpoints/CP-P08-T01-T04.md
**Verification:**
- Shadow dataset spans >=2 release cycles with non-zero findings per cycle
- FPR, TPR, and p95 latency computed with documented methodology
- Retrospective validation confirms step_runner detection (SC-009)
**Exit Criteria:**
- Statistical metrics are reproducible from raw dataset
- Alias noise floor is characterized with separability assessment
- p95 latency is <5s for 50 Python files (SC-008)

---

### T08.05 -- Validate measured_FPR + 2sigma < 15% Threshold

| Field | Value |
|---|---|
| Roadmap Item IDs | R-045 |
| Why | Section 7 Phase 2 FPR calibration gate requires statistical proof that measured FPR plus 2 standard deviations is below 15% before soft-mode activation |
| Effort | S |
| Risk | Medium |
| Risk Drivers | compliance (section 7 Phase 2 FPR calibration) |
| Tier | STRICT |
| Confidence | [████████░░] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0040 |

**Artifacts (Intended Paths):**
- .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0040/evidence.md

**Deliverables:**
- FPR threshold validation result: `measured_FPR + 2*sigma < 15%` evaluated as PASS or FAIL with supporting computation

**Steps:**
1. **[PLANNING]** Load FPR and standard deviation values from T08.02 metrics
2. **[PLANNING]** Confirm threshold formula: `measured_FPR + 2 * sigma_FPR < 0.15`
3. **[EXECUTION]** Compute `measured_FPR + 2 * sigma_FPR` and compare against 15% threshold
4. **[EXECUTION]** Record PASS or FAIL result with exact values
5. **[VERIFICATION]** Cross-check computation against raw data to prevent arithmetic errors
6. **[COMPLETION]** Record result in evidence artifact with section 7 Phase 2 reference

**Acceptance Criteria:**
- Threshold computation is documented with exact FPR value, sigma value, and result of `FPR + 2*sigma < 0.15`
- Result is unambiguous: PASS (proceed to soft mode) or FAIL (extend shadow period)
- Computation is reproducible from T08.02 metrics
- If FAIL, recommendation includes specific remediation (extend shadow, improve analyzer, defer to v2.1)

**Validation:**
- Manual check: threshold computation exists with PASS/FAIL result and supporting values
- Evidence: linkable artifact produced at .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0040/evidence.md

**Dependencies:** T08.02 (FPR and sigma values)
**Rollback:** TBD (gate decision; no code rollback needed)

---

### T08.06 -- Produce Readiness Report with Explicit Shadow-to-Soft Recommendation

| Field | Value |
|---|---|
| Roadmap Item IDs | R-046 |
| Why | The readiness report aggregates all Phase 8 evidence into a single decision document with an explicit recommendation for shadow-to-soft transition or extended shadow |
| Effort | S |
| Risk | Medium |
| Risk Drivers | compliance (readiness decision record) |
| Tier | STANDARD |
| Confidence | [████████░░] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0041 |

**Artifacts (Intended Paths):**
- .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0041/spec.md

**Deliverables:**
- Readiness report documenting: FPR/TPR/p95 metrics, alias noise assessment, retrospective validation result, threshold evaluation, and explicit recommendation (proceed to soft mode OR extend shadow with rationale)

**Steps:**
1. **[PLANNING]** Collect all Phase 8 evidence: T08.02 metrics, T08.03 retrospective, T08.04 noise floor, T08.05 threshold
2. **[PLANNING]** Review exit criteria: FPR < 15%, TPR > 50%, p95 < 5s, alias noise separable, shadow data from >=2 releases
3. **[EXECUTION]** Compile readiness report with sections for each exit criterion and its status (MET/NOT MET)
4. **[EXECUTION]** Formulate explicit recommendation based on criteria evaluation: "Proceed to soft mode" or "Extend shadow period" with specific rationale
5. **[EXECUTION]** Reference all supporting evidence artifacts by path
6. **[VERIFICATION]** Verify all exit criteria are addressed and recommendation is consistent with evidence
7. **[COMPLETION]** Store readiness report at intended artifact path

**Acceptance Criteria:**
- Readiness report exists at `.dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0041/spec.md`
- Report addresses all 4 exit criteria (FPR, TPR, p95, alias separability) with MET/NOT MET status
- Report contains explicit recommendation (proceed/extend) with rationale referencing evidence
- All evidence artifacts referenced in report exist at their stated paths

**Validation:**
- Manual check: readiness report contains all exit criteria, evidence references, and explicit recommendation
- Evidence: linkable artifact produced at .dev/releases/current/v3.0_unified-audit-gating/artifacts/D-0041/spec.md

**Dependencies:** T08.02, T08.03, T08.04, T08.05
**Rollback:** TBD (decision document; no code rollback needed)

---

### Checkpoint: End of Phase 8

**Purpose:** Validate milestone M6a: statistical evidence supports or blocks soft-mode activation, documented in readiness report.
**Checkpoint Report Path:** .dev/releases/current/v3.0_unified-audit-gating/checkpoints/CP-P08-END.md
**Verification:**
- FPR < 15%, TPR > 50%, p95 < 5s thresholds evaluated
- Alias noise separable from signal (or blocking recommendation documented)
- Shadow data from >=2 release cycles confirmed
**Exit Criteria:**
- Readiness report produced with explicit recommendation and all evidence referenced
- `measured_FPR + 2*sigma < 15%` threshold evaluated as PASS or FAIL
- Readiness report reviewed and signed off before Phase 9 activation
