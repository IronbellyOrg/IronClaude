# Base Selection

Source requirements used for RC: the decision scope in `../../context.md`. There are no formal requirement IDs, so the orchestrator used topic matching on nine items: R1 SYM handling, R2 REF handling, R3 DIAG handling, R4 ALLOW handling, R5 reflect symbol chain, R6 nothing left dangling, R7 pinned tests, R8 Phase 3 handoff, R9 independence from the merge shape.

## Quantitative Scoring (50% weight)

| Metric | Weight | V1 (A) | V2 (B) | V3 (C) | Computation notes |
|--------|--------|--------|--------|--------|-------------------|
| Requirement coverage (RC) | 0.30 | 1.00 (9/9) | 0.89 (8/9) | 0.78 (7/9) | B misses R7. C misses R3 (DIAG not stated) and R7 (test not named). |
| Internal consistency (IC) | 0.25 | 0.86 (2 conflicts / 14 claims) | 0.86 (1 / 7) | 1.00 (0 / 9) | A: X-002 and X-003. B: X-001. |
| Specificity ratio (SR) | 0.15 | 0.92 (12 / 13) | 0.86 (6 / 7) | 0.89 (8 / 9) | Vague: A "some steps"; B "larger design task"; C "short native instruction". |
| Dependency completeness (DC) | 0.15 | 0.75 (3 / 4) | 0.67 (2 / 3) | 0.71 (5 / 7) | Unresolved: A "contract tokens already decided"; B and C "acceptance search" (not defined in context.md); C "troubleshoot Tier 1: auggie + Read" (the actual fallback is Glob + Grep). |
| Section coverage (SC) | 0.15 | 1.00 (4 blocks) | 0.75 (3) | 0.75 (3) | No H2 headings in any variant, so paragraph blocks were counted. |
| **quant_score** | | **0.915** | **0.823** | **0.837** | |

## Qualitative Scoring (50% weight) — Additive Binary Rubric

The dual pass was run by the orchestrator sequentially in one context: pass 1 in order V1, V2, V3; pass 2 in order V3, V2, V1. The passes did not disagree on any criterion, so no re-evaluation was needed. Each cell is MET (1) or NOT (0). Evidence is abbreviated in CEV form.

### Completeness
| # | Criterion | V1 | V2 | V3 | Evidence |
|---|-----------|----|----|----|----------|
| 1 | All explicit requirements | 1 | 0 | 0 | V1 covers SYM, REF, impl, DIAG, ALLOW and reflect. V2 leaves steps dangling at the end of Phase 1 (context.md:3 requirement). V3 does not state DIAG. |
| 2 | Edge and failure cases | 1 | 1 | 1 | V1 "best effort"; V2 "if Phase 3 slips"; V3 "fallback is skip". |
| 3 | Dependencies | 1 | 1 | 1 | V1 pinned test; V2 Phase 3 merge; V3 primitive-usage.md. |
| 4 | Success criteria | 1 | 1 | 1 | "no dangling step at any commit" / "no released build" / "acceptance search can be zero". |
| 5 | Out of scope stated | 1 | 1 | 0 | V1 "separate, already decided"; V2 MEM and ACT/NUDGE "already-decided"; V3 says nothing. |

### Correctness
| # | Criterion | V1 | V2 | V3 | Evidence |
|---|-----------|----|----|----|----------|
| 1 | No factual errors | 0 | 1 | 0 | V1 calls the contract-token removal "already decided", but context.md does not say so. V3: the troubleshoot fallback is Glob + Grep, not Read, and the reuse-auditor fallback calls Serena (reuse-auditor.md:131). |
| 2 | Feasible under constraints | 0 | 0 | 0 | V1: Bash inside read-only rosters (X-002). V2: the merge shape is not planned (X-001). V3: the reflect fallback halts every run (contract.py:33). |
| 3 | Consistent terminology | 1 | 1 | 1 | — |
| 4 | No internal contradictions | 1 | 1 | 1 | — |
| 5 | Claims have rationale | 1 | 1 | 1 | For/Against in each. |

### Structure
All five criteria are MET for all three variants: logical order, flat consistent hierarchy, separated concerns, a cross-reference to context.md, and the For/Against decision-option convention. 5 / 5 / 5.

