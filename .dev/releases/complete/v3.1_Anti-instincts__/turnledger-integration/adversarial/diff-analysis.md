---
artifact: diff-analysis
pipeline: sc:adversarial
mode: compare-existing
date: 2026-03-20
variants:
  V1: turnledger-refactor-proposal-agent1.md (v3.05 Deterministic Fidelity Gates)
  V2: turnledger-refactor-proposal-agent2.md (v3.1 Anti-Instincts Gate)
  V3: turnledger-refactor-proposal-agent3.md (v3.2 Wiring Verification Gate)
---

# Diff Analysis: TurnLedger Integration Refactoring Proposals

## 1. Structural Differences

### S-001: Document Organization Pattern

| Aspect | V1 | V2 | V3 |
|--------|----|----|-----|
| Frontmatter | YAML with metadata fields | Blockquote header (no YAML) | YAML with metadata fields |
| Section numbering | 7 top-level sections | 8 top-level sections | 6 top-level sections |
| Executive summary | Present | Absent | Present (as "Overview") |
| Diff format | Prose with "What stays / What changes / What's new" | Table-driven (Aspect / AIG Current / TLD Impact / Verdict) | Table-driven (Aspect / Status) with inline prose |

V2 uses the most structured tabular format. V1 uses the most narrative format. V3 is a hybrid.

### S-002: Conflict Identification Scheme

| Aspect | V1 | V2 | V3 |
|--------|----|----|-----|
| ID scheme | CONFLICT-1 through CONFLICT-6 | CONFLICT-01 through CONFLICT-04 + RISK-01 | C1 through C5 (abbreviated) |
| Severity scale | HIGH / MEDIUM / LOW | Described in verdicts, no formal scale | Medium / Low (explicit labels) |
| Evidence citations | Line-level references to spec and design sections | Section and line references to both AIG and TLD | Section references to design.md |

### S-003: Resolution Format

| Aspect | V1 | V2 | V3 |
|--------|----|----|-----|
| Resolution location | Inline under each conflict + summary table (Section 5) | Dedicated Section 5 with per-conflict resolutions | Dedicated Section 5 with per-conflict resolutions |
| Summary table | Present (Section 5) | Absent (uses Section 6 summary table instead) | Absent |
| Code examples | None in resolutions | None in resolutions | Present (enforcement_mode_label mapping) |

### S-004: Implementation Ordering Depth

| Aspect | V1 | V2 | V3 |
|--------|----|----|-----|
| Ordering section | Section 6: explicit 7-step sequence with rationale | Section 8: 3-phase sequence (AIG Phase 1, TLD Integration, Cross-Pipeline) | Section 6: 7-step update plan referencing spec sections |
| Dependency analysis | Implicit in ordering | Explicit: "Neither blocks the other" | Explicit critical path with parallel tracks |
| Task-level granularity | FR-level ordering | Phase-level ordering | Task ID-level ordering (T01, T01b, T07, etc.) |

### S-005: Scope of "Files Affected"

| Aspect | V1 | V2 | V3 |
|--------|----|----|-----|
| Table present | Yes (Section 7, 5 files) | Absent (deferred to AIG Section 12 reference) | Yes (Section 5, 11 files with LOC estimates) |
| LOC estimates | None | None | Before/after estimates for production and test code |
| Change type classification | MODIFY / NO CHANGE / AMEND | N/A | CREATE / MODIFY / NEW with delta estimates |

---

## 2. Content Differences

### C-001: Budget Model -- Turn-Based vs. Pipeline-Scoped

**V1** treats TurnLedger as a convergence-specific budget engine. The budget governs a closed-loop convergence cycle (catch/verify/backup runs). Cost constants (CHECKER_COST=10, REMEDIATION_COST=8, REGRESSION_VALIDATION_COST=15) are calibrated to this specific workload. Budget is constructed per-convergence-invocation.

**V2** treats TurnLedger as sprint-level infrastructure. The budget spans the entire sprint execution, with gates (including anti-instinct) participating in a shared debit/credit lifecycle. The anti-instinct step has near-zero turn cost. Budget is constructed once per sprint.

**V3** treats TurnLedger as per-task budget accounting. Each task's wiring analysis has a debit/credit cycle (debit_wiring, credit_wiring). The budget is threaded through the executor and is persistent across tasks within a sprint.

These are different scoping decisions driven by the different specs, but they share the same TurnLedger primitive.

### C-002: Enforcement Tier Handling

**V1** does not address enforcement tiers. The convergence gate has a single behavior: pass (0 HIGHs) or fail. There is no shadow/soft/full rollout because convergence is binary.

**V2** identifies a direct conflict between AIG's `enforcement_tier="STRICT"` and TLD's graduated rollout (shadow -> soft -> full). Proposes dual-mode enforcement: intrinsic tier stays STRICT, sprint executor overrides via `gate_rollout_mode`.

**V3** identifies a related conflict where `wiring_gate_mode` strings are replaced by `GateScope` + `resolve_gate_mode()`. Proposes keeping `enforcement_mode` as a derived human-readable label.

