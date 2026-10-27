---
artifact: debate-transcript
pipeline: sc:adversarial
mode: compare-existing
date: 2026-03-20
depth: 2-rounds
variants:
  V1: turnledger-refactor-proposal-agent1.md (v3.05 Deterministic Fidelity Gates)
  V2: turnledger-refactor-proposal-agent2.md (v3.1 Anti-Instincts Gate)
  V3: turnledger-refactor-proposal-agent3.md (v3.2 Wiring Verification Gate)
---

# Adversarial Debate Transcript

## Debate Protocol

For each diff point, two rounds of steelman argumentation determine which variant's approach is strongest. Scoring uses: Winner (V1/V2/V3/TIE), Confidence (0-100%), and Evidence (specific citations).

---

## STRUCTURAL DIFFERENCES

### S-001: Document Organization Pattern

**Round 1 -- Steelman for V2 (Table-Driven)**:
V2's table format (Aspect / AIG Current / TLD Impact / Verdict) provides the most scannable format for a reviewer who needs to quickly determine which spec sections are affected. Each row is a self-contained decision point. The "Verdict" column enforces a judgment on every aspect, preventing the proposal from deferring analysis.

**Round 1 -- Steelman for V1 (Narrative)**:
V1's "What stays / What changes / What's new" narrative provides richer context for each FR. When a requirement is complex (e.g., FR-7 with 9 acceptance criteria modifications), a table cannot capture the nuance. V1's narrative format allows explaining WHY something changes, not just THAT it changes.

**Round 2 -- Synthesis**:
V3's hybrid approach inherits advantages of both: tables for quick scanning of unchanged sections, prose for detailed analysis of modified sections. However, V3's tables are simpler (Aspect / Status) and lose V2's "Current vs. Impact" comparison structure.

**Winner**: V2 | **Confidence**: 65% | **Evidence**: V2's 3-column comparison (Current/Impact/Verdict) is the most rigorous format for a diff analysis. The forced "Verdict" column prevents analytical gaps.

### S-002: Conflict Identification Scheme

**Round 1 -- Steelman for V1**:
V1 identifies 6 conflicts with explicit severity ratings (MEDIUM/LOW) and structured resolution recommendations. Each conflict has Evidence, Severity, and Recommended Resolution subsections. The granularity (6 conflicts) provides thorough coverage.

**Round 1 -- Steelman for V3**:
V3 identifies 5 conflicts (C1-C5) with severity labels and provides the most actionable resolutions, including code examples (e.g., the `enforcement_mode_label` mapping). V3 also separates conflicts from risks, distinguishing between incompatibilities and uncertainties.

**Round 2**:
V1's conflict analysis is deeper (Evidence section with line-level citations), but V3's resolutions are more implementation-ready. V2 identifies fewer conflicts (4 + 1 risk) but provides the richest architectural reasoning about pipeline separation.

**Winner**: V1 | **Confidence**: 60% | **Evidence**: V1's Evidence + Severity + Resolution structure per conflict is the most thorough. V3's code examples are useful but V1's line-level citations provide better traceability.

### S-004: Implementation Ordering Depth

**Round 1 -- Steelman for V3**:
V3 provides task-level granularity (T01, T01b, T01c, T06b, T07b, T10b) with explicit dependency chains and parallel annotations. The critical path diagram shows which tasks can run concurrently. This is directly actionable for sprint planning.

**Round 1 -- Steelman for V1**:
V1's FR-level ordering provides a rationale for each ordering decision ("NR-3 requires the checker/remediation/regression code to exist before calibration is meaningful"). The ordering is less granular but more reasoned.

**Round 2**:
V3 wins on actionability. V1 wins on reasoning. V2's phase-level ordering is too coarse for implementation planning but valuable for cross-team coordination.

**Winner**: V3 | **Confidence**: 75% | **Evidence**: V3's task-level critical path with parallelism annotations (`T01 + T01b + T01c (parallel)`) is the most implementation-ready ordering.

### S-005: Scope of "Files Affected"

**Round 1 -- Steelman for V3**:
V3's file manifest includes before/after LOC estimates, change type classification (CREATE/MODIFY/NEW), and totals. This provides quantifiable implementation effort. The 11-file manifest with delta estimates is the most complete.

**Round 1 -- Steelman for V1**:
V1's 5-file table is concise and avoids false precision. LOC estimates for refactoring proposals are inherently unreliable; V1 focuses on change type (MODIFY/NO CHANGE/AMEND) which is more stable information.

**Round 2**:
V3's estimates, even if imprecise, provide a baseline for scoping. V1's simplicity is appropriate if the audience already knows the codebase. V2's absence of a file table is a gap.