### Clarity
| # | Criterion | V1 | V2 | V3 | Evidence |
|---|-----------|----|----|----|----------|
| 1 | Unambiguous | 1 | 1 | 0 | V3 "mostly", "short native instruction". |
| 2 | Concrete | 1 | 1 | 1 | — |
| 3 | Clear purpose per block | 1 | 1 | 1 | — |
| 4 | Acronyms defined in the doc | 0 | 0 | 0 | SYM, REF, LB etc. are defined only in context.md. |
| 5 | Actionable | 1 | 1 | 1 | — |

### Risk Coverage
| # | Criterion | V1 | V2 | V3 | Evidence |
|---|-----------|----|----|----|----------|
| 1 | ≥3 risks with probability and impact | 0 | 0 | 0 | None gives a probability. |
| 2 | Mitigation per risk | 0 | 0 | 0 | Mitigations are partial or absent. |
| 3 | Failure modes and recovery | 1 | 1 | 1 | — |
| 4 | External dependency failure | 1 | 1 | 1 | Codegraph absent / Phase 3 slip / merge timing. |
| 5 | Validation mechanism | 1 | 1 | 1 | Testable / acceptance search. |

### Invariant & Edge Case Coverage
| # | Criterion | V1 | V2 | V3 | Evidence |
|---|-----------|----|----|----|----------|
| 1 | Collection boundaries | 0 | 0 | 0 | — |
| 2 | Cross-component state | 1 | 1 | 0 | V1: roster and test together. V2: intermediate-commit state across the branch. |
| 3 | Guard gaps | 1 | 0 | 1 | V1 "best effort" marking; V3 identifies the steps with no fallback. |
| 4 | Count divergence | 0 | 0 | 0 | — |
| 5 | Interaction effects | 1 | 1 | 1 | V1: tier above the floor. V2: merge coupling. V3: line drift after edits. |

### Qualitative Summary
| Dimension | V1 | V2 | V3 |
|-----------|----|----|----|
| Completeness | 5 | 4 | 3 |
| Correctness | 3 | 4 | 3 |
| Structure | 5 | 5 | 5 |
| Clarity | 4 | 4 | 3 |
| Risk | 3 | 3 | 3 |
| Invariant/Edge | 3 | 2 | 2 |
| **Total / 30** | **23 (0.767)** | **22 (0.733)** | **19 (0.633)** |

### Edge Case Floor Check
V1 3/5, V2 2/5, V3 2/5. All are eligible (≥1/5).

## Position-Bias Mitigation
| Metric | Value |
|--------|-------|
| Disagreements between pass 1 and pass 2 | 0 |
| Verdicts changed by re-evaluation | 0 |

Caveat: both passes were made by the same evaluator in one context, so this mitigation is weaker than independent passes.

## Combined Scoring
| Variant | Quant ×0.5 | Qual ×0.5 | Final |
|---------|-----------|-----------|-------|
| V1 (option-a) | 0.458 | 0.383 | **0.841** |
| V2 (option-b) | 0.412 | 0.367 | 0.778 |
| V3 (option-c) | 0.418 | 0.317 | 0.735 |

Margin V1 over V2: 6.3%, which exceeds the 5% tiebreak trigger, so no tiebreaker was applied. Debate performance agrees: V1 won 8 points outright, V3 won 1, V2 won 0.

## Selected Base: Variant 1 (option-a.md, architect advocate)

**Rationale.** Highest score on both layers. It is the only variant that covers every scope item (SYM, REF, DIAG, ALLOW, reflect, the pinned tests, the Phase 3 handoff) and is independent of the merge shape. All three advocates chose its approach on 8 points outright, and on 3 more tied with V3.

**Strengths to preserve.** The per-job native-floor mapping; the codegraph slots ledger; the rule that rosters and pinned tests change together; the reflect contract-token concern; the floor as a permanent tier below codegraph; independence from Phase 3 timing.

**Strengths to incorporate.**
- From V3: delete the Serena half instead of rewriting wherever the same step already names a Serena-free native path (C-001, C-008, U-005).
- From V2: edit-once caution. Keep reflect contract and telemetry field names stable in Phase 1, with constant values, so Phase 3 does not redesign them twice (A-003).
- From the debate: the X-002 and X-003 corrections (no Bash in closed rosters; the floor is phrased as the Grep tool); A-004 (floor evidence is normal; the `serena` tokens leave the halt set); the A-001 roster rule; the ledger keyed by file plus step heading (C-002); the reuse-auditor:131 rewrite.
