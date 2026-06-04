# Base Selection — Per-Task QA Architectures

## Quantitative Scoring (50% weight)

Per protocol §5.3 quantitative_layer, scored across 5 metrics. NOTE: artifacts here are architecture descriptions, not implementation code; quantitative metrics adapted to descriptive-artifact context.

| Metric | Weight | V1 /task | V2 /task-builder | V3 /sc:task |
|---|---|---|---|---|
| Requirement coverage (vs CONTEXT bullets) | 0.30 | 0.95 | 0.92 | 0.90 |
| Internal consistency (no contradictions) | 0.25 | 1.00 | 1.00 | 1.00 |
| Specificity ratio (concrete vs vague) | 0.15 | 0.85 | 0.90 | 0.88 |
| Dependency completeness (internal refs resolve) | 0.15 | 0.90 | 0.95 | 0.85 |
| Section coverage (vs max) | 0.15 | 0.86 | 1.00 | 0.86 |
| **quant_score** | | **0.92** | **0.95** | **0.90** |

## Qualitative Scoring (50% weight) — Across 5 User-Specified Focus Dimensions

User mapped the 6-dimension rubric to 5 focus areas: correctness, coverage, asymmetric-cost, token-efficiency, operational-realism. Scored 0-1 per dimension; aggregated.

### Correctness — which catches the most real defects?
- V1: 0.75 — phase-gate at execution time grounds verification on actual outputs; cross-phase post-completion catches integration bugs; weakness on test-gaming defense
- V2: 0.85 — 3 orthogonal layers catch different defect classes; AX-5 invented-content axis explicitly defends against QA-agent hallucination; weakness on execution-behavior validation (plan-time only)
- V3: 0.80 — TFEP regression detection via baseline snapshot is structurally sound; weakness on tier-routed skip allowing under-validation in LIGHT/EXEMPT

### Coverage — which has the fewest blind spots?
- V1: 0.72 — covers execution path well; blind on test-modification; blind on partition-agent crash
- V2: 0.85 — 3 layers + DNSP + DM-005 + INV-002/010 freshness; broadest coverage; remaining blind spot: execution behavior
- V3: 0.62 — tier-skipping leaves blind spots in LIGHT-tier work with hidden criticality; Critical Path Override is keyword-only; blind on QA-agent hallucination

### Asymmetric-cost — best handles catastrophic misses?
- V1: 0.60 — fix_authorization with no monotonicity guard can introduce subtle regressions while resolving surface defects
- V2: 0.72 — anti-inflation rule + 3-gate redundancy provide structural protection; plan-time means catastrophic execution misses possible
- V3: 0.92 — TFEP's no-ad-hoc-fixes prohibition is the gold standard for test-gaming protection; forensic ladder formalises catastrophic-miss response

### Token-efficiency — best findings per token?
- V1: 0.55 — phase-gate runs on every phase regardless of need; baseline cost is high
- V2: 0.45 — 3 layers cost 30-50K; DM-005 passthrough reduces some redundancy but total cost is substantial
- V3: 0.92 — tier classification routes verification cost to actual risk; LIGHT/EXEMPT skip is genuinely cheap

### Operational-realism — works across diverse task shapes?
- V1: 0.82 — applies to any MDTM task file; handles code/docs/config equally; phase-gate is shape-agnostic
- V2: 0.62 — A.10/A.10.5 checklists are task-file-shape-oriented; less applicable to non-task-file builders
- V3: 0.70 — tier classification works across shapes but Critical Path Override is path-string-specific (could miss domain-specific criticality)

### Qualitative Summary

| Dimension | V1 | V2 | V3 |
|---|---|---|---|
| Correctness | 0.75 | 0.85 | 0.80 |
| Coverage | 0.72 | 0.85 | 0.62 |
| Asymmetric-cost | 0.60 | 0.72 | 0.92 |
| Token-efficiency | 0.55 | 0.45 | 0.92 |
| Operational-realism | 0.82 | 0.62 | 0.70 |
| **qual_score (mean)** | **0.69** | **0.70** | **0.79** |

### Edge Case Floor Check

The 5-dimension scoring uses no explicit "edge case" dimension; the floor rule from protocol §qualitative_scoring.edge_case_floor does not directly apply. INVARIANT PROBE INV-006 (HIGH UNADDRESSED across all 3) acts as the de-facto edge-case floor and FAILS for all three variants on the dimension of "self-confirmation-bias detection." All three variants are equally ineligible AS THE FINAL BASE on this dimension — informing the merged-recommendation's structural change.

## Position-Bias Mitigation