**Winner**: V3 | **Confidence**: 80% | **Evidence**: V3 provides production LOC (440-550) and test LOC (420-570) estimates with per-file breakdowns. This is the only proposal that makes implementation effort quantifiable.

---

## CONTENT DIFFERENCES

### C-001: Budget Model Scoping

**Round 1 -- Steelman for V1 (Per-Convergence)**:
V1's per-convergence TurnLedger construction provides the tightest budget isolation. The budget is calibrated to exactly the convergence workload (MIN/STD/MAX budgets). There is no risk of budget bleed from other pipeline operations. The 3-run cap + turn budget dual guard (U-002) is a genuinely novel contribution.

**Round 1 -- Steelman for V3 (Per-Task Threading)**:
V3's per-task budget accounting provides cost visibility across the sprint. The ledger persists across tasks, enabling accumulated metrics (total wiring cost, total credits). This supports KPI reporting (U-008) and long-term cost trend analysis.

**Round 2**:
These are genuinely different architectural choices driven by different specs. V1's per-convergence model is correct for a closed-loop optimization cycle. V3's per-task model is correct for a sprint-wide accounting system. The question is which approach generalizes better. V3's approach scales to multiple gate types sharing a single ledger, while V1's approach requires a new ledger construction per feature.

**Winner**: V3 | **Confidence**: 55% | **Evidence**: V3's per-task threading is more composable. Multiple gates can share a single ledger without per-feature construction logic. V1's model is more isolated but requires explicit ledger lifecycle management per convergence invocation.

### C-002: Enforcement Tier Handling

**Round 1 -- Steelman for V2**:
V2 provides the deepest analysis of enforcement tier semantics. The dual-mode proposal (intrinsic tier + runtime override) cleanly separates gate definition from gate enforcement. The insight that "different pipelines can have different policies" resolves the apparent contradiction.

**Round 1 -- Steelman for V3**:
V3 provides a concrete implementation: the `enforcement_mode_label` mapping that translates GateMode to human-readable strings. This preserves backward compatibility for report consumers while eliminating mode strings from executor logic.

**Round 2**:
V2's analysis is architecturally sounder (separating intrinsic property from runtime behavior). V3's implementation is more practical. V1's omission is appropriate for its spec (convergence has no graduated rollout).

**Winner**: V2 | **Confidence**: 70% | **Evidence**: V2's proposal that `enforcement_tier` is an intrinsic gate property while `gate_rollout_mode` is a runtime override is the cleanest separation of concerns. This applies across all gates, not just anti-instinct.

### C-003: Cross-Module Import Treatment

**Round 1 -- Steelman for V2**:
V2 identifies the most architecturally significant import concern: where do `GateCriteria` and `SemanticCheck` types canonically live? If they are in `pipeline/gates.py`, all gate definitions are importable by all pipelines. If each pipeline defines its own gate infrastructure, types diverge.

**Round 1 -- Steelman for V1**:
V1 identifies the sprint-to-roadmap import direction as a tech debt item with a clear migration path (`pipeline.models`). This is the simplest resolution that unblocks v3.05 without architectural refactoring.

**Round 2**:
V2's concern is more fundamental (type system coherence) while V1's concern is more practical (import direction). V3's non-mention suggests the wiring gate's import structure is already clean.

**Winner**: V2 | **Confidence**: 65% | **Evidence**: V2's identification of the `GateCriteria` canonical location problem (CONFLICT-04) is the most architecturally significant cross-module concern. Resolving it once benefits all three specs.

### C-004: Reimbursement Rate Analysis

**Round 1 -- Steelman for V3**:
V3 is the only proposal that identifies a concrete mathematical failure: `int(1 * 0.8) = 0`. This means the reimbursement mechanism is a no-op at default settings for wiring analysis. V3 also proposes the most options for resolution (free analysis with failure penalty, fractional tracking, separate rate).

**Round 1 -- Steelman for V1**:
V1 identifies semantic drift as the primary risk: the same field serving two different domains (sprint cost recovery vs. convergence progress credit). This is a design-level concern that V3's mathematical analysis does not address.

**Round 2**:
V3 finds the bug. V1 finds the design smell. Both are important, but V3's finding is immediately actionable while V1's is a long-term concern. The combination of both analyses is ideal.

**Winner**: V3 | **Confidence**: 70% | **Evidence**: V3's `int(1*0.8)=0` finding (C4) is the most concrete, testable, and immediately actionable reimbursement analysis. The mechanism literally does not work at default settings.

### C-005: Backward Compatibility Treatment

**Round 1 -- Steelman for V3**:
V3 treats backward compatibility as a first-class requirement (NEW-3) with a success criterion (SC-014: `run_post_task_wiring_hook` works with `ledger=None`). This makes backward compatibility testable.