### C-003: Cross-Module Import Treatment

**V1** identifies the `sprint/models.py` -> `roadmap/convergence.py` import as CONFLICT-3 (LOW risk). Proposes accepting with a documented tech debt item to migrate TurnLedger to `pipeline/models.py`.

**V2** identifies a different cross-module concern: `roadmap/gates.py` vs. `pipeline/gates.py` (CONFLICT-04). Proposes establishing that `GateCriteria` and `SemanticCheck` are canonical in `pipeline/gates.py`.

**V3** does not flag cross-module imports as a risk. The wiring gate lives in `audit/wiring_gate.py` and the sprint integration is in `sprint/executor.py`, which already imports from `sprint/models.py`.

### C-004: Reimbursement Rate Semantics

**V1** identifies `reimbursement_rate` semantic drift as CONFLICT-4 (MEDIUM risk). The field was designed for sprint cost recovery but is repurposed for convergence progress credits. Proposes accepting for v3.05 with documentation.

**V2** mentions reimbursement only in passing. The anti-instinct gate has near-zero cost, making reimbursement negligible. No conflict flagged.

**V3** identifies the `int(1 * 0.8) = 0` rounding problem as Conflict C4 (MEDIUM severity). This is the most concrete analysis of reimbursement failure modes. Proposes accepting the 1-turn cost with documentation.

### C-005: Backward Compatibility

**V1** addresses backward compatibility through the `convergence_enabled` feature flag. When false, TurnLedger is never constructed. Legacy path is "byte-identical" to pre-v3.05.

**V2** states "AIG can ship first without any TLD dependencies. TLD can ship first without AIG's gate definitions. Neither blocks the other." Backward compatibility is implicit in pipeline separation.

**V3** identifies backward compatibility as a new requirement (NEW-3). The `ledger=None` handling pattern is explicitly called out, with SC-014 as a new success criterion.

### C-006: Remediation Path Design

**V1** describes remediation as a budget-guarded operation: `ledger.can_remediate()` checked before each cycle, `REMEDIATION_COST = 8 turns` debited before execution. Remediation is tightly coupled to the convergence loop.

**V2** describes remediation as an executor-level concern: `attempt_remediation()` re-runs the upstream task subprocess and re-evaluates the gate. Remediation is decoupled from the gate definition (`retry_limit=0` for deterministic gates, but remediation retries the input, not the check).

**V3** describes remediation as a budget-aware path: `attempt_remediation()` is called for BLOCKING failures, with credit-on-successful-remediation. Remediation is integrated into the data flow diagram.

---

## 3. Contradictions

### X-001: Remediation Retry Semantics

**V1** treats remediation as retrying the convergence loop (re-run checkers, re-check findings). The `retry_limit` is governed by the 3-run loop cap plus TurnLedger budget.

**V2** explicitly distinguishes between retrying the gate check (meaningless for deterministic checks) and retrying the upstream subprocess (meaningful). States: "TLD's `attempt_remediation()` does not retry the gate; it retries the *task subprocess*."

These are incompatible retry models. V1's remediation re-runs the same checkers on potentially modified code (after applying patches). V2's remediation re-runs the code generation that produced the artifact being checked. Both are valid for their respective specs, but if a unified remediation model is needed, the retry target (check vs. upstream) must be reconciled.

### X-002: Where Gate Criteria Live

**V1** places all gate logic in `roadmap/convergence.py`. No shared gate infrastructure referenced.

**V2** states `ANTI_INSTINCT_GATE` should live in `roadmap/gates.py` but `GateCriteria` types should be canonical in `pipeline/gates.py`.

**V3** states `WIRING_GATE` lives in `roadmap/gates.py` (or `pipeline/gates.py`) with gate evaluation via `gate_passed()` in `pipeline/gates.py`.

V2 and V3 agree on a `pipeline/gates.py` canonical location. V1 does not address shared gate infrastructure at all, placing everything convergence-specific.

### X-003: SprintConfig Field Design

