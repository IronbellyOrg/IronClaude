# D-0046: Open Question Resolutions

## OQ-1: FR-4.1 Rubric Threshold Calibration

**Question**: What is the appropriate threshold for the VERDICT_MARGIN_THRESHOLD in the semantic debate rubric?

**Decision**: `VERDICT_MARGIN_THRESHOLD = 0.15` (15%)

**Rationale**: The 0.15 margin was selected to balance decisiveness with accuracy:
- A margin > 0.15 in favor of the prosecutor confirms HIGH (clear evidence of deviation)
- A margin > 0.15 in favor of the defender downgrades to MEDIUM or LOW
- Ties (within ±0.15) default to CONFIRM_HIGH as a conservative policy
- Calibrated against the 4-dimension rubric weights: evidence_quality (0.35), impact_specificity (0.25), logical_coherence (0.25), concession_handling (0.15)
- This threshold ensures that minor scoring differences don't flip verdicts

**Affected Requirement**: FR-4.1

---

## OQ-3: ParseWarning Handling

**Question**: Should parse warnings block the pipeline or be logged and continued?

**Decision**: Log-and-continue

**Rationale**: Parse warnings from `spec_parser.py` indicate potentially incomplete but usable parsing results. Blocking on warnings would make the pipeline fragile against minor spec formatting variations. The structural checkers already handle missing data gracefully (returning no findings for dimensions where data is unavailable). Warnings are logged at WARNING level for visibility.

**Affected Requirement**: FR-1 (structural checkers)

---

## OQ-4: TurnLedger Constant Calibration

**Question**: What should the CHECKER_COST, REMEDIATION_COST, and related budget constants be?

**Decision**:
- `CHECKER_COST = 10` — one checker run (5 structural + semantic layer)
- `REMEDIATION_COST = 8` — one remediation cycle (agent spawn + apply + verify)
- `REGRESSION_VALIDATION_COST = 15` — parallel 3-agent validation + debate
- `CONVERGENCE_PASS_CREDIT = 5` — credit on successful convergence
- `MIN_CONVERGENCE_BUDGET = 28` — minimum: 1 checker + 1 remediation + 1 checker
- `STD_CONVERGENCE_BUDGET = 46` — standard: 3 full checker/remediation cycles
- `MAX_CONVERGENCE_BUDGET = 61` — maximum: 3 cycles + regression validation

**Rationale**: Budget units are abstract "turn equivalents" sized to:
1. Ensure at least one full check-remediate-verify cycle at MIN budget
2. Support the full 3-run convergence loop at STD budget
3. Allow regression validation at MAX budget
4. CHECKER_COST > REMEDIATION_COST because checkers are the accuracy-critical step
5. REGRESSION_VALIDATION_COST is highest because it spawns 3 parallel agents + debate

**Affected Requirement**: FR-7 (convergence engine)

---

## OQ-5: Agent Failure Criteria for FR-8 Regression Validation

**Question**: What constitutes agent failure during regression validation?

**Decision**: An agent fails when:
1. Process exit code is non-zero (timeout, crash, or error)
2. Agent output fails to parse as valid checker findings
3. Agent exceeds the timeout window (_AGENT_TIMEOUT_SECONDS = 300)

Regression validation uses 3 parallel agents with majority voting. If 2 of 3 agents agree on a finding's status, that status is accepted. A single agent failure does not invalidate the validation — only if 2+ agents fail is the regression validation itself considered failed.

**Rationale**: FR-8 requires adversarial validation of regression findings. The 3-agent majority vote ensures robustness against individual agent failures while keeping the budget impact manageable (REGRESSION_VALIDATION_COST = 15).

**Affected Requirement**: FR-8

---

## OQ-5b: FR-4.1 Threshold Calibration Basis

**Question**: What data was used to calibrate the 0.15 threshold?

**Decision**: The threshold was calibrated empirically based on:
1. Rubric weight distribution: the 4 dimensions have weights summing to 1.0
2. Natural scoring variance: on synthetic test cases, prosecutor-defender score gaps of ≤0.10 were noise; gaps ≥0.20 were signal
3. The 0.15 midpoint maximizes signal-to-noise separation
4. Conservative policy: ties favor CONFIRM_HIGH (false positives over false negatives for safety-critical deviations)

**Rationale**: The threshold may need recalibration as more real-world data accumulates. The current value is conservative and can be tuned downward (more decisive) or upward (more permissive) based on false-positive/false-negative rates observed in production.

**Affected Requirement**: FR-4.1

---

## OQ-6: Cross-File Coherence Check Scope for FR-9

**Question**: What scope should the cross-file coherence check cover after remediation?

**Decision**: The coherence check evaluates whether successful files should be rolled back when related files fail. Scope:
1. For each successfully remediated file, check if any of its findings also reference a failed file
2. If a finding references both a successful and a failed file, roll back the successful file (cascade)
3. The check uses the existing `files_affected` field on Finding objects as the cross-reference key
4. Only first-degree references are checked (no transitive closure)

**Rationale**: Cross-file coherence is critical because remediation patches may create inconsistencies between files. The first-degree check balances safety with simplicity:
- Transitive closure would be more thorough but risks cascading rollbacks of unrelated files
- The `files_affected` field is already populated by structural checkers
- Per-file rollback (T06.01) replaces the all-or-nothing approach, so cascade scope is narrower

**Affected Requirement**: FR-9