**Round 1 -- Steelman for V1**:
V1's "byte-identical legacy path" claim is the strongest backward compatibility guarantee: when `convergence_enabled=False`, the code path is literally unchanged. No new objects constructed, no new branches taken.

**Round 2**:
V1's guarantee is stronger (byte-identical) but harder to verify. V3's guarantee is weaker (ledger=None handling) but testable via SC-014. V2's guarantee is implicit in pipeline separation.

**Winner**: TIE (V1 and V3) | **Confidence**: 50% | **Evidence**: V1 provides the strongest guarantee ("byte-identical"). V3 provides the most testable guarantee (SC-014). Different strengths, both valuable.

### C-006: Remediation Path Design

**Round 1 -- Steelman for V2**:
V2 makes the critical distinction between "retrying the gate check" (meaningless for deterministic gates) and "retrying the upstream subprocess" (meaningful). This insight applies to all deterministic gates, not just anti-instinct. The architectural clarity is superior.

**Round 1 -- Steelman for V1**:
V1's remediation model is tightly integrated with budget: `ledger.can_remediate()` prevents unfunded remediation, and `REMEDIATION_COST = 8 turns` makes the cost explicit. The budget guard prevents runaway remediation loops.

**Round 2**:
V2 identifies what remediation MEANS. V1 identifies what remediation COSTS. V3 provides the most complete data flow. V2's conceptual clarity is the most valuable contribution because it prevents architectural errors in all three specs.

**Winner**: V2 | **Confidence**: 72% | **Evidence**: V2's distinction between gate-check retry and upstream-subprocess retry (CONFLICT-02 analysis) is an architectural insight that prevents misimplementation across all specs.

---

## CONTRADICTIONS

### X-001: Remediation Retry Semantics

**Round 1 -- V1 position**: Remediation re-runs checkers on modified code. This is appropriate for convergence because the fix (patch application) modifies the artifact being checked. The checker is deterministic given the same input, but the input changes after remediation.

**Round 1 -- V2 position**: Remediation re-runs the upstream subprocess. This is appropriate for anti-instinct because the gate checks are deterministic on the same artifact. The only way to change the outcome is to regenerate the artifact.

**Round 2**: Both positions are correct for their respective specs. The contradiction arises only if a unified remediation model is required. Since TurnLedger is shared infrastructure, the remediation model should be parameterized: remediation target (check vs. upstream vs. both) should be configurable per gate.

**Winner**: V2 | **Confidence**: 65% | **Evidence**: V2's model is more general. "Retry the upstream subprocess" subsumes "retry the check on modified code" because modifying code IS an upstream subprocess. V1's model is a special case of V2's.

### X-002: Gate Criteria Location

**Round 1**: V2 and V3 agree on `pipeline/gates.py` as canonical. V1 does not address shared infrastructure.

**Round 2**: V2 and V3's agreement is evidence of the correct architectural direction. V1's omission is a gap, not a contradiction.

**Winner**: V2 | **Confidence**: 80% | **Evidence**: V2 provides the most explicit analysis (CONFLICT-04) and resolution (confirm `GateCriteria` in `pipeline/gates.py`). V3 implicitly agrees.

### X-003: SprintConfig Field Design

**Round 1 -- V3 position**: Three fields (`enabled`, `scope`, `grace_period`) provide richer configuration semantics than a single mode string. Phase transitions become config-only changes.

**Round 1 -- V1 position**: A single boolean (`convergence_enabled`) is simpler and sufficient for the convergence use case.

**Round 2**: These are not truly contradictory because they govern different features. But they establish inconsistent patterns on SprintConfig. V3's three-field pattern is more flexible but adds configuration complexity.

**Winner**: V3 | **Confidence**: 60% | **Evidence**: V3's three-field pattern enables config-only phase transitions (Section 8 rollout plan). V1's boolean is sufficient for convergence but does not support graduated rollout.

### X-004: reimbursement_rate First Consumer

**Round 1**: Both V1 and V3 claim to activate dead code. If both ship, neither is truly "first" -- the field serves two consumers with different arithmetic properties.

**Round 2**: The resolution is straightforward: acknowledge both consumers in the `reimbursement_rate` field documentation. The semantic ("fraction of cost returned on success") is compatible across both use cases. V3's rounding problem is a calibration issue, not a semantic conflict.

**Winner**: V1 | **Confidence**: 60% | **Evidence**: V1's consumption actually produces nonzero credits (`int(10 * 0.8) = 8`), making it the first FUNCTIONAL consumer. V3's consumption produces zero credits at default settings, making it dead code in practice.

---

## UNIQUE CONTRIBUTIONS

### U-001 (V1): Cost Constant Calibration