**V2** does not propose changes to SprintConfig (it addresses the roadmap pipeline's executor).

**V3** proposes replacing `wiring_gate_mode: Literal["off","shadow","soft","full"]` with three fields: `wiring_gate_enabled: bool`, `wiring_gate_scope: GateScope`, `wiring_gate_grace_period: int`.

**V1** does not address SprintConfig (convergence is feature-flagged via `convergence_enabled`).

V1 and V3 use different feature-flag patterns: V1 uses a boolean (`convergence_enabled`), V3 uses a boolean + enum + int triple. If both ship, SprintConfig would have inconsistent gating patterns.

### X-004: reimbursement_rate Production Status

**V1** states `reimbursement_rate` is "currently dead code" and proposes making convergence its first production consumer.

**V3** also states `reimbursement_rate` was dead code and proposes making wiring credits its first production consumer.

Both claim to be the first consumer. If both ship, the semantics must be unified or the field must serve both consumers coherently. V1 uses it for partial-run-cost recovery on convergence progress. V3 uses it for wiring-analysis cost recovery on gate pass. The math differs: V1 computes `int(run_cost * rate)` where run_cost is 10+ turns; V3 computes `int(1 * 0.8) = 0`, which is effectively a no-op.

---

## 4. Unique Contributions

### U-001 (V1 only): Cost Constant Calibration Framework

V1 defines a complete set of module-level cost constants with specific numeric values and derived budget ranges (MIN/STD/MAX). Neither V2 nor V3 provides this level of budget calibration. V1's NR-3 specifies exact values: CHECKER_COST=10, REMEDIATION_COST=8, REGRESSION_VALIDATION_COST=15, CONVERGENCE_PASS_CREDIT=5, and three derived budgets.

### U-002 (V1 only): Dual-Guard Invariant

V1 explicitly identifies that the 3-run loop cap and TurnLedger budget are independent guards that can terminate convergence independently. This dual-guard pattern (structural invariant + economic invariant) is not addressed by V2 or V3.

### U-003 (V2 only): Pipeline Separation Analysis

V2 is the only proposal that explicitly analyzes the roadmap vs. sprint pipeline distinction as a structural architecture concern. Section 7 ("Items in TLD That Do NOT Affect AIG") provides a clear boundary map showing which TLD sections are sprint-only. Neither V1 nor V3 performs this cross-pipeline boundary analysis.

### U-004 (V2 only): Graduated Rollout as Separate Concern

V2 proposes a new Section 13.1 for sprint pipeline rollout, distinguishing it from AIG's Phase 1/Phase 2 (which governs the roadmap pipeline). This separation of rollout strategy by pipeline is unique.

### U-005 (V2 only): DeferredRemediationLog Integration

V2 identifies `DeferredRemediationLog` as a new failure tracking mechanism that replaces binary GATE FAIL with a richer lifecycle (persistent journal, resume recovery, KPI feed). Neither V1 nor V3 addresses deferred remediation logging.

### U-006 (V3 only): LOC Impact Estimation

V3 is the only proposal that provides before/after LOC estimates for every affected file, with production and test code totals. This makes the implementation effort quantifiable.

### U-007 (V3 only): Task-Level Critical Path

V3 provides a revised critical path at task granularity (T01, T01b, T01c, etc.) with explicit parallelism annotations. V1 provides FR-level ordering. V2 provides phase-level ordering.

### U-008 (V3 only): Success Criteria Additions (SC-012 through SC-015)

V3 defines four new success criteria with specific assertion contracts. V1 adds acceptance criteria to existing FRs. V2 adds notes and subsections but no formal success criteria.

### U-009 (V3 only): `scan_duration_seconds` Field Discovery

V3 identifies a concrete missing field on `WiringReport` that blocks the remediation path. This is a specific, actionable finding that neither V1 nor V2 surfaces.

---

## 5. Shared Assumptions

### A-001: TurnLedger API Stability (UNSTATED)

All three proposals assume the TurnLedger API in `sprint/models.py` is stable and will not change between when the proposal is written and when it ships. None discusses versioning or API stability guarantees for TurnLedger.

### A-002: Feature Flags as Sufficient Isolation (UNSTATED)

All three proposals assume that feature flags (`convergence_enabled`, `wiring_gate_enabled`, gate rollout modes) provide sufficient isolation to prevent TurnLedger code from affecting non-TurnLedger paths. None proposes integration tests that verify the flag-off path remains truly inert.

### A-003: Single TurnLedger Instance Per Pipeline Run (UNSTATED)

V1 assumes a TurnLedger constructed per-convergence-invocation. V2 assumes a sprint-level TurnLedger. V3 assumes a TurnLedger threaded through the executor. All assume a single ledger instance -- none addresses what happens if multiple convergence/gate operations share a ledger or if nested pipeline invocations create competing ledger instances.

### A-004: Turn Costs Are Deterministic (UNSTATED)

All three proposals assign fixed turn costs to operations (CHECKER_COST=10, REMEDIATION_COST=8, WIRING_ANALYSIS_TURNS=1). None accounts for variable-cost operations where actual turn consumption depends on input size (e.g., a large spec requiring more checker turns, or a complex wiring analysis requiring more than 1 turn).

### A-005: No Concurrent Access to TurnLedger (UNSTATED)

V1 mentions parallel agent spawning for regression detection but does not address concurrent debit/credit on the same TurnLedger. V2 and V3 do not address concurrency at all. If parallel tasks debit the same ledger, race conditions could produce incorrect budget accounting.

### A-006: Backward Compatibility Means "Old Config Files Still Work" (UNSTATED)

V3 identifies SprintConfig field migration as a risk. V1 mentions byte-identical legacy paths. V2 claims neither spec blocks the other. None defines what backward compatibility means for user-facing configuration: do old YAML/TOML config files with `wiring_gate_mode="shadow"` continue to work, or do they error?

### A-007: reimbursement_rate Default of 0.8 Is Acceptable (UNSTATED)

All proposals that discuss reimbursement_rate accept the 0.8 default without questioning whether this value was chosen for convergence/wiring workloads or was an arbitrary sprint-domain default. V3 notes the `int(1*0.8)=0` rounding problem but still accepts the default.
