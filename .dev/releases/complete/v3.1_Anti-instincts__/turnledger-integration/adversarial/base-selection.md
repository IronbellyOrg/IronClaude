---
artifact: base-selection
pipeline: sc:adversarial
date: 2026-03-20
base_variant: V3
variants:
  V1: turnledger-refactor-proposal-agent1.md (v3.05 Deterministic Fidelity Gates)
  V2: turnledger-refactor-proposal-agent2.md (v3.1 Anti-Instincts Gate)
  V3: turnledger-refactor-proposal-agent3.md (v3.2 Wiring Verification Gate)
---

# Base Selection

## 1. Quantitative Scoring (50% weight)

### V1: v3.05 Deterministic Fidelity Gates

| Criterion | Weight | Score (0-1) | Weighted |
|-----------|--------|-------------|----------|
| Requirement coverage | 0.30 | 0.85 | 0.255 |
| Internal consistency | 0.25 | 0.90 | 0.225 |
| Specificity ratio | 0.15 | 0.80 | 0.120 |
| Dependency completeness | 0.15 | 0.70 | 0.105 |
| Section coverage | 0.15 | 0.75 | 0.113 |
| **Total** | | | **0.818** |

Rationale: V1 has strong requirement coverage (all FRs addressed with BEFORE/AFTER diffs) and high internal consistency (no contradictions within the proposal). Specificity is high due to concrete cost constants (NR-3). Dependency completeness drops because V1 does not address shared gate infrastructure (`pipeline/gates.py`) or SprintConfig patterns. Section coverage is moderate -- 7 top-level sections but missing pipeline separation analysis and LOC estimates.

### V2: v3.1 Anti-Instincts Gate

| Criterion | Weight | Score (0-1) | Weighted |
|-----------|--------|-------------|----------|
| Requirement coverage | 0.30 | 0.80 | 0.240 |
| Internal consistency | 0.25 | 0.85 | 0.213 |
| Specificity ratio | 0.15 | 0.65 | 0.098 |
| Dependency completeness | 0.15 | 0.80 | 0.120 |
| Section coverage | 0.15 | 0.85 | 0.128 |
| **Total** | | | **0.798** |

Rationale: V2 has broad coverage but is less specific -- many verdicts are "No conflict" or "Compatible" without deep analysis. The table-driven format enforces exhaustive coverage (high section count) but individual entries are sometimes thin. Dependency completeness is higher than V1 because V2 addresses the `pipeline/gates.py` canonical location. Specificity ratio suffers from the absence of code examples, LOC estimates, or formal success criteria.

### V3: v3.2 Wiring Verification Gate

| Criterion | Weight | Score (0-1) | Weighted |
|-----------|--------|-------------|----------|
| Requirement coverage | 0.30 | 0.90 | 0.270 |
| Internal consistency | 0.25 | 0.85 | 0.213 |
| Specificity ratio | 0.15 | 0.90 | 0.135 |
| Dependency completeness | 0.15 | 0.85 | 0.128 |
| Section coverage | 0.15 | 0.90 | 0.135 |
| **Total** | | | **0.880** |

Rationale: V3 covers all spec sections with Status tables, provides code examples (enforcement_mode_label mapping), LOC estimates (U-006), task-level critical path (U-007), formal success criteria SC-012 through SC-015 (U-008), and a concrete missing-field discovery (U-009). Internal consistency is slightly lower than V1 because the `int(1*0.8)=0` rounding problem is identified but accepted without full resolution. Dependency completeness is high because the file manifest resolves all 11 affected files.

### Quantitative Summary

| Variant | Quantitative Score |
|---------|-------------------|
| V1 | 0.818 |
| V2 | 0.798 |
| V3 | **0.880** |

---

## 2. Qualitative Scoring (50% weight) -- 30-Criterion Binary Rubric

### Completeness (5 criteria)

| Criterion | V1 | V2 | V3 |
|-----------|----|----|-----|
| Covers all spec requirements | 1 | 1 | 1 |
| Edge cases addressed | 1 | 0 | 1 |
| Dependencies identified | 0 | 1 | 1 |
| Success criteria defined | 1 | 0 | 1 |
| Out-of-scope boundaries stated | 0 | 1 | 1 |
| **Subtotal** | **3/5** | **3/5** | **5/5** |

Notes: V1 misses cross-pipeline dependencies and scope boundaries. V2 misses edge cases (no mathematical analysis of reimbursement) and formal success criteria. V3 hits all five.

### Correctness (5 criteria)

| Criterion | V1 | V2 | V3 |
|-----------|----|----|-----|
| No factual errors | 1 | 1 | 1 |
| Feasible approaches | 1 | 1 | 1 |
| Consistent terminology | 1 | 1 | 0 |
| No internal contradictions | 1 | 1 | 1 |
| Evidence-backed claims | 1 | 1 | 1 |
| **Subtotal** | **5/5** | **5/5** | **4/5** |

Notes: V3 uses "GateMode" and "GateScope" somewhat interchangeably in places (Sections 4.5c and 8), losing a point for terminology consistency.

### Structure (5 criteria)

| Criterion | V1 | V2 | V3 |
|-----------|----|----|-----|
| Logical ordering | 1 | 1 | 1 |
| Consistent hierarchy | 1 | 1 | 1 |
| Separation of concerns | 0 | 1 | 1 |
| Navigation aids | 0 | 1 | 1 |
| Follows conventions | 1 | 1 | 1 |
| **Subtotal** | **3/5** | **5/5** | **5/5** |