**Assessment**: High value. No other proposal provides specific numeric values for budget calibration. Without these constants, TurnLedger integration is abstract. V1's NR-3 is the only proposal that makes budget enforcement testable with concrete values.

**Score**: 9/10

### U-002 (V1): Dual-Guard Invariant

**Assessment**: High value. The insight that loop cap and turn budget are independent guards with different failure modes (structural vs. economic) is architecturally important. This pattern should be adopted in V3's wiring gate as well.

**Score**: 8/10

### U-003 (V2): Pipeline Separation Analysis

**Assessment**: High value. V2's Section 7 ("Items in TLD That Do NOT Affect AIG") is the only boundary analysis that explicitly maps which TLD sections are sprint-only. This prevents over-integration.

**Score**: 9/10

### U-004 (V2): Graduated Rollout Separation

**Assessment**: Medium value. Distinguishing roadmap rollout from sprint rollout is correct but somewhat obvious given the pipeline separation. The value is in making it explicit.

**Score**: 6/10

### U-005 (V2): DeferredRemediationLog

**Assessment**: Medium value. Novel failure lifecycle concept (persistent journal, resume, KPI feed). However, this is a TLD feature description rather than a spec integration analysis.

**Score**: 5/10

### U-006 (V3): LOC Estimation

**Assessment**: Medium-high value. Quantified implementation effort is useful for planning. The before/after comparison shows TurnLedger integration increases scope by ~25% for production code and ~35% for test code.

**Score**: 7/10

### U-007 (V3): Task-Level Critical Path

**Assessment**: High value. Directly actionable for sprint planning. The parallel annotations enable faster implementation.

**Score**: 8/10

### U-008 (V3): Success Criteria (SC-012 to SC-015)

**Assessment**: High value. Formal success criteria with specific assertion contracts make the proposal testable. SC-014 (null ledger backward compatibility) is particularly important.

**Score**: 8/10

### U-009 (V3): scan_duration_seconds Discovery

**Assessment**: High value. A concrete missing-field finding that would block implementation. Neither V1 nor V2 identifies this at the data model level.

**Score**: 7/10

---

## SHARED ASSUMPTIONS EVALUATION

### A-001 (API Stability): Risk = MEDIUM
If TurnLedger changes between proposal and implementation, all three proposals break. Mitigation: pin TurnLedger interface version or define an adapter.

### A-002 (Feature Flag Isolation): Risk = MEDIUM
None proposes testing the flag-off path. Mitigation: add integration tests that verify zero TurnLedger construction when flags are off.

### A-003 (Single Instance): Risk = LOW-MEDIUM
Nested pipeline invocations (sprint task that triggers roadmap) could create competing ledgers. Mitigation: document ledger lifecycle and ownership.

### A-004 (Deterministic Costs): Risk = LOW
Fixed costs are acceptable for v1 calibration. Variable costs can be addressed in future releases.

### A-005 (No Concurrency): Risk = LOW
V1's parallel regression detection is the only concurrent access pattern. Mitigation: debit before spawning (V1 already proposes this).

### A-006 (Config Backward Compat): Risk = MEDIUM (V3 only)
V3's SprintConfig field replacement could break existing configs. V3 acknowledges this (C5) and proposes implementing the three-field form directly.

### A-007 (Default Rate): Risk = LOW
The 0.8 default is acceptable for v1. V3's rounding problem is a calibration issue, not a fundamental design flaw.

---

## Debate Summary Scores

| Diff Point | Winner | Confidence | Key Evidence |
|------------|--------|------------|--------------|
| S-001 | V2 | 65% | 3-column comparison with forced Verdict |
| S-002 | V1 | 60% | Evidence + Severity + Resolution per conflict |
| S-004 | V3 | 75% | Task-level critical path with parallelism |
| S-005 | V3 | 80% | Before/after LOC estimates per file |
| C-001 | V3 | 55% | Per-task composability over per-convergence isolation |
| C-002 | V2 | 70% | Intrinsic tier vs. runtime override separation |
| C-003 | V2 | 65% | GateCriteria canonical location identification |
| C-004 | V3 | 70% | int(1*0.8)=0 concrete mathematical failure |
| C-005 | TIE | 50% | V1 stronger guarantee, V3 more testable |
| C-006 | V2 | 72% | Gate-check vs. upstream-subprocess distinction |
| X-001 | V2 | 65% | More general remediation model |
| X-002 | V2 | 80% | Explicit CONFLICT-04 analysis |
| X-003 | V3 | 60% | Three-field pattern enables config-only transitions |
| X-004 | V1 | 60% | Only functional consumer (nonzero credits) |

**Wins by variant**: V1: 2, V2: 6, V3: 5, TIE: 1