Per protocol §5.3 position_bias_mitigation, dual-pass evaluation applied:
- Pass 1 (A, B, C order — V1, V2, V3): scores above
- Pass 2 (C, B, A order — V3, V2, V1): scores within 0.02 of Pass 1 on every dimension; no re-evaluation required
- Disagreements found: 0
- Verdicts changed: 0

## Combined Scoring

| Variant | quant × 0.50 | qual × 0.50 | combined |
|---|---|---|---|
| V1 /task | 0.46 | 0.345 | **0.805** |
| V2 /task-builder | 0.475 | 0.350 | **0.825** |
| V3 /sc:task | 0.45 | 0.395 | **0.845** |

## Tiebreaker Protocol

Top-two margin: V3 (0.845) vs V2 (0.825) = 0.020 (2.0% — within tiebreaker threshold of 5%).

- **Level 1 — Debate performance**: V3 won 7 of 14 numbered scoring-matrix rows (C-001 fix authority, C-002 test modification, C-003 regression, C-006 token cost, X-001 fix_auth, X-003 tests-are-wrong, S-004 failure ladder); V2 won 5 (S-002 layer count, C-005 partition, X-004 hallucination, U-003 DNSP, U-004 DM-005). V3 advantage: +2 points.
- **Level 2 — Correctness count**: not applicable (no binary correctness criteria in this debate)
- **Level 3 — Input order**: V1 first; not consulted

**Tiebreaker resolved at Level 1 in favor of V3.**

But: convergence is BLOCKED_BY_INVARIANTS per the §invariant probe gate. The base-selection is therefore CONTINGENT on the merged recommendation addressing INV-006.

## Selected Base: V3 (/sc:task, SuperClaude Tier-Classified Executor)

**Selection rationale**:
- Highest combined score (0.845) with 2-point debate-performance tiebreaker
- Strongest on asymmetric-cost (0.92) and token-efficiency (0.92) — the two dimensions where catastrophic-miss cost and operating-budget converge
- TFEP's VIOLATION-level prohibitions are empirically informed (Goodhart's-law / test-gaming literature) and structurally enforced beyond prompt-level restraint
- Test baseline snapshot is the only automatic regression detector across variants

**Strengths to preserve (from V3 base)**:
- TFEP no-ad-hoc-fixes prohibition (architectural defense against test-gaming)
- Test baseline snapshot pre-implementation (automatic regression detection)
- Forensic ladder graduated escalation (light → standard → FULL-STOP)
- Tier-classified verification routing (cost matched to risk)
- Tests-are-wrong → user adjudication (never auto-edit tests)

**Strengths to incorporate (from non-base variants)**:
- **From V1** (HIGH-value transfers):
  - Cross-phase orphaned-output / missing-output detection (post-completion structural pass)
  - 15-item operational checklist as the STRICT-tier verification depth
  - Mandatory verification floor (eliminate the "EXEMPT tier skips entirely" loophole for any task that touches a tested module)
- **From V2** (HIGH-value transfers):
  - DNSP synthetic-finding protocol (for QA-agent partition failures inside STRICT-tier verification)
  - DM-005 Phase Contract pattern (for the producer/consumer wire between forensic and the next remediation phase)
  - 5 Adversarial Axes (incorporate AX-5 invented-content axis as a hallucination defense at STRICT-tier)
  - Anti-inflation rule (prevent Self-Audit gaming when forensic reports a fix)

**Strengths NOT being incorporated (rejected with rationale)**:
- V1's fix_authorization: true at execution time — REJECTED. V3's prohibition is the operationally safer default. V1's auto-fix model is the test-gaming attack surface.
- V2's plan-time-only scope — REJECTED. The merged base operates at task-time and execution-time; plan-time validation belongs in a separate pre-execution gate, not in the QA architecture.
- V3's tier-routed SKIP for LIGHT/EXEMPT — PARTIALLY REJECTED. Skipping is allowed for tasks that genuinely produce no verifiable output (e.g., status-update items), but the merged recommendation tightens the criteria: ANY task that touches a tested module triggers minimum verification.

**Convergence-block resolution**:
- INV-006 sufficiency_challenge (HIGH UNADDRESSED across all 3) requires a structural addition NOT present in any variant
- Resolution: incorporate `/sc:reflect --mode post --depth deep` as an OUT-OF-CONTEXT independent verifier between QA cycles, per memory `feedback_sc_reflect_vs_inline_rfqa.md` and the SprintRunReflect brainstorm (`.dev/releases/backlog/SprintRunReflect/`)
- This is the structural mechanism that downgrades A-001 from UNSTATED to ADDRESSED and unblocks the convergence gate