Notes: V1 mixes conflict analysis with resolution inline rather than separating them. V1 also lacks a pipeline separation section (V2's Section 7). V2 and V3 both have clean structural separation.

### Clarity (5 criteria)

| Criterion | V1 | V2 | V3 |
|-----------|----|----|-----|
| Unambiguous language | 1 | 1 | 1 |
| Concrete specifics | 1 | 0 | 1 |
| Clear purpose per section | 1 | 1 | 1 |
| Terms defined | 0 | 1 | 1 |
| Actionable next steps | 1 | 1 | 1 |
| **Subtotal** | **4/5** | **4/5** | **5/5** |

Notes: V1 does not define key TurnLedger terms (debit/credit semantics assumed). V2 lacks concrete code examples or numeric specifics in its resolutions.

### Risk Coverage (5 criteria)

| Criterion | V1 | V2 | V3 |
|-----------|----|----|-----|
| >=3 risks identified | 1 | 1 | 1 |
| Mitigations provided | 1 | 1 | 1 |
| Failure modes addressed | 1 | 1 | 1 |
| External dependencies considered | 0 | 1 | 1 |
| Monitoring mechanisms | 0 | 0 | 1 |
| **Subtotal** | **3/5** | **4/5** | **5/5** |

Notes: V1 does not consider pipeline/gates.py as an external dependency. Neither V1 nor V2 proposes monitoring mechanisms; V3's KPI report extension (NEW-4) serves this role.

### Invariant and Edge Case Coverage (5 criteria)

| Criterion | V1 | V2 | V3 |
|-----------|----|----|-----|
| Collection boundaries | 1 | 0 | 1 |
| State variable interactions | 1 | 1 | 1 |
| Guard condition gaps | 1 | 1 | 1 |
| Count divergence | 1 | 0 | 1 |
| Interaction effects | 0 | 1 | 1 |
| **Subtotal** | **4/5** | **3/5** | **5/5** |

Notes: V1 identifies dual-guard invariant (U-002) and budget model duality (collection boundary). V2 misses mathematical edge cases (reimbursement rounding, count divergence). V3 identifies `int(1*0.8)=0` (count divergence), `ledger=None` handling (guard condition gap), and interaction effects between SprintConfig fields and GateScope.

### Qualitative Summary

| Variant | Completeness | Correctness | Structure | Clarity | Risk | Invariant | Total | Normalized |
|---------|-------------|-------------|-----------|---------|------|-----------|-------|------------|
| V1 | 3 | 5 | 3 | 4 | 3 | 4 | 22/30 | 0.733 |
| V2 | 3 | 5 | 5 | 4 | 4 | 3 | 24/30 | 0.800 |
| V3 | 5 | 4 | 5 | 5 | 5 | 5 | 29/30 | 0.967 |

---

## 3. Composite Score

| Variant | Quantitative (50%) | Qualitative (50%) | Composite |
|---------|--------------------|--------------------|-----------|
| V1 | 0.409 | 0.367 | **0.776** |
| V2 | 0.399 | 0.400 | **0.799** |
| V3 | 0.440 | 0.483 | **0.923** |

---

## 4. Debate Transcript Corroboration

The debate transcript awards wins as follows: V1: 2, V2: 6, V3: 5, TIE: 1.

V2 won more debate points overall, primarily on architectural reasoning (enforcement tier separation, cross-module imports, remediation semantics, gate criteria location). However, V3 won on the dimensions most relevant to base selection: implementation actionability (S-004: 75%, S-005: 80%), concrete mathematical analysis (C-004: 70%), and composability (C-001: 55%).

The debate confirms that V2's strengths are architectural insights that should be *incorporated into* the base, not that V2 should *be* the base. V2's wins on C-002, C-003, C-006, X-001, and X-002 represent ideas that can be merged into V3's more comprehensive structure.

V1's wins (S-002: conflict scheme depth, X-004: functional reimbursement consumer) represent specific techniques (line-level evidence citations, cost constant calibration) that can also be incorporated into V3.

---

## 5. Selection Decision

**Base Variant: V3** (turnledger-refactor-proposal-agent3.md -- v3.2 Wiring Verification Gate)

**Rationale**: V3 scores highest on both quantitative (0.880) and qualitative (0.967) dimensions. It provides the most implementation-ready proposal with task-level critical paths, LOC estimates, formal success criteria, code examples, and concrete edge case discoveries. Its structure (hybrid tables + prose) accommodates merging content from V1 and V2 without structural refactoring.

**Primary strengths of V3 as base**:
- Most complete file manifest with quantified effort (U-006)
- Most granular implementation ordering (U-007)
- Formal success criteria SC-012 through SC-015 (U-008)
- Concrete missing-field discovery blocking remediation (U-009)
- Testable backward compatibility contract (NEW-3, SC-014)

**Primary gaps to fill from V1 and V2**:
- V1's cost constant calibration framework (U-001) and dual-guard invariant (U-002)
- V2's pipeline separation analysis (U-003) and enforcement tier semantics (dual-mode enforcement)
- V2's remediation retry model distinction (gate-check vs. upstream-subprocess)
- V1's line-level evidence citations in conflict analysis
- V2's DeferredRemediationLog failure lifecycle concept (U-005)
